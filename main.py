from urllib.parse import urlparse

import pandas as pd
import tldextract
import requests

BLOCKLIST_URLS = [
    "https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews-gambling-porn-social/hosts"
]

KEYWORDS  = [
    "porn", "sex", "xxx", "adult", "escort", "hanime",
    "casino", "bet", "poker", "gambling", "lotto", "game", "hot", "hentai",
    "game", "bingo", "slot"
]

def download_blocklist(url: str) -> set:
    print(f" Download of blocklist from {url} ...")
    r = requests.get(url)
    r.raise_for_status()
    domains = set()
    for line in r.text.splitlines():
        if line.startswith("#") or line.strip() == "":
            continue
        parts = line.split()
        if len(parts) >= 2:
            domains.add(parts[1].lower())
    print(f" {len(domains)} domains loaded in blocklist")
    return domains

def matches_keywords(domain):
    return any(word in domain for word in KEYWORDS)

def is_blocked(domain, blocklist):
    return domain in blocklist or matches_keywords(domain)

def get_limited_domain(url: str) -> str:
    ext = tldextract.extract(url)
    parts = ext.subdomain.split(".") if ext.subdomain else []

    if len(parts) >= 2:
        sub = ".".join(parts[-2:])
        return f"https://{sub}.{ext.domain}.{ext.suffix}".lower()
    elif len(parts) == 1:
        return f"https://{parts[0]}.{ext.domain}.{ext.suffix}".lower()
    elif ext.domain and ext.suffix:
        return f"https://{ext.domain}.{ext.suffix}".lower()
    return url.lower()

def main(input_csv: str, output_csv: str, blocklist: set):

    df = pd.read_csv(input_csv, names=["url", "popularity"])

    df = df[df["url"].str.startswith("https://")]
    df["domain"] = df["url"].apply(get_limited_domain)

    #filtered = df[~df["main_domain"].isin(blocklist)]
    filtered = df[~df["domain"].apply(lambda d: is_blocked(d, blocklist))]

    filtered = filtered.drop_duplicates(subset=["url"])
    filtered.to_csv(output_csv, index=False, columns=["url", "popularity"])
    print(f"File salvato in {output_csv}")
    print(f"Domini iniziali: {len(df)} → Domini finali: {len(filtered)}")

if __name__ == "__main__":
    blocklist = set()
    for url in BLOCKLIST_URLS:
        blocklist |= download_blocklist(url)
    main("crux-2023-12-top17m.csv", "completed-filter.csv", blocklist)