"""Minimal example: run the hospitality-jobs-scraper Actor and print the results.

Usage: APIFY_TOKEN=... python run.py   (pip install apify-client)
"""
import os
import sys

from apify_client import ApifyClient

token = os.environ.get("APIFY_TOKEN")
if not token:
    sys.exit("Set the APIFY_TOKEN environment variable first.")

client = ApifyClient(token)

run_input = {
    "keywords": "chef de cuisine",
    "location": "",
    "countries": ["FR", "DE", "GLOBAL"],
    "sources": ["lhotellerie", "hogapage", "gastrojobs", "hosco"],
    "publishedWithinDays": 7,
    "remote": "any",
    "maxItems": 20,
    "includeDescriptions": False,
    "onlyNew": False,
}

run = client.actor("bibian/hospitality-jobs-scraper").call(run_input=run_input)

count = 0
for item in client.dataset(run.default_dataset_id).iterate_items():
    count += 1
    print(f"{item['title']} | {item.get('companyName')} | {item.get('locationLabel')} | {item.get('source')}")
print(f"{count} results")
