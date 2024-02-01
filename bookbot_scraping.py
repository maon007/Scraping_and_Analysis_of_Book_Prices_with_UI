import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

class AbeBooksScraper:
    def __init__(self):
        """Initialize the AbeBooksScraper object."""
        self.base_url = "https://www.abebooks.de/servlet/SearchResults?prevpage={}&bi=0&bsi={}&sortby=1&vci=87044093&ds=50"
        self.target_count = 1000
        self.max_pages = 30
        self.titles = []
        self.isbns = []
        self.provider = []
        self.prices = []
        self.countries = []
        self.scanned_pages = []
        self.start_time = time.time()

    def handle_rate_limiting(self, url):
        """Handle rate limiting with exponential backoff.

        Args:
            url (str): The URL to send the GET request to.

        Returns:
            requests.Response: The response object from the GET request.
        """
        retry_attempts = 0
        while retry_attempts < 12:  # Set a maximum number of retry attempts
            try:
                response = requests.get(url)
                response.raise_for_status()  # Raise an exception for HTTP errors
                return response
            except requests.exceptions.RequestException as e:
                if response.status_code == 429:  # Check if it's a rate limit error
                    retry_attempts += 1
                    print(f"Rate limit exceeded. Retrying in {2**retry_attempts} seconds...")
                    time.sleep(2**retry_attempts)  # Exponential backoff
                else:
                    print("Error fetching URL:", e)
                    break

    def scrape(self):
        """Scrape data from AbeBooks website."""
        page_number = 0
        item_counter = 0

        while True:
            if page_number >= self.max_pages:
                break
            
            url = self.base_url.format(page_number, item_counter)
            print("Scanning URL:", url)

            response = self.handle_rate_limiting(url)

            soup = BeautifulSoup(response.text, 'html.parser')
            listing_items = soup.find_all('li', {'data-cy': 'listing-item'})

            for item in listing_items:
                listing_links = item.find_all('a', id=lambda x: x and 'listing' in x)
                for link in listing_links:
                    link_url = link['href']
                    full_link = "https://www.abebooks.de" + link_url

                    try:
                        response = self.handle_rate_limiting(full_link)
                        link_soup = BeautifulSoup(response.text, 'html.parser')
                    except requests.exceptions.RequestException as e:
                        print("Error fetching link:", e)
                        continue

                    snippet = link_soup.find('hr', id='hr1')
                    if snippet:
                        more_buying_options_div = snippet.find_next_sibling('div', {'id': 'more-buying-options'})
                        if more_buying_options_div:
                            more_buying_options_link = more_buying_options_div.find('a', id='view-all-listings')
                            if more_buying_options_link:
                                full_buying_options_link = "https://www.abebooks.de" + more_buying_options_link['href']
                                try:
                                    response = self.handle_rate_limiting(full_buying_options_link)
                                    soup = BeautifulSoup(response.text, 'html.parser')
                                except requests.exceptions.RequestException as e:
                                    print("Error fetching buying options link:", e)
                                    continue

                                listing_items = soup.find_all('li', {'data-cy': 'listing-item'})
                                for item in listing_items:
                                    price_meta = item.find('meta', {'itemprop': 'price'})
                                    if price_meta:
                                        price = price_meta['content']

                                    seller_link = item.find('a', {'data-cy': 'listing-seller-link'})
                                    if seller_link:
                                        provider_name = seller_link.text.strip()
                                        next_sibling_text = seller_link.find_next_sibling(text=True).strip()
                                        country = next_sibling_text.split(',')[-1].strip()

                                        isbn_meta = item.find('meta', {'itemprop': 'isbn'})
                                        if isbn_meta and isbn_meta['content']:
                                            isbn = isbn_meta['content']
                                            title = item.find('span', {'data-cy': 'listing-title'}).text.strip()

                                            self.titles.append(title)
                                            self.isbns.append(isbn)
                                            self.provider.append(provider_name)
                                            self.countries.append(country)
                                            self.prices.append(price)
                                            self.scanned_pages.append(page_number)

                                            print("Item:", isbn, ",",title, ",",country, ",",provider_name, ",",price, ",",page_number)
                                            print("-" * 50)

                                            if len(set(self.isbns)) == self.target_count:
                                                break
                                if len(set(self.isbns)) == self.target_count:
                                    break
                        if len(set(self.isbns)) == self.target_count:
                            break
                if len(set(self.isbns)) == self.target_count:
                    break

            if len(set(self.isbns)) == self.target_count:
                break

            page_number += 1
            item_counter += 50

            if not listing_items:
                break

    def save_to_csv(self, filename):
        """Save scraped data to a CSV file.

        Args:
            filename (str): The filename to save the CSV file as.
        """
        unique_isbns = list(set(self.isbns))[:self.target_count]
        df = pd.DataFrame({'ISBN13': self.isbns, 'Title': self.titles, 'Provider': self.provider, 'Country': self.countries,
                           'Price': self.prices, 'Scanned_Page': self.scanned_pages})
        df = df[df['ISBN13'].isin(unique_isbns)]
        df.to_csv(filename, index=False)

    def display_summary(self):
        """Display summary information after scraping."""
        end_time = time.time()
        running_time = end_time - self.start_time
        print("Total running time:", running_time, "seconds")
        print(df.head(20))
        print(df.shape)

def main():
    scraper = AbeBooksScraper()
    scraper.scrape()
    scraper.save_to_csv("1000_all_providers_with_limit.csv")
    scraper.display_summary()

if __name__ == "__main__":
    main()
