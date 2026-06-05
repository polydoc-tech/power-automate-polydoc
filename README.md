# power-automate-polydoc

A Microsoft Power Platform **custom connector** for [PolyDoc](https://polydoc.tech):
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

> The policy-based auth is verified by schema (`paconn validate`). Its runtime
> behavior can only be confirmed by creating a real connection in a tenant,
> which is part of the live-import follow-up below. If certification surfaces a
> problem with the per-connection policy reference, the fallback is a plain
> `apiKey` security definition on the `Authorization` header where the user
> pastes `Bearer <key>`.

## Validate

```bash
# paconn from a throwaway venv
python3 -m venv .venv && . .venv/bin/activate && pip install paconn
paconn validate --api-def PolyDoc/apiDefinition.swagger.json
```

## Test the bodies

See `example-flows/README.md` for `curl` commands that exercise each body
against the live API in sandbox mode.

## Status and follow-ups

Done: connector definition, properties, icon, READMEs, and three example bodies,
validated and smoke-tested against the live API in sandbox.

Not done yet (tracked as follow-ups):

- Live import into a Power Automate environment, create a connection, run all
  three operations, and capture screenshots.
- Independent Publisher submission PR to `microsoft/PowerPlatformConnectors`
  (PR titled "PolyDoc (Independent Publisher)"; the README must include
  screenshots of three operations succeeding in flows).
- Create the GitHub repository under the `polydoc-tech` org and push.
