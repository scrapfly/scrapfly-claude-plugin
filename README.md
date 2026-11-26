# Scrapfly plugin for Claude Code

Answers from the web for Claude Code. This plugin connects Claude to [Scrapfly](https://scrapfly.io)
so it can read public web pages and answer from them, with every answer linked
to its source.

It adds:

- **Scrapfly's hosted MCP server** (`plugin/.mcp.json`), signed in with OAuth.
- **Task skills** that know how to answer a kind of question:

  | Skill | Answers |
  |---|---|
  | `prices-and-plans` | What a product or plan costs, compared across vendors |
  | `product-data` | Product details, specifications, availability and reviews |
  | `job-postings` | Open roles on a careers page or job board |
  | `property-listings` | Homes and rentals with price, size and location |
  | `news-coverage` | Article summaries and how outlets covered a story |
  | `read-docs` | Current documentation, changelogs and release notes |
  | `seo-audit` | On-page SEO findings with fixes |
  | `page-screenshots` | How a page looks, on desktop, mobile or in dark mode |
  | `scrapfly` | The tools, costs and rules every task shares |
  | `mcp-server` | The connection, credits, usage metrics and alerts |

- **Commands**:

  | Command | Does |
  |---|---|
  | `/scrapfly:setup` | Checks the sign-in and the account's credits |
  | `/scrapfly:scrape <url> [what to get]` | Reads a page, returns its content or the details asked for |
  | `/scrapfly:screenshot <url> [fullpage, viewport or selector] [mobile] [dark]` | Captures a page or an element |
  | `/scrapfly:extract <url> [what to extract or model]` | Returns structured data as JSON |

## Install

In Claude Code:

```text
/plugin marketplace add scrapfly/scrapfly-claude-plugin
/plugin install scrapfly@scrapfly
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

## Examples

```text
Compare the pricing plans of three email marketing tools.
What backend roles is this company hiring for, and which are remote?
Summarize how these three sites covered the same announcement.
Audit the SEO of https://web-scraping.dev/products and show it on a phone.
/scrapfly:extract https://web-scraping.dev/product/1 product
```

## Costs

Every call is billed in API credits of your plan: reading a static page costs 1
credit, JavaScript rendering 5 more, an extraction 5, and a screenshot 60.
Claude reports what each call cost and asks before work expected to cost more
than 100 credits. See [pricing](https://scrapfly.io/pricing).

## Data and terms

The URLs of each request go to Scrapfly at `mcp.scrapfly.io`, and the content
of the pages comes back into your Claude Code session.

Structured extraction (`extraction_model`, `extraction_prompt`, `/scrapfly:extract`)
is written by Scrapfly's own AI model, run by Scrapfly on the page it read, not
by Claude. Claude passes your request to that model and returns its result. Claude treats page
content as data, not as instructions. Use of Scrapfly is subject to its
[terms of service](https://scrapfly.io/terms-of-service) and
[privacy policy](https://scrapfly.io/privacy-policy).

## Development

```bash
claude plugin validate plugin --strict --profile directory
claude --plugin-dir plugin
```

## License

MIT, see [LICENSE](LICENSE).
