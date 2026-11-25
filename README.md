# Scrapfly plugin for Claude Code

Web data for Claude Code. This plugin connects Claude to [Scrapfly](https://scrapfly.io)
and teaches it every Scrapfly product: scrape a page as markdown, capture a
screenshot, extract structured data with AI, and drive a cloud browser.

It adds:

- **Scrapfly's hosted MCP server** (`plugin/.mcp.json`): scraping, screenshots, Cloud
  Browser sessions and page interaction, WebMCP, monitoring, alerts,
  documentation search and account tools.
- **Six skills** that pick the right product for a task and know its
  parameters, costs and errors:

  | Skill | Covers |
  |---|---|
  | `scrapfly` | Picks the product and the tool, shared rules, costs at a glance |
  | `web-scraping-api` | The content of a URL: rendering, proxies, country, the Unblocker, headers, cookies, scenarios, cache |
  | `screenshot-api` | Images of a page or an element |
  | `extraction-api` | Structured data with an LLM prompt or an AI model |
  | `cloud-browser` | A remote browser driven through MCP tools |
  | `mcp-server` | The connection, its tools, the account, alerts |

- **Commands** for the common jobs:

  | Command | Does |
  |---|---|
  | `/scrapfly:setup` | Checks the sign-in, the MCP connection and the account's credits |
  | `/scrapfly:scrape <url> [what to get]` | Fetches a page, returns its content or the details asked for |
  | `/scrapfly:screenshot <url> [fullpage, viewport or selector] [mobile] [dark]` | Captures a page or an element |
  | `/scrapfly:extract <url> [what to extract or model]` | Extracts structured data as JSON |

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

## Sign in

1. Create an account at [scrapfly.io/register](https://scrapfly.io/register)
   (the Free plan comes with 1,000 API credits).
2. Run `/mcp`, select `plugin:scrapfly:scrapfly` and sign in to Scrapfly in the
   browser. The first Scrapfly tool call also starts the sign-in.
3. Run `/scrapfly:setup` to check the connection and your credits.

The plugin uses OAuth only: no API key is stored in the plugin, your
environment or your files.

## Products

| Product | What for | Documentation |
|---|---|---|
| Web Scraping API | The content of any URL, rendered in a browser when needed, through datacenter or residential proxies in the country you pick, with the Unblocker for pages that need it | [docs](https://scrapfly.io/docs/scrape-api/getting-started) |
| Screenshot API | Full-page, window or element captures, at any resolution | [docs](https://scrapfly.io/docs/screenshot-api/getting-started) |
| Extraction API | JSON from a page: LLM prompts and AI models (product, article, review list, job posting and more) | [docs](https://scrapfly.io/docs/extraction-api/getting-started) |
| Cloud Browser | A remote Chrome driven by Claude through MCP tools | [docs](https://scrapfly.io/docs/cloud-browser-api/getting-started) |
| MCP server | The tools above for any MCP client | [docs](https://scrapfly.io/docs/mcp/getting-started) |

## Examples

```text
/scrapfly:scrape https://web-scraping.dev/products list the product names and prices
/scrapfly:screenshot https://web-scraping.dev/product/1 mobile
/scrapfly:extract https://web-scraping.dev/product/1 product
```

```text
Open https://web-scraping.dev/products in a Scrapfly cloud browser, go to the second page and list its products.
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
needs. Besides the MCP server at `mcp.scrapfly.io`, code examples in the
product skills call Scrapfly's HTTP API at `api.scrapfly.io` and its Cloud
Browser at `browser.scrapfly.io`; those calls use your own API key and go only
to Scrapfly. Claude treats fetched content as data, not as instructions. Use of
Scrapfly is subject to its [terms of service](https://scrapfly.io/terms-of-service)
and [privacy policy](https://scrapfly.io/privacy-policy).

## Skill synchronization

The four product skills (`web-scraping-api`, `screenshot-api`, `extraction-api`
and `cloud-browser`) are generated from
[`scrapfly/skills`](https://github.com/scrapfly/skills), their golden source.
The `scrapfly` and `mcp-server` skills, commands, plugin configuration and the
small Claude-specific rules in `scripts/skill-overrides/` are maintained here.
The hourly sync workflow also runs after a change to its script and can be
started manually with **Run workflow**. It validates the plugin and publishes
only when a product skill changed.

To run the sync and its tests locally:

```bash
python3 -m unittest discover -s scripts/tests -t scripts/tests
python3 scripts/sync-skills.py --skills /path/to/scrapfly-skills --out plugin

# Report drift without changing the plugin
python3 scripts/sync-skills.py --skills /path/to/scrapfly-skills --out plugin --check
```

## Development

```bash
claude plugin validate plugin --strict --profile directory
claude --plugin-dir plugin
```

## Links

- [Scrapfly documentation](https://scrapfly.io/docs)
- [Scrapfly MCP server](https://github.com/scrapfly/scrapfly-mcp)
- [Scrapfly CLI](https://github.com/scrapfly/scrapfly-cli)
- [Skills for the SDKs and the CLI](https://github.com/scrapfly/skills)
- [Support](https://scrapfly.io/docs/support)

## License

MIT, see [LICENSE](LICENSE).
