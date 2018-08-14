# Indeed web crawler
Scrapy crawler for www.indeed.com . Extracts The company name, job
title, company link on indeed.com

## Usage
This will crawl all full-time "data engineer" positions in the USA
posted within the last day

```
$ scrapy crawl indeed -a job="data engineer" -a loc="USA" -a
jobtype="fulltime" -a age=1

```
