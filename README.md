# Homeware site scraper
#### A scraper written using the `Scrapy` framework to extract data from a homeware site
Data is outputted as an Excel (CSV) file - see `ecommerce/example.csv` for output format 

<br />
To run scraper locally:

``` pip install -r requirements.txt ```

``` cd ecommerce ```

``` scrapy crawl homeware -O Homeware.csv```