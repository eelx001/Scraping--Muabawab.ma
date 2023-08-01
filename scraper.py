import sys
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import concurrent.futures


def typing(text, delay=0.01):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\n")
    
typing("Choose an operation:")
typing("1. Tous")
typing("1. Apartments")
typing("2. locaux Commerciaux")
typing("3. Maison")
typing("4. Terrains")
typing("5. Villas")
typing("6. Bureaux")
CATEGORIE = input("Entrer votre choix : ")
if CATEGORIE == 1:
    CATEGORIE = "apartments-for-sale"
if CATEGORIE == 2:
    CATEGORIE = "commercial-property-for-sale"
if CATEGORIE == 3:
    CATEGORIE = "houses-for-sale"
if CATEGORIE == 4:
    CATEGORIE = "land-for-sale"
if CATEGORIE == 5:
    CATEGORIE = "villas-and-luxury-homes-for-sale"
if CATEGORIE == 6:
    CATEGORIE = "offices-for-sale"
if CATEGORIE == 0:
    CATEGORIE = ""
else:
    ('wrong choice')

BASE_URL = "https://www.mubawab.ma/"
SEARCH_KEYWORD = input("entrer le prix: ")
SEARCH_RESULT_FILE = "Mubawab.ma.txt"
WAIT_TIME_BETWEEN_REQUESTS = 1


RESULTS_TABLE_CLASS = "promotionListing listingBox w100"
PRICE_TAG_CLASS = "priceTag"
LOCATION_TAG_CLASS = "listingH3"
NO_RESULTS_MESSAGE_CLASS = "red"

def fetch_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to fetch results from {url}.")
        return None

def parse_results(html):
    if html is None:
        return set()

    soup = BeautifulSoup(html, 'html.parser')
    no_results_message = soup.find("h3", class_=NO_RESULTS_MESSAGE_CLASS)
    if no_results_message and "Désolé! Aucun résultat ne" in no_results_message.text:
        return set()

    results = soup.find_all("li", class_=RESULTS_TABLE_CLASS)

    parsed_results = set()
    for result in results:
        price = result.find("span", class_=PRICE_TAG_CLASS).text.strip()
        location = result.find("h3", class_=LOCATION_TAG_CLASS).text.strip()
        linkref = result.get("linkref")

        parsed_results.add((price, location, linkref))

    return parsed_results

def update_search_query(base_url, keyword, page_number,CATEGORIE):
    search_query = f"/fr/listing-promotion:prmx:{keyword}:scat:{CATEGORIE}:p:{page_number}"
    return urljoin(base_url, search_query)

def search_website(keyword):
    page_number = 1

    with open(SEARCH_RESULT_FILE, "w", encoding="utf-8") as file:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            while True:
                url = update_search_query(BASE_URL, keyword, page_number,CATEGORIE)
                html = fetch_page(url)
                if html is None:
                    print(f"Page {page_number} not found. Stopping the script.")
                    break
                results = parse_results(html)
                if not results:
                    print(f"No results found on page {page_number}. Stopping the script.")
                    break
                os.system('cls')
                print('La Recherche est en cours....')
                for price, location, linkref in results:
                    
                    data = f"Prix: {price}\nLocation: {location}\nLink: {linkref}\n---------------\n"
                    file.write(data)
                page_number += 1
                time.sleep(WAIT_TIME_BETWEEN_REQUESTS)
                

if __name__ == "__main__":
    search_website(SEARCH_KEYWORD)
