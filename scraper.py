import requests
from bs4 import BeautifulSoup
import json

def main():
    print("--- Web Scraper Started ---")
    
    # Target URL (Using quotes sandbox site for reliable practice)
    url = "http://quotes.toscrape.com/"
    
    # Basic headers to avoid getting blocked
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    print(f"Fetching data from: {url}")
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() # Check for HTTP errors
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch page: {e}")
        return

    # Parse page content with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    quotes_data = []

    # Extracting elements based on HTML structure
    items = soup.find_all("div", class_="quote")
    
    for item in items:
        quote_text = item.find("span", class_="text").get_text(strip=True)
        author_name = item.find("small", class_="author").get_text(strip=True)
        
        # Extracting multiple tags for each quote
        tag_elements = item.find_all("a", class_="tag")
        tags_list = [tag.get_text(strip=True) for tag in tag_elements]
        
        # Storing into dictionary
        quotes_data.append({
            "quote": quote_text,
            "author": author_name,
            "tags": tags_list
        })

    # Saving the extracted data into a clean JSON file
    output_file = "headlines_and_quotes.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(quotes_data, f, indent=4, ensure_ascii=False)

    print(f"Success! {len(quotes_data)} records saved to {output_file}")

if __name__ == "__main__":
    main()
