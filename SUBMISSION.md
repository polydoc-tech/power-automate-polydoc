# Microsoft Independent Publisher submission

This connector is built, validated, and published. What remains is the
Independent Publisher certification flow with Microsoft. Steps are grouped by
who does them.

## Status

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
   (`polydoc-tech`).
2. Install Microsoft Authenticator on your phone.
3. Trigger verification by opening a proposal PR (see step C/D) from that
   account. Microsoft has no standalone "request verification" portal; opening
   the PR is what starts it.
4. Microsoft emails the GitHub-registered address a form. Fill it so the form,
   your GitHub profile, and your government ID all match.
5. You then get an AU10TIX email. Open its link in a private window: enter the
   email PIN, your phone number, photograph your ID, take a selfie.
6. Add the resulting Verified ID to Microsoft Authenticator. Done.

## C. Three operation screenshots — Tobias only

Microsoft requires one screenshot per operation showing it working.

1. Import `PolyDoc/apiDefinition.swagger.json` + `apiProperties.json` as a
   custom connector in a Power Automate environment. `backend@polydoc.tech` has
   a Premium trial.
2. Run each of the 3 operations once: PDF, screenshot, e-invoice (e-invoice is
   the PDF action with the E-invoice fields filled in).
3. Capture one screenshot of each working. Three total, for the PR body.

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
