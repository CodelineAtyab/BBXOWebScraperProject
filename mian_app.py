import json
import requests
from parsel import Selector
from typing import List, Dict, Any

def scrape_dubizzle_properties(url: str):
    """
    Scrape property listings from dubizzle.com.om
    
    Args:
        url: The URL to scrape
    
    Returns:
        List of dictionaries containing property information
    """
    properties = []
    
    print(f"Scraping: {url}")
    
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch page. Status code: {response.status_code}")
        return properties
    
    selector = Selector(text=response.text)
    # Find all property listings
    property_listings = selector.css('li article._63a946ba')
    
    for listing in property_listings:
        try:
            # Extract price
            price = listing.css('div._948d9e0a._8d76513c span.ddc1b288::text').get('')
            
            # Extract title
            title = listing.css('h2._562a2db2::text').get('')
            
            # Extract description
            description = listing.css('div.dd57f32f span._8206696c::text').get('')
            
            # Extract bedrooms
            bedrooms = listing.css('span._18b01e88[aria-label="Beds"] span._3e1113f0::text').get('')
            
            # Extract bathrooms
            bathrooms = listing.css('span._18b01e88[aria-label="Bathrooms"] span._3e1113f0::text').get('')
            
            # Extract area
            area = listing.css('span._18b01e88[aria-label="Area"] span._3e1113f0::text').get('')
            
            # Extract location
            location = listing.css('span.f7d5e47e[aria-label="Location"]::text').get('')
            
            # Extract date posted
            date_posted = listing.css('span.c72cec28 span[aria-label="Creation date"]::text').get('')
            
            # Extract seller/agency name
            seller_name = listing.css('div._948d9e0a.e814c74d span._8206696c::text').get('')
            
            # Extract property URL
            property_url_element = listing.css('a::attr(href)').get('')
            property_url = f"https://www.dubizzle.com.om{property_url_element}" if property_url_element else ''
            
            # Extract image URL
            image_url = listing.css('picture._5a8a8551 img::attr(src)').get('')
            
            property_data = {
                'price': price,
                'title': title,
                'description': description,
                'bedrooms': bedrooms,
                'bathrooms': bathrooms,
                'area': area,
                'location': location,
                'date_posted': date_posted,
                'seller_name': seller_name,
                'property_url': property_url,
                'image_url': image_url
            }

            # Make a request to bring the contact number

            properties.append(property_data)
            print(f"Scraped: {title}")
            
        except Exception as e:
            print(f"Error extracting property data: {e}")
    
    return properties

def save_to_json(data: List[Dict[str, Any]], filename: str) -> None:
    """
    Save data to a JSON file
    
    Args:
        data: The data to save
        filename: The name of the file to save to
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print(f"Data saved to {filename}")

def main():
    url = "https://www.dubizzle.com.om/en/properties/properties-for-rent/"
    
    properties = scrape_dubizzle_properties(url)
    
    if properties:
        print(f"Scraped {len(properties)} properties")
        save_to_json(properties, "./dubizzle_properties.json")
    else:
        print("No properties found")

if __name__ == "__main__":
    main()
