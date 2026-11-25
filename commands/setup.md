---
description: Set up or check the Scrapfly API key and connection - whether SCRAPFLY_API_KEY is set, whether the MCP server answers, the plan and the credits left. Use for "set up my Scrapfly key", "connect Scrapfly", "is Scrapfly working". Never asks for the key in the conversation.
---

# Scrapfly setup

Check the connection to Scrapfly, step by step, without ever printing the key.
Never ask for the key in the conversation.

1. Run `test -n "$SCRAPFLY_API_KEY" && echo "SCRAPFLY_API_KEY is set" || echo "SCRAPFLY_API_KEY is not set"`.
   When the shell is not available, go to step 2.
2. Call `info_account` on a connected Scrapfly MCP server. When it answers, the
   connection works: report the plan, the credits used and left, and the
   concurrency limit. When the variable is not set, the connection is an OAuth
   sign-in: say so, and that only crawls and extraction of a file need
   `SCRAPFLY_API_KEY`.
3. When no Scrapfly tool answers: if the variable is not set, tell the user to
   get a key at https://scrapfly.io/dashboard/project, to add
   `export SCRAPFLY_API_KEY=<their key>` to the profile of the shell that starts
   Claude Code, to restart Claude Code and to run `/scrapfly:setup` again, or to
   sign in with OAuth as the `scrapfly:mcp-server` skill shows. If the variable
   is set, follow that skill's section "When the connection fails" and say which
   case applies.
4. List what the plugin adds: `/scrapfly:scrape`, `/scrapfly:screenshot`,
   `/scrapfly:extract`, `/scrapfly:crawl`, and plain requests ("scrape
   https://web-scraping.dev/products", "screenshot this page") that the skills
   route to the right Scrapfly product.
