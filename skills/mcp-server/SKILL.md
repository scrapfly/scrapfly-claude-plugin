---
name: mcp-server
description: Scrapfly's hosted MCP server as this plugin connects it - authentication with SCRAPFLY_API_KEY or OAuth, the tool groups (scraping, screenshots, Cloud Browser, page interaction, WebMCP, credential vaults, monitoring, alerts, documentation search, account), what calls cost, permission rules, and how to fix a connection that fails. Use for "is Scrapfly connected", "how many credits do I have left", "which Scrapfly tools exist", "set up an alert on my success rate", or an MCP connection error.
user-invocable: false
---

# Scrapfly MCP server

The plugin connects Claude Code to `https://mcp.scrapfly.io/mcp` (streamable
HTTP), listed as `plugin:scrapfly:scrapfly` in `/mcp`. Its tools appear as
`mcp__plugin_scrapfly_scrapfly__<tool>`. Documentation:
https://scrapfly.io/docs/mcp/getting-started

## Authentication

The plugin sends `SCRAPFLY_API_KEY` from the environment as
`Authorization: Bearer <key>`. The key is on the dashboard:
https://scrapfly.io/dashboard/project. Claude Code reads the variable when it
starts, so a key set afterwards needs a restart.

The hosted server also accepts an OAuth sign-in in the browser, with no key in
the environment. Claude Code does not fall back to OAuth for a server that sends
an `Authorization` header, so for OAuth add the server on its own and disable
the plugin's in `/mcp`:

```bash
claude mcp add --transport http scrapfly-oauth https://mcp.scrapfly.io/mcp
```

then run `/mcp`, select it and sign in. https://scrapfly.io/docs/mcp/authentication

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
| Credential vaults | `cloud_browser_vault_*`: logins the browser fills in |
| Monitoring | `monitoring_get_metrics`, `monitoring_get_target_metrics`: success rate, errors and cost per product, project or website |
| Alerts | `alert_metric_families`, `alert_preview`, `alert_create`, `alert_list`, `alert_get`, `alert_update`, `alert_delete`, `alert_series`, `alert_test`, `alert_snooze`, `alert_unsnooze`, `alert_count_active` |
| Documentation | `docs_search`: Scrapfly's documentation, by product |

The product skills say when to use each: `scrapfly:web-scraping-api`,
`scrapfly:screenshot-api`, `scrapfly:extraction-api`, `scrapfly:cloud-browser`.
The Crawler API and the extraction of a document already at hand have no tool:
`scrapfly:crawler-api` and `scrapfly:extraction-api` call the HTTP API.

## Alerts: preview before you create

Ground a threshold in the account's own numbers:
`monitoring_get_metrics` (and `monitoring_get_target_metrics` for one website)
for the baseline, `alert_metric_families` for a valid `metric_id`,
`alert_preview` to count how often the rule would have fired, then
`alert_create` without `confirm` to show the dry run, and with `confirm: true`
once the user agrees. Leave `project_uuid` empty: the key's project is used.

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
| `Failed to connect`, HTTP 401 | `SCRAPFLY_API_KEY` is not set in Claude Code's environment, or the key is wrong | `export SCRAPFLY_API_KEY=...` in the shell that starts Claude Code, then restart it; `/scrapfly:setup` checks it |
| `network unauthorized`, `Access restricted by your project` | The key's project only accepts some IP addresses | Allow the address the message names in the project settings (Security & Access), or clear the list |
| Tools missing | The server is disabled in `/mcp`, or the plugin is | Enable it in `/mcp`, `/plugin` |

The server is open source, and can also run on your own machine:
https://github.com/scrapfly/scrapfly-mcp
