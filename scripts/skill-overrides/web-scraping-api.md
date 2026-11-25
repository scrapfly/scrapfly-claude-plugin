## Claude Code rules

Pick the MCP tool before scraping: `web_get_page` for a straightforward read,
`web_scrape` for rendering, proxy pools, countries, headers, cookies, scenarios,
cache and extraction. Keep `render_js: false` for a static page and use the
Unblocker only when the target needs it. Prefer the cheaper stateless scrape to
a Cloud Browser session.

The result includes `api_cost` and `cost_details`. Report them, and report
errors with their `ERR::...` code, `retryable` flag and documentation link.
