"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Ngoc Khanh Vy Tranová
email: ngtranova@gmail.com
discord: veelilly 
"""

import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import sys

"""
# Najdeme odkazy na všechny kraje

def get_region_links(link):
    response = get(link) # Získání zdrojového kódu
    divided_html = BeautifulSoup(response.text, "html.parser") # Rozdělení zdrojového kódu
    region_links = []

    h3_tags = divided_html.find_all("h3", class_="kraj")
    for h3 in h3_tags:
        a_tag = h3.find("a", href=True)
        if a_tag:
            region_links.append("https://www.volby.cz/pls/ps2017nss/" + a_tag['href'])
    
    print(f"Nalezeno {len(region_links)} odkazů na kraje.")

    return region_links

link = "https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ"
region_links = get_region_links(link)
print(f"Nalezeno {len(region_links)} odkazů na kraje.")
for region_link in region_links:
    print(region_link)
"""

# Najdeme všechny odkazy na obce pomoxí X ve sloupci Výběr okrsku

def get_municipality_links(region_link):
    response = requests.get(region_link)
    divided_html = BeautifulSoup(response.text, "html.parser")
    municipality_links = []

    td_tags = divided_html.find("td", {"class": "center", "headers": "t1sa2"})
    for td_tag in td_tags:
        a_tag= td_tag.find("a", href=True)
        if a_tag:
            municipality_links.append("https://www.volby.cz/pls/ps2017nss/" + a_tag['href'])
    
    print(f"Nalezeno {len(municipality_links)} obcí v kraji {region_link}:")
    return municipality_links

# Získáme výsledky voleb pro každou obec

def get_data(municipality_link):
    response = get(municipality_link)
    divided_html = BeautifulSoup(response.text, "html.parser")

    # extrakce základních informací
    code_element = divided_html.row.find('td', {'headers': 't1sa1 t1sb1'})
    location_element = divided_html.find('td', {'headers': 't1sa1 t1sb2'})
    registered_element = divided_html.find('td', {'headers': 'sa2'})
    envelopes_element = divided_html.find('td', {'headers': 'sa3'})
    valid_votes_element = divided_html.find('td', {'headers': 'sa6'})

    code = code_element.text.strip() if code_element else "N/A"
    location = location_element.text.strip() if location_element else "N/A"
    registered = registered_element.text.replace('\xa0', '').strip() if registered_element else "N/A"
    envelopes = envelopes_element.text.replace('\xa0', '').strip() if envelopes_element else "N/A"
    valid_votes = valid_votes_element.text.replace('\xa0', '').strip() if valid_votes_element else "N/A"
    
    # extrakce hlasů pro jednotlivé strany
    candidate_parties = [party.text.strip() for party in divided_html.find_all('td', {'headers': 't1sa1 t1sb2 t1sc2'})]
    votes = [vote.text.replace('\xa0', '').strip() for vote in divided_html.find_all('td', {'headers': 't1sa2 t1sb3 t1sc3'})]

    data = {
        "kód obce": code,
        "název obce": location,
        "voliči v seznamu": registered,
        "vydané obálky": envelopes,
        "platné hlasy": valid_votes,  
    } 
    
    for party, vote in zip(candidate_parties, votes):
        data[party] = vote
    
    print(f"Získána data pro obec: {location}")
    return data

# Hlavní funkce
def main(region_link, output):
    "region_links = get_region_links(region_link)"
    all_data = []

    "for region_link in region_links:"
    municipality_links = get_municipality_links(region_link)
    for municipality_link in municipality_links:
        municipality_data = get_data(municipality_link)
        if municipality_data is not None:
            all_data.append(municipality_data)

    df = pd.DataFrame(all_data)
    print(df.head())
    df.to_csv(output, index=False, encoding='utf-8')
    print(f" Data uložena do souboru: {output}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Použití: python projekt_3.py <URL> <vystupni_soubor>")
        sys.exit(1)

    region_link = sys.argv[1]
    output = sys.argv[2]

    if not region_link.startswith("https://www.volby.cz/pls/ps2017nss"):
        print("Nesprávný odkaz na územní celek.")
        sys.exit(1)

main(region_link, output)