# PolyDoc

[PolyDoc](https://polydoc.tech) turns HTML or a URL into pixel-perfect PDFs and
screenshots, and generates EU-compliant hybrid e-invoices (ZUGFeRD / Factur-X).
Conversions render in a real browser engine, so what you see in the page is what
you get in the document.

## Publisher

PolyDoc

## Prerequisites

You need a PolyDoc account and an API key. The free tier is enough to evaluate
the connector. No Power Automate premium license is required to use a custom
connector (unlike the generic HTTP action).

## Obtaining credentials

1. Sign in at [dashboard.polydoc.tech](https://dashboard.polydoc.tech).
2. Open **API Keys** and create a key.
3. When you create the connection, paste the key into **PolyDoc API key**. Paste
   only the key; the connector adds the `Bearer ` prefix for you.

## Supported operations

| Operation | What it does |
| --- | --- |
| **Convert to PDF** | Render HTML, a URL, or a saved template into a PDF. Controls for page format, margins, scale, headers/footers, bookmarks, accessible (tagged) PDFs, metadata, encryption, watermarks, and PDF/A. |
| **Capture screenshot** | Capture a PNG, JPEG, or WebP of HTML, a URL, or a template. Full-page or clipped, with viewport and device-pixel-ratio control. |

**E-invoices** are produced with **Convert to PDF**: fill in the **E-invoice**
fields (standard, profile, and the structured `invoice` object) and PolyDoc
embeds a ZUGFeRD / Factur-X invoice in the returned PDF. See the
`example-flows/` folder in the connector repository for a ready-to-use body.

### Source

Every operation takes a single **Source** that is one of:

- a URL, e.g. `https://example.com`
- an inline HTML string
- a saved template reference, `[template:TEMPLATE_ID]`, optionally with
  **Template data** for the Liquid renderer

### Delivery

By default the file is returned as binary content, ready to drop into
**Create file** (OneDrive, SharePoint, Blob) or an email attachment. Two
alternative delivery modes are available under advanced options:

- **Cloud storage**: provide a presigned PUT URL; PolyDoc uploads the file and
  the action returns JSON containing the stored URL.
- **Webhook**: PolyDoc delivers the file to your webhook and the action returns
  a JSON acknowledgement (HTTP 202 when async).

When either delivery mode is used the response is JSON rather than a binary
file.

### Sandbox mode

Each operation has an advanced **Sandbox mode** input. Set it to `true` to
generate watermarked output from a separate quota with a lower rate limit, which
is useful while building and testing a flow. Leave it `false` for production
documents.

## Known issues and limitations

- The response of each action is declared as a binary file. When **Cloud
  storage** or **Webhook** delivery is configured, the action returns JSON
  instead of a file.
- Pages that load JavaScript from an external CDN can slow the converter
  significantly. For inline HTML, prefer self-contained markup (inline CSS,
  data-URI images).
- E-invoices follow EN 16931. At minimum provide a due date or payment terms
  (rule BR-CO-25), the seller tax ID when a line uses VAT category `S`, and
  consistent totals (net + tax = gross). With **Verify** enabled an invoice that
  fails validation returns an error.

## Deployment instructions

This connector is defined as a standard Power Platform custom connector
(`apiDefinition.swagger.json` + `apiProperties.json` + `icon.png`). Deploy it
with the Power Platform Connectors CLI:

```bash
# one-time login
paconn login

# validate the definition
paconn validate --api-def apiDefinition.swagger.json

# create the connector in the selected environment
paconn create --api-def apiDefinition.swagger.json \
  --api-prop apiProperties.json --icon icon.png --secret <none>
```

You can also import `apiDefinition.swagger.json` directly from the Power Automate
maker portal (**Data > Custom connectors > New custom connector > Import an
OpenAPI file**).
