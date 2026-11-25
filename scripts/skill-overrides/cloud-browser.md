## Claude Code rules

For an interactive page, use the Cloud Browser MCP tools, not a local browser.
`cloud_browser_open` returns a live session and a snapshot with element `uid`
values. Read that snapshot before choosing `click`, `fill`, `type_text`,
`press_key`, `select_option` or another page tool, then call them with those
`uid` values. After anything that changes the page, call `take_snapshot` again
and use the new `uid` values instead of stale ones. Close the session when the
task is done.

Use `cloud_browser_navigate` to move the same session, `cloud_browser_screenshot`
or `cloud_browser_eval` to inspect it, and `cloud_browser_close` to release it.
For Playwright, Puppeteer, Browser Use or Stagehand, connect over CDP instead of
calling the MCP page tools.

Never put a credential in a prompt or a tool call. Create and fill credential
vaults from the dashboard; do not ask for a password, token or vault key in the
conversation.
