# online-bookshop-market-analysis

## Overview

This project is designed to scrape data from an online bookstore using the [Scrapy](https://scrapy.org/) framework. The goal is to collect and analyze information on available books, including details such as the title, author, price, availability, and ratings. The scraped data can be used for further analysis, such as price comparisons, rating trends, or even building a recommendation system.

## Features

- **Book Information Scraping**: Extracts key details like title, author, price, and availability from the bookstore website.
- **Rating and Review Collection**: Gathers user ratings and review counts to help analyze customer preferences.
- **Export in Various Formats**: Supports exporting scraped data into CSV, JSON, and other structured formats for further analysis.
- **Polite Scraping**: Implements delays and adheres to the website’s `robots.txt` to ensure scraping does not overload the server.
- **Database storage**: Snowflake has been used for this project but it is possible to adapt the pipelines.py file to store data in mysql database a more open source option.
