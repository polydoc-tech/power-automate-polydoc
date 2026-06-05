# Example flows

Each JSON file here is the **action body** for one PolyDoc use case. They mirror
the three angles shipped for the n8n connector (PDF, screenshot, e-invoice) and
double as the request payloads used to smoke-test the connector.

| File | Operation | Use case |
| --- | --- | --- |
| `1-pdf-from-html.json` | Convert to PDF | A self-contained HTML report rendered to an A4 PDF. |
| `2-screenshot-of-url.json` | Capture screenshot | A full-page PNG of a public URL. |
| `3-einvoice-zugferd.json` | Convert to PDF (E-invoice) | A ZUGFeRD / EN 16931 hybrid invoice with `verify` enabled. |

## Using one in a flow

1. Add the **PolyDoc** connector action (**Convert to PDF** or **Capture
   screenshot**) to your flow.
2. Map the fields from the matching JSON file. For the PDF and screenshot bodies
   the **Source** is the main input; the e-invoice body additionally fills the
   **E-invoice** section.
3. Pass the action output (binary file content) to a downstream step, for
   example **Create file** (OneDrive / SharePoint / Blob) or an email
   attachment.

## Testing a body directly

The same bodies work against the API with `curl`. Use sandbox mode while
testing:

```bash
curl -sS -D - -o out.pdf \
  -H "Authorization: Bearer $POLYDOC_API_KEY" \
  -H "Content-Type: application/json" \
  -H "X-Sandbox: true" \
  --data @1-pdf-from-html.json \
  https://api.polydoc.tech/pdf/convert

curl -sS -D - -o out.png \
  -H "Authorization: Bearer $POLYDOC_API_KEY" \
  -H "Content-Type: application/json" \
  -H "X-Sandbox: true" \
  --data @2-screenshot-of-url.json \
  https://api.polydoc.tech/screenshot/convert

curl -sS -D - -o invoice.pdf \
  -H "Authorization: Bearer $POLYDOC_API_KEY" \
  -H "Content-Type: application/json" \
  -H "X-Sandbox: true" \
  --data @3-einvoice-zugferd.json \
  https://api.polydoc.tech/pdf/convert
```

Sandbox output is watermarked and the sandbox rate limit is low (about 5
requests per second), so space the calls out.
