# Microsoft Independent Publisher submission

This connector is built, validated, and published. What remains is the
Independent Publisher certification flow with Microsoft. Steps are grouped by
who does them.

## Status

- PR: microsoft/PowerPlatformConnectors#4222, opened from `blue-d3v`
  (branch `polydoc-ip-proposal`). CLA signed 2026-06-25. Full connector files
  (`apiDefinition.swagger.json`, `apiProperties.json`, `readme.md`) added
  2026-07-01; title still `Proposal - ...` (prefix drops at final submission
  once screenshots exist).
- Cert team engaged the PR 2026-07-02 (first human contact). Their comment: (1)
  "prepare connector package and upload as part of the artifacts" (links the
  general certification-submission doc), (2) follow the IP cert process, (3)
  remove `Proposal -` from the title "when the IP connector policy [is] met".
  This is largely boilerplate. See section F for what actually applies.
- The two real gates now: OneVet verified credentials (not started; no form
  link received) and the operation screenshots (need a tenant import). Both are
  Tobias-only. Everything file-side is done and compliant.
- Connector files (`PolyDoc/`): complete and validated (OpenAPI 2.0 passes).
- `iconBrandColor`: `#da3b01` (the mandatory Independent Publisher color).
- `info.title`: `PolyDoc (Independent Publisher)` (required naming pattern; the
  30-char limit applies to the base name only).
- `x-ms-connector-metadata`: Website, Privacy policy, Categories set.
- Support contact: `hello@polydoc.tech` in `info.contact`.
- Premium note in `PolyDoc/README.md` is correct: flows using this connector
  need a Power Automate Premium plan.

## A. File touch-ups (done)

Premium claim corrected, connector metadata added, title suffixed. Nothing
left here.

When building the submission PR, do NOT copy `PolyDoc/settings.json` into the
Microsoft repo. It is a local paconn helper, not a submission artifact.

## B. Verified credentials (One Vet) — Tobias only

The submission is bound to a real person's verified identity AND the GitHub
account that opens the PR. Anonymous or generic org accounts do not pass: the
GitHub profile name must match a government-issued ID.

Vendor: AU10TIX. App: Microsoft Authenticator. Time: ~15 min. You have 30 days
to finish once started. The credential is reusable for all future PRs and
expires after 1 year or at ID expiry.

1. Pick the submission GitHub account. Its profile name must match your
   government ID (passport / driver's license), and its registered email must
   be one you monitor. This account can be separate from the build account
   (`polydoc-tech`). Account is `blue-d3v`; profile name `Tobias Satzger` (OK).

   LIKELY BLOCKER (found 2026-07-01): `blue-d3v` has **no public email**. The
   cert team "sends an email to the email account associated with your GitHub
   profile" (verified-credentials-ip doc). With no visible email, a human has
   no address to write to. Fix: GitHub Settings > Public profile > set Public
   email to a monitored inbox (e.g. hello@polydoc.tech). That same address is
   entered at AU10TIX for the PIN, so it must be a real inbox on the account.
2. Install Microsoft Authenticator on your phone.
3. Trigger verification by opening a proposal PR (see step C/D) from that
   account. Microsoft has no standalone "request verification" portal; opening
   the PR is what starts it.
4. Microsoft emails the GitHub-registered address a form. Fill it so the form,
   your GitHub profile, and your government ID all match.
5. You then get an AU10TIX email. Open its link in a private window: enter the
   email PIN, your phone number, photograph your ID, take a selfie.
6. Add the resulting Verified ID to Microsoft Authenticator. Done.

## C. Operation screenshots — DONE 2026-07-07

Captured against a live tenant. Files in `tools/tmp/` (Screen Shot 2026-07-07
at 21.12/21.17/21.19/21.20):
1. ConvertToPdf - 200, application/pdf, body %PDF-1.7.
2. CaptureScreenshot - 200, image/png.
3. ConvertToPdf + e-invoice (facturx / en16931, verify:true) - 200,
   application/pdf with embedded Factur-X metadata. E-invoice is a mode of
   ConvertToPdf, not a separate operation, so this is a bonus showcase.
4. Definition tab - both operations, verb POST, api.polydoc.tech/pdf/convert.

How it was done (repeatable):
- `connectors@polydoc.tech` has Premium in env
  `Default-879b76bf-6137-4078-9740-64b497de3840` (Custom connectors visible).
- paconn session re-auth: device-code login. paconn's `print(code['message'])`
  is block-buffered when stdout isn't a TTY, so the code never surfaces; run
  `/tmp/paconn_login.py` (flushes the code, writes the token via TokenManager).
  Defaults: client_id 04b07795-8ddb-461a-bbee-02f9e1bf7b46, tenant common,
  resource https://service.powerapps.com/.
- Connector pushed with `paconn create -e <ENV> -d apiDefinition.swagger.json
  -p apiProperties.json -i icon.png`. It creates the connector, then crashes at
  the local settings.json overwrite prompt (NoTTYException) - the connector is
  already created at that point. Connector id:
  `shared_polydoc-20-28independent-20publisher-29-5fe90c6-df19e27a38e78b61`
  (now saved in PolyDoc/settings.json with the env).
- Test tab lives behind the pencil/edit icon (not the `...` menu). Raw Body
  toggle accepts pasted JSON, so nested e-invoice needs no form filling.
- Validated request bodies live-tested first (all 200): bodies in
  scratchpad/body_{pdf,screenshot,einvoice}.json.
- X-Sandbox swagger default is "false" (production safe); the Test runs used
  true (watermarked, separate quota) which is fine for screenshots.

GitHub has no API to upload images into a PR comment/description (drag-drop
only). To post via gh, images must be hosted with a public raw URL first
(e.g. committed to polydoc-tech/power-automate-polydoc). Otherwise Tobias
drag-drops them into the PR in the browser as blue-d3v.

## D. The PR — mostly automatable, final click is Tobias

1. From the verified account, fork `microsoft/PowerPlatformConnectors`.
2. Copy `PolyDoc/` (without `settings.json`) into
   `independent-publisher-connectors/PolyDoc/`.
3. Open the PR. Title: `PolyDoc (Independent Publisher)`. Add label
   `independent-publisher-connector`. Fill the PR template checklist. Paste the
   3 screenshots into the body.

The documented path opens a `Proposal - PolyDoc (Independent Publisher)` PR
first (this is also the verification trigger in step B), then drops the
`Proposal -` prefix and adds all files when ready.

## E. Review — automatable responses, Tobias relays account actions

Swagger Validator and Breaking Change bots run automatically. A Microsoft
reviewer follows. Average deployment is ~15 business days. Updates must come
from the same publisher account that opened the PR.

## F. Reviewer response (2026-07-02) and the package.zip question

The cert-team comment asked us to "prepare connector package and upload as part
of the artifacts" and pointed at the general certification-submission doc. That
doc's packaging flow (maker-portal solution export, `package.zip`, the
ConnectorPackageValidator.ps1 nested-solution structure, Partner Center) is the
**verified-publisher** path. It leaked into the IP doc's Step 6 during a doc
merge. Verified against the repo:

