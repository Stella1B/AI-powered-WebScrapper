import requests
from bs4 import BeautifulSoup, Tag
import csv
from textblob import TextBlob

def scrape_all_quotes(base_url):
    url = base_url
    all_quotes = []
    while url:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to retrieve page: {url}")
            break
        soup = BeautifulSoup(response.text, 'html.parser')
        quotes = soup.find_all('div', class_='quote')
        for quote in quotes:
            text = quote.find('span', class_='text').get_text()
            author = quote.find('small', class_='author').get_text()
            tags = [tag.get_text() for tag in quote.find_all('a', class_='tag')]
            # Sentiment analysis
            sentiment = TextBlob(text).sentiment.polarity
            all_quotes.append({
                'text': text,
                'author': author,
                'tags': ', '.join(tags),
                'sentiment': sentiment
            })
        # Find next page
        next_btn = soup.find('li', class_='next')
        if next_btn:
            next_link = next_btn.find('a')
            if next_link and isinstance(next_link, Tag) and next_link.get('href'):
                next_url = next_link.get('href')
                url = base_url.rstrip('/') + '/' + next_url
            else:
                url = None
        else:
            url = None
    return all_quotes

def save_quotes_to_csv(quotes, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['text', 'author', 'tags', 'sentiment']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for quote in quotes:
            writer.writerow(quote)

if __name__ == "__main__":
    url = input("Enter the URL to scrape: ")
    quotes = scrape_all_quotes(url)
    print(f"Scraped {len(quotes)} quotes.")
    save_quotes_to_csv(quotes, 'quotes.csv')
    print("Quotes saved to quotes.csv.")
