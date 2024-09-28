# PROJEKT 3: SCRAPER VÝSLEDKŮ VOLEB

Toto je třetí projet v rámci Engeto Online Python Akademie. 
Cílem projektu je vytvořit webový scraper pro výsledky voleb do Poslanecké sněmovny z roku 2017. 
Program scrappuje data z webu volby.cz a ukládá je do souboru CSV.

## Autor
- Ngoc Khanh Vy Tranová
- Email: ngtranova@gmail.com
- Discord: veelilly

## Popis
Program scrappuje výsledky voleb z konkrétního územního celku České republiky. 
Stačí zadat URL konkrétního území (např. kraj nebo obec) a výstupní soubor CSV, kam se data uloží. 
Výstupní CSV obsahuje informace o počtu registrovaných voličů, vydaných obálkách, platných hlasech a počtu hlasů pro jednotlivé kandidující strany.

## Instalace knihoven

Projekt vyžaduje Python a několik externích knihoven. 
Tyto knihovny je možné nainstalovat pomocí souboru requirements.txt:
_**pip3 install -r requirements.txt**_

**Seznam knihoven:**

1. **Requests:** _Pro stahování obsahu webu._
2. **BeautifulSoup4:** _Pro parsování HTML obsahu._
3. **Pandas:** _Pro práci s daty a export do CSV._

## Použití
Pro spuštění programu použijte následující příkaz:
_**python3 projekt_3.py <link_kraje_nebo_obce> <název_výstupního_souboru>**_

_příklad:
python3 projekt_3.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=5&xnumnuts=4101" "vysledky_voleb.csv"_

## Výstup

**Struktura dat v CSV souboru**
1. **kód obce:** _Kód obce, kde volby probíhaly._
2. **název obce:** _Název obce._
3. **voliči v seznamu:** _Počet registrovaných voličů._
4. **vydané obálky:** _Počet vydaných obálek._
5. **platné hlasy:** _Počet platných hlasů._
6. **hlasy pro jednotlivé strany:** _Každý sloupec reprezentuje jednu stranu a obsahuje počet hlasů._

**Struktura kódu**
- Program je rozdělen do několika funkcí:

1. **get_region_links(link):** _Získá odkazy na všechny kraje z hlavní stránky._
2. **get_municipality_links(region_link):** _Získá odkazy na všechny obce v daném kraji._
3. **get_data(municipality_link):** _Získá volební výsledky pro jednotlivou obec._
4. **main(region_link, output):** _Řídí celý proces scrappingu a ukládání dat._

### Vysvětlení
- README obsahuje všechny základní informace o projektu, včetně účelu, požadavků, instalace, použití a struktury kódu.
- Instrukce jsou přizpůsobeny pro MacOS, s použitím `python3` a `pip`.
- Uživatelé jsou vedeni krok za krokem, aby mohli snadno nainstalovat knihovny a spustit program.