- Merged IP connector folders universally ship exactly
  `{apiDefinition.swagger.json, apiProperties.json, readme.md}` (~88% of 461).
- Zero IP connectors ship a Dataverse solution export
  (`customizations.xml`/`solution.xml`) - the validator's structure.
- A minority (~16/461) additionally include a paconn-style
  `ConnectorPackage.zip`. It is optional, not a merge gate.

Conclusion: we do NOT build the solution-export package.zip. Our 3 files are the
required set and are already present. If the reviewer insists on a packaged
artifact, add a paconn `ConnectorPackage.zip` (produced by `paconn download`
during the tenant session, alongside the screenshots) - not the .ps1 structure.

Compliance re-check against certification-submission Step 1/Step 3 (done, all
pass): title base `PolyDoc` (7 chars, < 30), no banned words; description 30-500
chars, no product names; operation summaries short; descriptions end with
punctuation; exact response schemas (200 + 4xx), no empty operations/props;
APIKey `uiDefinition` shape matches the doc example; `iconBrandColor` `#da3b01`.

`paconn validate` result (2026-07-02, logged in as connectors@polydoc.tech):
"Swagger certification succeeded with warnings." Zero errors. Two advisory
warnings, both expected for a binary-file connector and both left as-is:
- `produces` MIME types (application/pdf, image/png/jpeg/webp) are "not
  supported" per the validator's list (json/text/form only). Leaving them:
  they are the honest content types for a file download; swapping to
  application/json to silence the warning would misrepresent the response. The
  binary body is driven by the 200 `format: binary` schema regardless.
- Each operation has "more than one response with specified schema, only one
  used in the designer" - because we document 400/401/402/403/429 with an
  ErrorResponse schema alongside 200. Kept: the 4xx docs are useful; the warning
  is informational.
The speculative `x-ms-summary` punctuation concern (`/`, `%`) did NOT fire -
those labels are fine, leave them.

## G. OneVet verified credentials (Step 5) - the actual gate, Tobias only

Same substance as section B, restated as the current blocker. No autogenerated
form link has arrived. Now that a human is on the PR, the fastest unblock is to
ask them in a PR reply how to initiate the verified-credentials process (draft
prepared 2026-07-02). Keep `blue-d3v`'s public email set to a monitored inbox so
the outreach can reach it. Do not sign anything on Tobias' behalf.
