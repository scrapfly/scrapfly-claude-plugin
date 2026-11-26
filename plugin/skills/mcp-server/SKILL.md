---
name: mcp-server
description: Scrapfly's hosted MCP server as this plugin connects it - OAuth sign-in, the account's credits, usage metrics and alerts, and how to fix a connection that fails. Use for "is Scrapfly connected", "how many credits do I have left", "how many calls failed this week", "set up an alert on my usage", or an MCP connection error.
user-invocable: false
---

# Scrapfly MCP server

The plugin connects Claude Code to `https://mcp.scrapfly.io/mcp` (streamable HTTP), listed as `plugin:scrapfly:scrapfly` in `/mcp`. Documentation: https://scrapfly.io/docs/mcp/getting-started

## Sign-in

The server uses OAuth: the first tool call, or selecting the server in `/mcp`, opens the browser to sign in to Scrapfly and pick a project. No API key is stored in the plugin or the environment. Never ask the user for a key, a password or a token.

## Account tools

| Need | Tools |
|---|---|
| Plan, credits used and left | `info_account` |
| Success rate, errors and cost per product or website | `monitoring_get_metrics`, `monitoring_get_target_metrics` |
| Alerts on those metrics | `alert_metric_families`, `alert_preview`, `alert_create`, `alert_list`, `alert_get`, `alert_update`, `alert_delete`, `alert_snooze`, `alert_unsnooze` |
| Scrapfly's documentation | `docs_search` |

The task skills say which tools read pages.

## Alerts: preview before you create

Get the baseline with `monitoring_get_metrics`, a valid `metric_id` from `alert_metric_families`, count how often the rule would have fired with `alert_preview`, then call `alert_create` without `confirm` to show the dry run, and with `confirm: true` once the user agrees. Leave `project_uuid` empty: the signed-in project is used.

## When the connection fails

| `/mcp` or `claude mcp list` shows | Cause | Fix |
|---|---|---|
| `Needs authentication`, HTTP 401 | Not signed in, or the sign-in expired | Select the server in `/mcp` and sign in again |
| `network unauthorized`, `Access restricted by your project` | The project only accepts some IP addresses | Allow the address the message names in the project settings, or clear the list |
| Tools missing | The server or the plugin is disabled | Enable it in `/mcp` or `/plugin` |
