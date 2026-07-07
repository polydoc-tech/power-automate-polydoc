Thanks for the review. The connector package (`apiDefinition.swagger.json`, `apiProperties.json`, `readme.md`) is in place, and I've now tested every operation in a Power Platform environment. Screenshots below.

**1. ConvertToPdf** — `200`, `content-type: application/pdf` (body `%PDF-1.7`).

**2. CaptureScreenshot** — `200`, `content-type: image/png`.

**3. ConvertToPdf in e-invoice mode** (Factur-X / EN16931, `verify: true`) — `200`, `application/pdf` with the embedded e-invoice XML. E-invoice is a mode of `ConvertToPdf` (one PDF endpoint), not a separate operation, so this connector has two operations by design.

**4. Definition tab** — both operations (`ConvertToPdf`, `CaptureScreenshot`), verb `POST`, host `api.polydoc.tech`.

One question on process: could you point me to how the verified-credentials (One Vet) step is initiated? I haven't received the verification form at my GitHub-registered email yet, and I'd like to complete it so this can move forward. Thanks!
