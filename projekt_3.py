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


# Najdeme odkazy na všechny kraje

""" def get_region_links(link):
    response = get(link) # Získání zdrojového kódu
    divided_html = BeautifulSoup(response.text, "html.parser") # Rozdělení zdrojového kódu
    region_links = []

    h3_tags = divided_html.find_all("h3", class_="kraj")
    for h3 in h3_tags:
        a_tag = h3.find("a", href=True)
        if a_tag:
            region_links.append("https://www.volby.cz/pls/ps2017nss/" + a_tag['href'])
    
    print(f"Nalezeno {len(region_links)} odkazů na kraje.")

    return region_links """

# Najdeme všechny odkazy na okrsky pomocí čísla obce

def get_municipality_links(link):
    response = requests.get(link)
    divided_html = BeautifulSoup(response.text, "html.parser")
    municipality_data = []

    rows = divided_html.find_all("tr")[2:] # první dva řádky jsou hlavičky
    for row in rows:
        code_element = row.find("td", class_="cislo")
        name_element = row.find("td", class_="overflow_name")

        if code_element and name_element and code_element.a:
            code = code_element.text.strip()
            name = name_element.text.strip()
            municipality_link = "https://www.volby.cz/pls/ps2017nss/" + code_element.a["href"]
            municipality_data.append((code, name, municipality_link))

    print(f"Nalezeno {len(municipality_data)} obcí:")
    return municipality_data

# Získáme výsledky voleb pro každou obec
def get_data(code, name, link):
    response = requests.get(link)
    divided_html = BeautifulSoup(response.text, "html.parser")

    # Extrakce základních informací
    """ 
    code_element = divided_html.find("td", class_="cislo")
    code = code_element.text.strip() if code_element else "N/A"

    name_element = divided_html.find("td", class_="overflow_name")
    name = name_element.text.strip() if name_element else "N/A" 
    """ 

    registered_element = divided_html.find("td", {"class": "cislo", "headers": "sa2"})
    registered = registered_element.text.replace("\xa0", "").strip() if registered_element else "N/A"

    envelopes_element = divided_html.find("td", {"class": "cislo", "headers": "sa3"})
    envelopes = envelopes_element.text.replace("\xa0", "").strip() if envelopes_element else "N/A"

    valid_votes_element = divided_html.find("td", {"class": "cislo", "headers": "sa6"})
    valid_votes = valid_votes_element.text.replace("\xa0", "").strip() if valid_votes_element else "N/A"

    # Extrakce hlasů pro jednotlivé strany
    candidate_parties = []
    votes = []

    for headers in ["t1sa1 t1sb2", "t2sa1 t2sb2", "t3sa1 t3sb2"]:
        candidate_parties.extend([party.text.strip() for party in divided_html.find_all("td", {"headers": headers})])

    for headers in ["t1sa2 t1sb3", "t2sa2 t2sb3", "t3sa2 t3sb3"]:
        votes.extend([vote.text.replace("\xa0", "").strip() for vote in divided_html.find_all("td", {"headers": headers})])

    data = {
        "kód obce": code,
        "název obce": name,
        "voliči v seznamu": registered,
        "vydané obálky": envelopes,
        "platné hlasy": valid_votes,
    }

    # Přidání hlasů pro každou stranu
    for party, vote in zip(candidate_parties, votes):
        data[party] = vote

    print(f"Získána data pro obec: {name}")
    return data

# Hlavní funkce
def main(link, output):
    municipality_list = get_municipality_links(link)
    all_data = []

    for code, name, municipality_link in municipality_list:
        municipality_data = get_data(code, name, municipality_link)
        if municipality_data is not None:
            all_data.append(municipality_data)

    # Vytvoření DataFrame

    df = pd.DataFrame(all_data)
    print(df.head())

    # Uložení dat 

    df.to_csv(output, index=False, encoding='utf-8')
    print(f"Data uložena do souboru: {output}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Použití: python3 projekt_3.py <URL> <vystupni_soubor>")
        sys.exit(1)

    link = sys.argv[1]
    output = sys.argv[2]

    if not link.startswith("https://www.volby.cz/pls/ps2017nss"):
        print("Nesprávný odkaz na územní celek.")
        sys.exit(1)

    main(link, output)