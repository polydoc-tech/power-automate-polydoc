# power-automate-polydoc

A Microsoft Power Platform **certified independent publisher connector** for
[PolyDoc](https://polydoc.tech):
HTML/URL to PDF, screenshots, and EU hybrid e-invoices (ZUGFeRD / Factur-X).
This is the Power Automate / Power Apps / Copilot Studio counterpart of the
published [`n8n-nodes-polydoc`](https://www.npmjs.com/package/n8n-nodes-polydoc)
node, built from the same product model in `../../CONNECTOR-PLAYBOOK.md`.

It targets the Microsoft **Independent Publisher** program, so the layout under
`PolyDoc/` matches the
[microsoft/PowerPlatformConnectors](https://github.com/microsoft/PowerPlatformConnectors)
`independent-publisher-connectors/<Name>/` convention.

## Layout

```
PolyDoc/
  apiDefinition.swagger.json   OpenAPI 2.0 - the connector operations and body schemas
  apiProperties.json           auth (API key + Bearer policy), brand color, publisher
  settings.json                paconn settings (connectorId/environment filled at deploy time)
  icon.png                     connector icon (PolyDoc mark on the brand color)
  icon.svg                     icon source
  README.md                    connector README (ships with the IP submission)
  intro.md                     connector intro (ships with the IP submission)
example-flows/                 the three use-case bodies (PDF / screenshot / e-invoice)
```

## Connector shape

One connector, two actions, three angles:

- **Convert to PDF** -> `POST /pdf/convert`
- **Capture screenshot** -> `POST /screenshot/convert`
- **Generate e-invoice** -> the Convert to PDF action with the `eInvoice` body
  populated (e-invoices route through `/pdf/convert`, exactly as in the n8n node)

The full PolyDoc request body is modelled as typed fields (layout, screenshot
settings, e-invoice, render, request, cloud storage, webhook), so flow authors
get rich field mapping rather than a raw JSON blob.

## Authentication

Each connection collects only the PolyDoc API key (a `securestring` connection
parameter). A `setheader` policy in `apiProperties.json` builds the
`Authorization: Bearer <key>` header, so users never type the `Bearer ` prefix.

> The policy is verified by schema (`paconn validate`) and at runtime: both
> operations returned 200 from a tenant import with only the API key in the
> connection. It has not been re-verified on the certified connector, which is
> a separate deployment of the same definition. If that surfaces a problem with
> the per-connection policy reference, the fallback is a plain `apiKey` security
> definition on the `Authorization` header where the user pastes `Bearer <key>`.

## Validate

```bash
# paconn from a throwaway venv
python3 -m venv .venv && . .venv/bin/activate && pip install paconn
paconn validate --api-def PolyDoc/apiDefinition.swagger.json
```

## Test the bodies

See `example-flows/README.md` for `curl` commands that exercise each body
against the live API in sandbox mode.

## Status

Certified and merged. The connector is published in
[microsoft/PowerPlatformConnectors](https://github.com/microsoft/PowerPlatformConnectors/tree/dev/independent-publisher-connectors/PolyDoc)
under `independent-publisher-connectors/PolyDoc/`.

- Definition, properties, icon, READMEs and the three example bodies validated
  and smoke-tested against the live API in sandbox mode.
- Imported into a Power Automate tenant; both operations and the e-invoice mode
  of **Convert to PDF** returned 200, with operation screenshots captured.
- Independent Publisher submission
  [#4222](https://github.com/microsoft/PowerPlatformConnectors/pull/4222):
  OneVet verification completed 2026-08-10, certification approved 2026-08-14,
  merged 2026-09-08.

Remaining: Microsoft's production deployment, which it puts at three to four
weeks from approval and rolls out by region. Until it lands, the connector is
not selectable in Power Automate and
`learn.microsoft.com/en-us/connectors/polydocip/` returns 404.

`package.zip` (the solution-export artifact the certification process requires)
is committed upstream but deliberately not committed here: it is a build
artifact, rebuilt with the `pac` recipe in `SUBMISSION.md` and structurally
checked with `scripts/validate_package.py`.
