---
description: Set up or check the Scrapfly connection - whether the MCP server is signed in, the plan and the credits left. Use for "connect Scrapfly", "is Scrapfly working", "how many credits do I have". Never asks for a key or a password.
---

# Scrapfly setup

Check the connection to Scrapfly. Never ask for an API key, a password or a
token.

1. Call `info_account`. When it answers, the connection works: report the plan,
   the credits used and left, and the concurrency limit.
2. When it asks for authentication or no Scrapfly tool answers, tell the user to
   run `/mcp`, select `plugin:scrapfly:scrapfly` and sign in to Scrapfly in the
   browser (an account is free at https://scrapfly.io/register), then run
   `/scrapfly:setup` again. For any other error, follow the
   `scrapfly:mcp-server` skill's section "When the connection fails" and say
   which case applies.
3. List what the plugin adds: `/scrapfly:scrape`, `/scrapfly:screenshot`,
   `/scrapfly:extract`, and plain requests ("scrape
   https://web-scraping.dev/products", "screenshot this page") that the skills
   route to the right Scrapfly product.
