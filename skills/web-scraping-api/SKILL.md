---
name: web-scraping-api
description: Load first for any request to scrape, fetch or read the content of a URL ("scrape this page", "get this page", "fetch the JSON at", "read this site in markdown"), before calling web_get_page or web_scrape. Covers Scrapfly's Web Scraping API: which tool and settings cost least, JavaScript rendering, proxy pool and country, the Unblocker, headers, cookies, POST bodies, browser scenarios, cache, output formats and error codes.
user-invocable: false
---

# Web Scraping API

One request fetches one URL through Scrapfly's proxies, in a real browser when
asked, and returns the content with its status code and cost. Documentation:
https://scrapfly.io/docs/scrape-api/getting-started

## Pick the tool

- **`web_get_page`**: JavaScript rendering and the Unblocker always on, markdown
  by default. Takes `url`, `country`, `format`, `format_options`, `proxy_pool`,
  `rendering_wait`, `capture_page`, `capture_flags`, `extraction_model`. The
  shortest way to read a page, at 6 credits or more.
- **`web_scrape`**: every option of the API below. `render_js` and `unblocker`
  are on unless set to `false`.
- **HTTP API** (`GET https://api.scrapfly.io/scrape`): what the MCP tools do not
  take, such as `session`, `cost_budget`, `tags`, `correlation_id`, `os` or
  `auto_scroll`, or when the MCP server is not connected:

```bash
curl -G https://api.scrapfly.io/scrape \
  --data-urlencode "key=$SCRAPFLY_API_KEY" \
  --data-urlencode 'url=https://web-scraping.dev/products' \
  --data-urlencode 'format=markdown'
```

The JSON answer holds the content in `result.content`, the website's status in
`result.status_code`, the configuration in `config` and the cost in `context`.

## Spend the fewest credits

1. A static page or a JSON endpoint: `web_scrape` with `render_js: false` and
   `unblocker: false` costs 1 credit through a datacenter proxy.
2. Content built by JavaScript: `render_js: true` adds 5 credits.
3. A page that needs residential proxies and a real browser to load: keep the
   Unblocker on. It has no flat fee, but it can move the request to a
   residential proxy and a browser, which raises the cost; `cost_budget` (HTTP
   API) caps what one scrape may cost.
4. `proxy_pool: public_residential_pool` costs 25 credits instead of 1: use it for
   a page that needs residential proxies.
5. `cache: true` serves a repeat within `cache_ttl` seconds (86400 by default)
   for 1 credit.

`api_cost` and `cost_details` in the tool result give the cost of the call.

## Main parameters

| Parameter | What it does |
|---|---|
| `url` | The page to fetch, `http://` or `https://` |
| `format` | `markdown`, `text`, `clean_html`, `json` or `raw`; options `no_links`, `no_images`, `only_content` for markdown and text |
| `render_js` | Load the page in a browser (+5 credits): on by default on `web_scrape`, off on the HTTP API; set it to `false` for a static page |
| `rendering_wait` | Milliseconds to wait after the page loads (1000 by default with a browser) |
| `wait_for_selector` | A CSS or XPath selector to wait for, 15 seconds at most |
| `js` | JavaScript to run in the page before the content is read |
| `js_scenario` | Browser steps: `click`, `fill`, `scroll`, `wait`, `wait_for_selector`, `wait_for_navigation`, `execute`; needs `render_js` |
| `unblocker` | The Unblocker, for pages that need residential proxies and a real browser; its former name `asp` still works |
| `proxy_pool` | `public_datacenter_pool` (default) or `public_residential_pool` |
| `country` | Proxy country, ISO 3166-1 alpha-2 (`us`, `de`); the HTTP API also takes lists (`us,ca`) and exclusions (`-gb`) |
| `lang` | Page languages, sent as `Accept-Language` |
| `method`, `body`, `headers`, `cookies` | The request itself: `GET` by default, `POST`, `PUT`, `PATCH`, `OPTIONS`, `HEAD` |
| `cache`, `cache_ttl`, `cache_clear` | Serve and refresh from Scrapfly's cache |
| `retry`, `timeout` | Retries on transient errors (on by default). A custom `timeout` (milliseconds, 150000 at most) needs `retry: false` and, on `web_scrape`, `unblocker: false`: with the Unblocker on, or a retry, the API sets the timeout itself and drops yours |
| `extraction_prompt`, `extraction_model` | Structured data from the page: see `scrapfly:extraction-api`. They turn the Unblocker on whatever `unblocker` says |
| `screenshots`, `screenshot_flags` | Images taken during the scrape, billed with the scrape |
| `session` (HTTP API) | Keeps cookies and the proxy between scrapes of a multi-step flow |
| `tags`, `correlation_id` (HTTP API) | Labels to find the scrapes in the monitoring dashboard |

With `render_js`, only the `Cookie` and `Referer` headers are sure to reach the
website. The Unblocker may change the proxy pool, the country, the browser and
some headers to load the page: `context.proxy.country` tells which country served
it.

## Errors

The error comes with a code (`ERR::...`), a `retryable` flag and a documentation
page at `https://scrapfly.io/docs/scrape-api/error/<code>`.

| Code | Meaning | What to do |
|---|---|---|
| `ERR::SCRAPE::BAD_UPSTREAM_RESPONSE` | The website answered with a status of 400 or more | A 404 or 410 is the website's own answer. Otherwise check the URL, the method, the headers and the cookies, then read the code's page; a 403, 429 or 5xx is not billed while the account has Scrape Failed Protection |
| `ERR::ASP::SHIELD_PROTECTION_FAILED` | The Unblocker did not get the page this time | Check the URL and retry later; contact support with the scrape's log if it persists |
| `ERR::SCRAPE::OPERATION_TIMEOUT` | An operation took too long (504, retryable) | Retry; lighten the scenario or the wait; with `unblocker: false`, raise `timeout` with `retry: false` |
| `ERR::SCRAPE::DOM_SELECTOR_NOT_FOUND` | `wait_for_selector` did not appear within 15 seconds (billed) | Check the selector against the rendered content returned |
| `ERR::SCRAPE::CONFIG_ERROR` | A parameter is invalid (400) | Read the message, fix the parameter |
| `ERR::SCRAPE::DNS_NAME_NOT_RESOLVED` | The domain does not resolve | Check the URL |
| `ERR::SCRAPE::COST_BUDGET_LIMIT` | `cost_budget` is lower than what the target needs (not billed when refused before the request) | Raise the budget |
| `ERR::SCRAPE::TOO_MANY_CONCURRENT_REQUEST`, `ERR::THROTTLE::MAX_CONCURRENT_REQUEST_EXCEEDED` | The account's or the project's concurrency is used up (429, retryable) | Run fewer requests at once |
| `ERR::SCRAPE::QUOTA_LIMIT_REACHED` | The plan's monthly credits are used up (429) | Upgrade the plan or wait for the next period |
| `ERR::SCRAPE::PROJECT_QUOTA_LIMIT_REACHED` | The project's own credit limit is reached (429) | Raise the limit in the project settings |
| HTTP 401 | The key is invalid, or the project only accepts some IP addresses | Check the key; the message names the address to allow |

Full list: https://scrapfly.io/docs/scrape-api/errors

## SDKs and CLI

The Python SDK (`pip install scrapfly-sdk`, `ScrapeConfig`), the TypeScript, Go
and Rust SDKs and the `scrapfly scrape` command take the same parameters. Their
skills: https://github.com/scrapfly/skills
