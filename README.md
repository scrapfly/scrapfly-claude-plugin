# Scrapfly plugin for Claude Code

Web data for Claude Code. This plugin connects Claude to [Scrapfly](https://scrapfly.io)
and teaches it every Scrapfly product: scrape a page as markdown, capture a
screenshot, extract structured data with AI, crawl a website, and drive a cloud
browser with Playwright, Puppeteer, Browser Use or Stagehand.

It adds:

- **Scrapfly's hosted MCP server** (`.mcp.json`): scraping, screenshots, Cloud
  Browser sessions and page interaction, WebMCP, monitoring, alerts,
  documentation search and account tools.
- **Seven skills** that pick the right product for a task and know its
  parameters, costs and errors:

  | Skill | Covers |
  |---|---|
  | `scrapfly` | Picks the product and the tool, shared rules, costs at a glance |
  | `web-scraping-api` | The content of a URL: rendering, proxies, country, the Unblocker, headers, cookies, scenarios, cache |
  | `screenshot-api` | Images of a page or an element |
  | `extraction-api` | Structured data with an LLM prompt, an AI model or a template |
  | `crawler-api` | Many pages of a site, their content and artifacts |
  | `cloud-browser` | A remote browser, through MCP tools or CDP from your own code |
  | `mcp-server` | The connection, its tools, the account, alerts |

- **Commands** for the common jobs:

  | Command | Does |
  |---|---|
  | `/scrapfly:setup` | Checks the API key, the MCP connection and the account's credits |
  | `/scrapfly:scrape <url> [what to get]` | Fetches a page, returns its content or the details asked for |
  | `/scrapfly:screenshot <url> [fullpage, viewport or selector] [mobile] [dark]` | Captures a page or an element |
  | `/scrapfly:extract <url or file> [what to extract or model]` | Extracts structured data as JSON |
  | `/scrapfly:crawl <url> [pages] [what to collect]` | Crawls a site and returns its pages or what was asked |

Plain requests work too: the skills choose the product and the tool.

## Install

In Claude Code:

```text
/plugin marketplace add scrapfly/scrapfly-claude-plugin
/plugin install scrapfly@scrapfly
```

Or from a shell:

```bash
claude plugin marketplace add scrapfly/scrapfly-claude-plugin
claude plugin install scrapfly@scrapfly
```

Then run `/reload-plugins` or start a new session.

## Set your API key

1. Create an account at [scrapfly.io/register](https://scrapfly.io/register)
   (the Free plan comes with 1,000 API credits) and copy your API key from the
   [dashboard](https://scrapfly.io/dashboard/project).
2. Export it in the shell that starts Claude Code, and add the line to your
   shell profile (`~/.zshrc`, `~/.bashrc`) to keep it:

   ```bash
   export SCRAPFLY_API_KEY="your-api-key"
   ```

3. Restart Claude Code and run `/scrapfly:setup`. Until the key is set, `/mcp`
   shows the plugin's server as failed.

The MCP server receives the key as an `Authorization: Bearer` header, and the
crawl and document extraction calls pass it to the Scrapfly API from the
environment. The plugin never writes the key to a file.

Prefer signing in with OAuth and keeping no key in your environment? The hosted
MCP server supports it: add it with
`claude mcp add --transport http scrapfly-oauth https://mcp.scrapfly.io/mcp`,
sign in from `/mcp`, and disable the plugin's own server there. Crawls and
document extraction still use `SCRAPFLY_API_KEY`.

## Products

| Product | What for | Documentation |
|---|---|---|
| Web Scraping API | The content of any URL, rendered in a browser when needed, through datacenter or residential proxies in the country you pick, with the Unblocker for pages that need it | [docs](https://scrapfly.io/docs/scrape-api/getting-started) |
| Screenshot API | Full-page, window or element captures, at any resolution | [docs](https://scrapfly.io/docs/screenshot-api/getting-started) |
| Extraction API | JSON from a page or a document: LLM prompts, AI models (product, article, review list, job posting and more), templates | [docs](https://scrapfly.io/docs/extraction-api/getting-started) |
| Crawler API | Whole sections of a site, as markdown, HTML, extracted data or a WARC archive | [docs](https://scrapfly.io/docs/crawler-api/getting-started) |
| Cloud Browser | A remote Chrome over CDP for Playwright, Puppeteer, Browser Use and Stagehand, or driven by Claude through MCP tools | [docs](https://scrapfly.io/docs/cloud-browser-api/getting-started) |
| MCP server | The tools above for any MCP client | [docs](https://scrapfly.io/docs/mcp/getting-started) |

## Examples

```text
/scrapfly:scrape https://web-scraping.dev/products list the product names and prices
/scrapfly:screenshot https://web-scraping.dev/product/1 mobile
/scrapfly:extract https://web-scraping.dev/product/1 product
/scrapfly:crawl https://web-scraping.dev/products 10 collect each product's name and price
```

```text
Open https://web-scraping.dev/products in a Scrapfly cloud browser, go to the second page and list its products.
Write a Playwright script that connects to Scrapfly's Cloud Browser and prints the titles on https://web-scraping.dev/products.
Get the request headers httpbin.dev sees from a Scrapfly scrape through a German proxy.
How many Scrapfly credits do I have left?
```

## Costs

Every call is billed in API credits of your plan: a scrape through a datacenter
proxy costs 1 credit, JavaScript rendering 5 more, a residential proxy 25, a
screenshot 60, an extraction 1 to 5, and a Cloud Browser session its time and
bandwidth. The skills give Claude the full table, Claude reports what each call
cost, and it asks before work expected to cost more than 100 credits. See
[pricing](https://scrapfly.io/pricing) and the
[billing documentation](https://scrapfly.io/docs/scrape-api/billing).

## Data and terms

The URLs and options of each request go to Scrapfly, and the content Scrapfly
fetches comes back into your Claude Code session: include only what the task
needs. Claude treats fetched content as data, not as instructions. Use of
Scrapfly is subject to its [terms of service](https://scrapfly.io/terms-of-service)
and [privacy policy](https://scrapfly.io/privacy-policy).

## Development

```bash
claude plugin validate .
claude --plugin-dir .
scripts/run-evals.sh
```

The evals run Claude on the plugin with stubbed tools, so they need a Claude
credential and no Scrapfly key. They cost a few cents.

## Links

- [Scrapfly documentation](https://scrapfly.io/docs)
- [Scrapfly MCP server](https://github.com/scrapfly/scrapfly-mcp)
- [Scrapfly CLI](https://github.com/scrapfly/scrapfly-cli)
- [Skills for the SDKs and the CLI](https://github.com/scrapfly/skills)
- [Support](https://scrapfly.io/docs/support)

## License

MIT, see [LICENSE](LICENSE).
