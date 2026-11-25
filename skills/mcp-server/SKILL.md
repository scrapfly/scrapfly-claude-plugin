---
name: mcp-server
description: Scrapfly's hosted MCP server as this plugin connects it - OAuth sign-in, the tool groups (scraping, screenshots, Cloud Browser, page interaction, WebMCP, credential vaults, monitoring, alerts, documentation search, account), what calls cost, permission rules, and how to fix a connection that fails. Use for "is Scrapfly connected", "how many credits do I have left", "which Scrapfly tools exist", "set up an alert on my success rate", or an MCP connection error.
user-invocable: false
---

# Scrapfly MCP server

The plugin connects Claude Code to `https://mcp.scrapfly.io/mcp` (streamable
HTTP), listed as `plugin:scrapfly:scrapfly` in `/mcp`. Its tools appear as
`mcp__plugin_scrapfly_scrapfly__<tool>`. Documentation:
https://scrapfly.io/docs/mcp/getting-started

## Sign-in

The server uses OAuth: the first tool call, or selecting the server in `/mcp`,
opens the browser to sign in to Scrapfly and pick a project. No API key is
stored in the plugin or the environment. Never ask the user for a key, a
password or a token. https://scrapfly.io/docs/mcp/authentication

## Tools

The connection lists the tools the account can use, and each tool's schema is
the authority for its parameters.

| Group | Tools |
|---|---|
| Scraping | `web_get_page`, `web_scrape`, `screenshot`, `scraping_instruction_enhanced` (a guide to the scraping options) |
| Account | `info_account`: plan, credits used and left, concurrency |
| Cloud Browser | `cloud_browser_open`, `browser_unblock`, `cloud_browser_navigate`, `cloud_browser_sessions`, `cloud_browser_close`, `cloud_browser_screenshot`, `cloud_browser_eval`, `cloud_browser_downloads`, `cloud_browser_performance` |
| Page interaction | `take_snapshot`, `take_screenshot`, `find_elements`, `get_page_url`, `evaluate_script`, `click`, `hover`, `drag`, `fill`, `type_text`, `press_key`, `select_option`, `dropdown_options`, `scroll`, `scroll_to_text`, `go_back`, `wait` |
| WebMCP | `list_webmcp_tools`, `call_webmcp_tool` |
| Credential vaults | `cloud_browser_vault_*`: manage credential vaults. A vault key, a password or a token passed to them stays in the conversation, so create and fill a vault from the dashboard |
| Monitoring | `monitoring_get_metrics`, `monitoring_get_target_metrics`: success rate, errors and cost per product, project or website |
| Alerts | `alert_metric_families`, `alert_preview`, `alert_create`, `alert_list`, `alert_get`, `alert_update`, `alert_delete`, `alert_series`, `alert_test`, `alert_snooze`, `alert_unsnooze`, `alert_count_active` |
| Documentation | `docs_search`: Scrapfly's documentation, by product |

The product skills say when to use each: `scrapfly:web-scraping-api`,
`scrapfly:screenshot-api`, `scrapfly:extraction-api`, `scrapfly:cloud-browser`.
The Crawler API and the extraction of a document already at hand have no tool:
link their documentation.

## Alerts: preview before you create

Ground a threshold in the account's own numbers:
`monitoring_get_metrics` (and `monitoring_get_target_metrics` for one website)
for the baseline, `alert_metric_families` for a valid `metric_id`,
`alert_preview` to count how often the rule would have fired, then
`alert_create` without `confirm` to show the dry run, and with `confirm: true`
once the user agrees. Leave `project_uuid` empty: the signed-in project is used.

## Cost

A tool call costs what the same API call costs (`scrapfly:scrapfly` has the
table), and each scraping result reports it in `api_cost` and `cost_details`.
A screenshot attached to a scrape (`screenshots` of `web_scrape`) is billed as
the scrape; one taken in a Cloud Browser session is part of the session's time.

## Permissions

Claude Code asks before each MCP tool call. To allow the read-only ones without
asking, add rules such as `mcp__plugin_scrapfly_scrapfly__web_get_page` or
`mcp__plugin_scrapfly_scrapfly__info_account` to `permissions.allow` in the
settings.

## When the connection fails

| `/mcp` or `claude mcp list` shows | Cause | Fix |
|---|---|---|
| `Needs authentication`, HTTP 401 | Not signed in, or the sign-in expired | Select the server in `/mcp` and sign in again |
| `network unauthorized`, `Access restricted by your project` | The project only accepts some IP addresses | Allow the address the message names in the project settings (Security & Access), or clear the list |
| Tools missing | The server is disabled in `/mcp`, or the plugin is | Enable it in `/mcp`, `/plugin` |

The server is open source, and can also run on your own machine:
https://github.com/scrapfly/scrapfly-mcp
