# Job Purpose

From the list of most visited domains on google extract domains that follow standard corporate policies. The list of the most visited domains can be found in the repo GitHub https://github.com/lkarlslund/topdomains, in a `csv` file .

Structure of the csv file:

| url, popularity |
| --- |
| [https://m.vk.com](https://m.vk.com/),1000
[https://m.yahoo.co.jp](https://m.yahoo.co.jp/),1000
[https://m.youtube.com](https://m.youtube.com/),1000 |

### Domain reduction

There are multiple domains in the CSV file that differ only in higher-level subdomains (e.g., xx or zz), but they all actually point to the same domain of interest. 

Example:

- `xx.yy.aa.google.com`
- `zz.yy.aa.google.com`

In these cases, the significant part we want to keep is from the second subdomain from (`yy.aa.google.com`). If the same "reduced" domain appears multiple times, only one occurrence should remain.

## How to go about filtering

### Method 1: List with banned words

A list of disallowed words is defined. For each domain, it is checked whether it contains at least one of the words in the list. If so, the domain is removed from the list. This automatically filters out domains that should not be considered for analysis.

```python
KEYWORDS  = [
    "porn", "sex", "xxx", "adult", "escort", "pornhub",
    "casino", "bet", "poker", "gambling", "lotto", "game", "hot",
    "game", "bingo", "slot"
]
```

| Advantages  | Disadvantages |
| --- | --- |
| If the domain contains one of these words, it is obviously a site that cannot be used on the work environment | Many “untrusted” domains do not explicitly contain words that refer to their content |
| This method is generic and allows domains to be identified quickly | Non si ha la certazza di rimuovere i domini non fidati |

### Method 2: Using a list of adult domains

Its possible to directly use public lists of domains already categorized as untrustworthy or undesirable (e.g., adult content, gambling, social media, etc.).

One example is the list maintained on GitHub by [StevenBlack/hosts](https://github.com/StevenBlack/hosts) or on the website https://firebog.net/, which provides an `hosts` file containing thousands of domains labeled as unsafe or unwanted.

Process

1. Download the list from a trusted source (e.g., the GitHub repository).
2. Extract domains from the list (they are usually written in the format `0.0.0.0 [domain.com](http://domain.com/)`).
3. Compare the domains in the CSV with the downloaded list:
    - If a CSV domain appears in the list → it is removed.
    - If it does not appear → is retained.
4. Continue processing only on the remaining domains.

| Advantages  | Disadvantages |
| --- | --- |
| The list contains a well-defined list of adult domains, which makes it possible to accurately identify all untrusted domains | The list is not exhaustive: there may be unwanted domains not included, so some may pass the filters. |
| The approach is more robust than simple keyword filtering because false positives are avoided. | You need to download the list periodically to keep it updated |
|  | It requires an extra step of management (downloading, parsing, automatic updating). |

### Method 3:  Whitelist

Instead of filtering out the bad ones, it starts with a list of domains considered safe and accepts only those.  Anything not on the whitelist is discarded.

| Advantages | Disadvantages |
| --- | --- |
| Maximum security. | Very restrictive. |
| No false negatives (unwanted domains do not pass). | It requires constant maintenance of the white list. |
|  |  |

### Method 4: Machine Learning

Train a model to recognize suspicious domains based on textual features (length, letter frequency, vowel/consonant pattern, presence of keywords).

| Advantages | Disadvantages |
| --- | --- |
| It can detect never-before-seen (zero-day) domains. | Requires training dataset. |
| Adaptable to multiple contexts. | More complex to implement than static blacklists. |

### Method 5: **Category-based Filtering**

Associate domains with subject categories (adult, gambling, social, news, etc.) using open source or commercial datasets. Then keep only certain categories (e.g., "business," "education") and exclude others.

| Advantages | Disadvantages |
| --- | --- |
| More granular filtering: not only adults, but also other undesirable contexts. | Requires categorized datasets or API services. |
| Useful for business scenarios. |  |
