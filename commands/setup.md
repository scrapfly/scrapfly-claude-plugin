---
description: Check that Scrapfly is connected - the API key in the environment, the MCP server, and the account's credits
disable-model-invocation: true
---

# Scrapfly setup

Check the connection to Scrapfly, step by step, without ever printing the key.

1. Run `test -n "$SCRAPFLY_API_KEY" && echo "SCRAPFLY_API_KEY is set" || echo "SCRAPFLY_API_KEY is not set"`.
   If it is not set, tell the user to get a key at
   https://scrapfly.io/dashboard/project, add `export SCRAPFLY_API_KEY=<their key>`
   to the profile of the shell that starts Claude Code, restart Claude Code and
   run `/scrapfly:setup` again. Stop there. Never ask for the key in the
   conversation.
2. Call the `info_account` tool of the Scrapfly MCP server. If the tool is
   missing or the call fails, follow the `scrapfly:mcp-server` skill, section
   "When the connection fails", and say which case applies.
3. Report the plan, the credits used and left, and the concurrency limit.
4. List what the plugin adds: `/scrapfly:scrape`, `/scrapfly:screenshot`,
   `/scrapfly:extract`, `/scrapfly:crawl`, and plain requests ("scrape
   https://web-scraping.dev/products", "screenshot this page") that the skills
   route to the right Scrapfly product.
