# How to Scrape Hospitality and Restaurant Job Boards (L'Hôtellerie Restauration, HOGAPAGE, Gastrojobs, Hosco)

> **Run it now, no code: [hospitality-jobs-scraper on the Apify Store](https://apify.com/bibian/hospitality-jobs-scraper)** &nbsp;|&nbsp; $3.70 per 1,000 job postings &nbsp;|&nbsp; no browser, no proxy, no login

Hospitality and restaurant jobs are scattered across sector-specific boards with no shared format and no public export: [L'Hôtellerie Restauration](https://www.lhotellerie-restauration.fr) (France), [HOGAPAGE](https://www.hogapage.de) (Germany), [Gastrojobs](https://www.gastrojobs.de) (Germany) and [Hosco](https://www.hosco.com) (worldwide). This guide shows how to pull postings from all four in a single run, mapped to one unified schema, with a free Apify Actor, from the console or from code.

Searches this page answers: hospitality jobs scraper, restaurant jobs scraper, hotel jobs scraper, L'Hôtellerie Restauration scraper, HOGAPAGE scraper, Gastrojobs scraper, Hosco scraper, no login job scraper.

## What you get

- Every job posting from L'Hôtellerie Restauration, HOGAPAGE, Gastrojobs and Hosco, in one unified schema: title, company, location, remote policy, employment type, salary range and dates.
- Deduplicated across sources and across runs (`onlyNew`), with country, source host and native id kept on every row.
- Optional full description as plain text. No personal data (recruiter contact details) is ever exported.

Export the dataset as JSON, CSV or Excel, or read it through the Apify API. A real sample (five results, already public, no personal data) is in [`sample-output.json`](sample-output.json).

## Output fields

| Field | Type | Meaning |
|---|---|---|
| `id` | string | Stable identifier (`<source>:<native id>`), used to deduplicate between runs. |
| `url` | string | Public page of the posting. |
| `title` | string | Job title as published. |
| `companyName` | string or null | Employer name; `null` when hidden (then `confidentialCompany: true`). |
| `companyUrl` | string or null | Company page on the source site, when it exists. |
| `locationLabel`, `city`, `region`, `postalCode` | string or null | Location as displayed by the site. |
| `country` | string | ISO 3166-1 alpha-2 country code (`FR`, `DE`, or the employer's own country for Hosco's worldwide postings). |
| `remote` | string | `remote`, `hybrid`, `onsite` or `unknown`. |
| `employmentType` | string | `full_time`, `part_time`, `contract`, `freelance`, `internship`, `apprenticeship`, `temporary` or `unknown`. |
| `salaryMin` / `salaryMax` | number or null | Salary range, as numbers. |
| `salaryCurrency` | string or null | ISO 4217 currency code. |
| `salaryPeriod` | string or null | `hour`, `day`, `month` or `year`. |
| `datePosted` / `validThrough` | string or null | Publication and expiry dates, ISO 8601. |
| `description` | string or null | Plain-text description, only when `includeDescriptions` is on. No personal data. |
| `experienceLevel`, `industry` | string or null | As named by the site. |
| `skills` | string[] | Skills listed by the site, if any. |
| `source`, `sourceId`, `scrapedAt` | string | Host name of the source site, its native id, extraction timestamp. |

### Example (real result, trimmed)

```json
{
  "id": "lhotellerie-restauration.fr:153W9288",
  "url": "https://www.lhotellerie-restauration.fr/emploi/c46fedcf/le-malabar-restaurant-de-cuisine-traditi/3627bbb5",
  "title": "Chef de partie H/F CDI",
  "companyName": "MALABAR",
  "city": "PARIS 07",
  "region": "75",
  "country": "FR",
  "remote": "onsite",
  "employmentType": "full_time",
  "datePosted": "2026-11-08T19:52:11.0870000+01:00",
  "source": "lhotellerie-restauration.fr"
}
```

## Use cases

- **Watch 4 sector boards from one place.** No need to check L'Hôtellerie Restauration, HOGAPAGE, Gastrojobs and Hosco separately: one schema, one schedule.
- **Build a daily alert for a role or a region.** Schedule a run every morning with `publishedWithinDays: 1` and `onlyNew: true`, then send only the new postings to Slack, e-mail or a spreadsheet.
- **Track hiring in hospitality and restaurants** across France, Germany and worldwide. Group postings by `country`, `employmentType` or `industry` to see where establishments are recruiting right now.
- **Feed a niche job board or newsletter** for hotel and restaurant professionals with structured, deduplicated data and the canonical `url` back to the original posting.

## Input

| Field | What it does |
|---|---|
| `keywords` | Job title or trade, for example `chef de cuisine` or `Koch`. Empty means every posting. |
| `location` | City or region, for example `Paris` or `Berlin`. Empty means all locations. |
| `countries` | Which countries to cover: `FR`, `DE`, `GLOBAL` (Hosco, regardless of the other countries chosen). Defaults to all 3. |
| `sources` | Which of the 4 job boards to query in this run. Defaults to all 4. |
| `publishedWithinDays` | Keep only postings published in the last N days. Use `1` for a daily monitoring run. |
| `remote` | Keep only postings with this remote policy: `any`, `remote`, `hybrid` or `onsite`. |
| `maxItems` | The run stops once this many postings are saved, across all sources combined (default 20 — Hosco's robots.txt imposes a 10-second delay between requests, which caps how many of its postings fit in one run). |
| `includeDescriptions` | Add the job description as plain text (default on). |
| `onlyNew` | For scheduled runs: skip postings an earlier run of this same search already delivered. |

Example input:

```json
{
  "keywords": "chef de cuisine",
  "location": "",
  "countries": ["FR", "DE", "GLOBAL"],
  "sources": ["lhotellerie", "hogapage", "gastrojobs", "hosco"],
  "publishedWithinDays": 7,
  "remote": "any",
  "maxItems": 20,
  "includeDescriptions": false,
  "onlyNew": false
}
```

## Four ways to use it

### 1. Apify console, no code

1. Open [the Actor page](https://apify.com/bibian/hospitality-jobs-scraper) and click **Try for free** (a free Apify account is enough).
2. Fill in the input form (keywords, countries and the maximum number of results) and click **Start**.
3. When the run finishes, open the **Output** tab, check the table, then **Export** as CSV, Excel or JSON.
4. For a daily alert, open **Schedules**, create a daily schedule for the Actor, turn `onlyNew` on, and optionally add an integration that sends new results to Slack, e-mail or Google Sheets.

### 2. Apify API with JavaScript

```bash
npm install apify-client
export APIFY_TOKEN="your token from Apify console, Settings, Integrations"
node examples/run.js
```

```js
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

const run = await client.actor('bibian/hospitality-jobs-scraper').call({
    "keywords": "chef de cuisine",
    "countries": ["FR", "DE", "GLOBAL"],
    "publishedWithinDays": 7,
    "maxItems": 20,
    "includeDescriptions": false
});

const { items } = await client.dataset(run.defaultDatasetId).listItems();
for (const item of items) {
    console.log(`${item.title} | ${item.companyName} | ${item.locationLabel} | ${item.source}`);
}
```

The complete file is [`examples/run.js`](examples/run.js) (ES module, Node 18 or later).

### 3. Apify API with Python

```bash
pip install apify-client
export APIFY_TOKEN="your token from Apify console, Settings, Integrations"
python examples/run.py
```

```python
import os
from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])

run = client.actor("bibian/hospitality-jobs-scraper").call(run_input={
    "keywords": "chef de cuisine",
    "countries": ["FR", "DE", "GLOBAL"],
    "publishedWithinDays": 7,
    "maxItems": 20,
    "includeDescriptions": False,
})

for item in client.dataset(run.default_dataset_id).iterate_items():
    print(f"{item['title']} | {item.get('companyName')} | {item.get('locationLabel')} | {item.get('source')}")
```

The complete file is [`examples/run.py`](examples/run.py). Never put your token in the code: read it from the `APIFY_TOKEN` environment variable as above.

### 4. Schedule it for a daily alert

Create an Apify Schedule for the Actor, set `publishedWithinDays` to `1` and `onlyNew` to `true`, and attach an integration (Slack, e-mail, Google Sheets, Make, Zapier or a webhook) so only the new postings reach you, every day.

## Pricing

Pay per result: **$3.70 per 1,000 job postings** (that is $0.0037 per posting), plus a small start fee per run. You pay only for the postings saved to the dataset, deduplicated across all 4 sources before being counted or charged. Apify's free plan includes monthly credits, enough to try it on a few hundred results. Prices are those shown on the [Store page](https://apify.com/bibian/hospitality-jobs-scraper) when this guide was written; the Store page is the reference.

## Limits and honest notes

- Hosco is throttled on purpose: its robots.txt sets a 10-second delay between requests, which this Actor respects, so it contributes fewer postings per run than the other 3 boards.
- `employmentType` and `remote` are read from each site's own fields when it has one, and left `unknown` rather than guessed when nothing matches.
- No personal data: contact details of individuals are stripped from descriptions; only companies are named. CV and candidate-profile pages are never read.
- Postings are the public ones: anything behind a login is out of scope.
- This is an unofficial tool, not affiliated with L'Hôtellerie Restauration, HOGAPAGE, Gastrojobs or Hosco. Check each site's terms and the data protection rules that apply to your use.

## FAQ

**Does it need a browser or a proxy?**
No. All 4 sources are read directly over HTTP, so runs are fast and cheap.

**How do I only get new postings every day?**
Set `publishedWithinDays` to `1`, turn `onlyNew` on, and schedule the Actor once a day. Each source is deduplicated against what a previous run already delivered.

**Why does Hosco return so few results compared to the other boards?**
Hosco's own robots.txt sets a 10-second delay between requests; this Actor respects it, which limits how many of its postings fit in a single run's time budget.

**Can I query just one source, like only Gastrojobs?**
Yes, set `sources` to `["gastrojobs"]` and `countries` to `["DE"]`.

**Can I get the data in Excel or Google Sheets?**
Yes. Export the dataset as CSV, Excel or JSON from the Apify console, or connect the Apify Google Sheets integration.

## Try it

**[Open hospitality-jobs-scraper on the Apify Store](https://apify.com/bibian/hospitality-jobs-scraper)**

The code in `examples/` is released under the MIT license (see [LICENSE](LICENSE)). The data belongs to its original publishers.
