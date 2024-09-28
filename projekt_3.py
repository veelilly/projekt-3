"""
projekt_2.py: třetí projekt do Engeto Online Python Akademie

author: Ngoc Khanh Vy Tranová
email: ngtranova@gmail.com
discord: veelilly 
"""

import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd

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
    return region_links

"""
zkouška:
link = "https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ"
region_links = get_region_links(link)
print(f"Nalezeno {len(region_links)} odkazů na kraje.")
for region_link in region_links:
    print(region_link)
"""

# Najdeme všechny odkazy na obce pomoxí X ve sloupci Výběr okrsku

def get_municipality_links(region_link):
    response = get(region_link)
    divided_html = BeautifulSoup(response.text, "html.parser")
    municipality_links = []

    td_tags = divided_html.find_all("td", {"class": "cislo"})
    for td_tag in td_tags:
        a = td_tag.find("a", href=True)
        if a:
            municipality_links.append("https://www.volby.cz/pls/ps2017nss/" + a['href'])
    return municipality_links

"""
zkouška:
link = "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=5&xnumnuts=4101"  
municipality_links = get_municipality_links(link)
print(f"Nalezeno {len(municipality_links)} odkazů na obce:")
for municipality_link in municipality_links:
    print(municipality_link) 
"""

# Získáme výsledky voleb pro každou obec

def get_data(municipality_link):
    response = get(municipality_link)
    divided_html = BeautifulSoup(response.text, "html.parser")

    # extrakce základních informací
    code = divided_html.find('td', {'headers': 't1sa1 t1sb1'}).text.strip()
    location = divided_html.find('td', {'headers': 't1sa1 t1sb2'}).text.strip()
    registered = divided_html.find('td', {'headers': 'sa2'}).text.replace('\xa0','').strip()
    envelopes = divided_html.find('td', {'headers': 'sa3'}).text.replace('\xa0', '').strip()
    valid_votes = divided_html.find('td', {'headers': 'sa6'}).text.replace('\xa0', '').strip()
    
    # extrakce hlasů pro jednotlivé strany
    candidate_parties = [party.text.strip() for party in divided_html.find_all('td', {'headers': 't1sa1 t1sb2'})]
    votes = [vote.text.replace('\xa0', '').strip() for vote in divided_html.find_all('td', {'headers': 't1sa2 t1sb3'})]

    
    data = {
        "kód obce": code,
        "název obce": location,
        "voliči v seznamu": registered,
        "vydané obálky": envelopes,
        "platné hlasy": valid_votes,  
    } 
    
    for party, vote in zip(candidate_parties, votes):
        data[party] = vote
    
    return data

# Hlavní funkce
def main(region_link, output):
    region_links = get_region_links(region_link)
    all_data = []

    for region_link in region_links:
        municipality_links = get_municipality_links(region_link)
        for municipality_link in municipality_links:
            municipality_data = get_data(municipality_link)
            all_data.append(municipality_data)

    df = pd.DataFrame(all_data)
    print(df.head())
    df.to_csv(output, index=False)
    print(f" Data uložena do souboru: {output}")

if __name__ == "__main__":
    region_link = "https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ"
    output = "vysledky_voleb.csv"
    main(region_link, output)
