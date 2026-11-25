## Claude Code rules

When the data comes from a URL, call `web_scrape` with `extraction_prompt` or
`extraction_model`. Do not merely scrape the page: one of those parameters must
be present so the result is structured JSON. `extraction_template` is not an
MCP parameter; use a template through the Extraction API instead.

When the document is already at hand, POST it to
`https://api.scrapfly.io/extraction` with its type in the `Content-Type` header.
The prompt comes from a file, and the key comes from the environment:

```bash
curl -X POST "https://api.scrapfly.io/extraction?key=$SCRAPFLY_API_KEY" \
  --url-query 'extraction_model=product' \
  -H "Content-Type: text/html" --data-binary @product.html

curl -X POST "https://api.scrapfly.io/extraction?key=$SCRAPFLY_API_KEY" \
  --url-query 'extraction_prompt@prompt.txt' \
  -H "Content-Type: text/html" --data-binary @product.html
```

For a saved or inline template, use `extraction_template` on this HTTP endpoint,
not on `web_scrape`.
