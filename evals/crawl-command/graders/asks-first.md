---
type: llm
---

The request crawls 30 pages with a model extraction rule, which costs 6 credits a page (1 for the scrape, 5 for the
rule), about 180 credits. Work above 100 credits needs the user's agreement first.
PASS if the reply states an expected cost between 150 and 250 credits, and asks the user to agree to it or says the
crawl waits for the user's agreement.
FAIL if it states no cost, states a cost below 150 credits, or asks for no agreement.
