#!/usr/bin/env python3
"""Runs validate_package.py as a subprocess against package.zip files built here.

package.zip is a build artifact and is not committed, so the packages are built from the
layout of a real export: an outer zip with intro.md and the .pdpkg.zip, a PkgAssets folder,
and one solution zip each for the connector and the flow.

Run: python3 scripts/validate_package.test.py
"""

import io
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

SCRIPT = Path(__file__).with_name('validate_package.py')

# The connector solution of a real export carries an empty <Workflows/>. The validator must
# not count it as a flow, or the connector solution reads as a second flow.
CONNECTOR_XML = (
    '<ImportExportXml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
    '<Entities/><Workflows/>'
    '<Connectors><Connector><name>polydoc</name></Connector></Connectors>'
    '</ImportExportXml>')
FLOW_XML = (
    '<ImportExportXml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
    '<Workflows><Workflow WorkflowId="{1}" Name="Test flow"><Type>1</Type></Workflow></Workflows>'
    '<Connectors><Connector><name>polydoc</name></Connector></Connectors>'
    '</ImportExportXml>')
PLUGIN_XML = (
    '<ImportExportXml><Workflows/>'
    '<Connectors><Connector><name>polydoc</name></Connector></Connectors>'
    '<aicopilot_aiplugins><aicopilot_aiplugin><name>p</name></aicopilot_aiplugin></aicopilot_aiplugins>'
    '</ImportExportXml>')


def solution(customizations, folders, drop=()):
    files = {
        '[Content_Types].xml': '<Types/>',
        'customizations.xml': customizations,
        'solution.xml': '<ImportExportXml/>',
    }
    for folder in folders:
        files[f'{folder}/item.json'] = '{}'
    return {k: v for k, v in files.items() if k not in drop}


def connector(**kw):
    return solution(CONNECTOR_XML, ['Connector'], **kw)


def flow(**kw):
    return solution(FLOW_XML, ['Connector', 'Workflows'], **kw)


def zip_bytes(files):
    """files maps a name to str, bytes, or a dict, which becomes a nested zip."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w') as z:
        for name, content in files.items():
            if isinstance(content, dict):
                content = zip_bytes(content)
            z.writestr(name, content)
    return buf.getvalue()


def package(solutions=None, assets_extra=None, pdpkg_extra=None, outer_extra=None):
    if solutions is None:
        solutions = {'PolyDocConnector_1_0_0_1.zip': connector(),
                     'PolyDocFlow_1_0_0_1.zip': flow()}
    pdpkg = {'PkgAssets/ImportConfig.xml': '<configdatastorage/>',
             'PkgAssets/manifest.ppkg.json': '{}',
             'PolyDocPackage.dll': b'MZ',
             '[Content_Types].xml': '<Types/>'}
    pdpkg.update({f'PkgAssets/{name}': files for name, files in solutions.items()})
    pdpkg.update(pdpkg_extra or {})
    pdpkg.update({f'PkgAssets/{name}': content for name, content in (assets_extra or {}).items()})
    outer = {'intro.md': '# PolyDoc', 'PolyDocPackage.1.0.0.pdpkg.zip': pdpkg}
    outer.update(outer_extra or {})
    return outer


class ValidatePackage(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.dir.cleanup)

    def run_on(self, outer, *args):
        path = Path(self.dir.name) / 'package.zip'
        path.write_bytes(zip_bytes(outer))
        return subprocess.run([sys.executable, str(SCRIPT), str(path), *args],
                              capture_output=True, text=True)

    def assert_fails(self, result, message):
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn('Validation failed', result.stdout)
        self.assertIn(message, result.stdout)

    def test_a_package_shaped_like_the_real_export_passes(self):
        result = self.run_on(package())
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('PolyDocConnector_1_0_0_1.zip: Connector=True Workflows=False', result.stdout)
        self.assertIn('-> connector', result.stdout)
        self.assertIn('-> flow', result.stdout)
        self.assertIn('Validation successful', result.stdout)

    def test_no_argument_prints_the_usage_and_exits_2(self):
        result = subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn('Usage:', result.stdout)

    def test_level_1_refuses_a_folder_in_the_outer_zip(self):
        self.assert_fails(self.run_on(package(outer_extra={'extra/notes.txt': 'x'})),
                          'Level 1: outer zip must contain no folders')

    def test_level_1_refuses_a_second_markdown_file(self):
        self.assert_fails(self.run_on(package(outer_extra={'README.md': 'x'})),
                          'Level 1: expected exactly 1 .md')

    def test_level_1_refuses_an_outer_zip_without_the_pdpkg(self):
        self.assert_fails(self.run_on({'intro.md': '# PolyDoc'}),
                          'Level 1: expected exactly 1 .zip')

    def test_level_2_refuses_a_second_folder_in_the_pdpkg(self):
        self.assert_fails(self.run_on(package(pdpkg_extra={'Other/x.txt': 'x'})),
                          'Level 2: .pdpkg.zip must contain exactly 1 folder')

    def test_level_3_refuses_a_subfolder_in_pkgassets(self):
        self.assert_fails(self.run_on(package(assets_extra={'nested/x.txt': 'x'})),
                          "Level 3: 'PkgAssets' must contain no subfolders")

    def test_level_3_refuses_a_missing_solution_zip(self):
        self.assert_fails(self.run_on(package(solutions={'C.zip': connector()})),
                          'must contain exactly 2 solution zips; found 1')

    def test_with_the_plugin_flag_level_3_wants_three_solution_zips(self):
        self.assert_fails(self.run_on(package(), 'y'),
                          'must contain exactly 3 solution zips; found 2')

    def test_with_the_plugin_flag_a_plugin_solution_passes(self):
        solutions = {'C.zip': connector(), 'F.zip': flow(),
                     'P.zip': solution(PLUGIN_XML, ['Connector'])}
        result = self.run_on(package(solutions=solutions), 'y')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('-> plugin', result.stdout)

    def test_with_the_plugin_flag_a_third_solution_that_is_no_plugin_fails(self):
        solutions = {'C.zip': connector(), 'F.zip': flow(), 'C2.zip': connector()}
        self.assert_fails(self.run_on(package(solutions=solutions), 'y'),
                          'plugin enabled but no valid plugin solution')

    def test_a_solution_without_solution_xml_fails(self):
        solutions = {'C.zip': connector(drop=['solution.xml']), 'F.zip': flow()}
        self.assert_fails(self.run_on(package(solutions=solutions)),
                          "solution 'C.zip' missing ['solution.xml']")

    def test_a_connector_node_without_its_folder_fails(self):
        solutions = {'C.zip': solution(CONNECTOR_XML, []), 'F.zip': flow()}
        self.assert_fails(self.run_on(package(solutions=solutions)),
                          "solution 'C.zip' has a Connector node but no 'Connector' folder")

    def test_a_flow_without_its_workflows_folder_fails(self):
        solutions = {'C.zip': connector(), 'F.zip': solution(FLOW_XML, ['Connector'])}
        self.assert_fails(self.run_on(package(solutions=solutions)),
                          "solution 'F.zip' is a flow solution but missing Connector/Workflows folder")

    def test_two_connector_solutions_and_no_flow_fail(self):
        solutions = {'C1.zip': connector(), 'C2.zip': connector()}
        self.assert_fails(self.run_on(package(solutions=solutions)),
                          'no valid flow solution')

    def test_two_flow_solutions_and_no_connector_fail(self):
        solutions = {'F1.zip': flow(), 'F2.zip': flow()}
        self.assert_fails(self.run_on(package(solutions=solutions)),
                          'no valid connector-only solution')


if __name__ == '__main__':
    unittest.main()
