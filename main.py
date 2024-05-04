# This is a sample Python script.
import sys
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

@dataclass
class Verb:
    infinitivo: str
    english: str
    polish: str

def extract(verb, polish_root_sg='', polish_root_pl=''):
    się = ' się' if verb.endswith("se") else ''
    try:
        f = open(f'cache/{verb}.html', encoding='utf-8').read()
    except:
        f = requests.get(f"https://ellaverbs.com/spanish-verbs/{verb}-conjugation/").text
        with open(f'cache/{verb}.html', 'w', encoding='utf-8') as h:
            h.write(f)

    soup = BeautifulSoup(f, 'html.parser')

    print('Title:', soup.title.string)
    div = soup.find('div', {'id': 'preterite-indicative'})
    table = div.find('table')
    c = table.find_all('td', {'class': 'spanish-conjugation'})
    translations = [i.text.strip() for i in c]

    with open("../Spanish__conjuBuild passed after gación.txt", "a", encoding='utf-8') as f:
        f.write(f'{translations[0]}	{verb}	yo	pretérito indefinido		{polish_root_sg}em{się}\n')
        f.write(f'{translations[1]}	{verb}	tú	pretérito indefinido		{polish_root_sg}eś{się}\n')
        f.write(f'{translations[2]}	{verb}	él / ella / usted	pretérito indefinido		{polish_root_sg}{się}\n')
        f.write(f'{translations[3]}	{verb}	nosotros	pretérito indefinido		{polish_root_pl}śmy{się}\n')
        f.write(f'{translations[4]}	{verb}	vosotros	pretérito indefinido		{polish_root_pl}ście{się}\n')
        f.write(f'{translations[5]}	{verb}	ellos / ellas / ustedes	pretérito indefinido		{polish_root_pl}{się}\n')

def try_extract(verb, polish_root_sg='', polish_root_pl=''):
    try:
        extract(verb, polish_root_sg, polish_root_pl)
    except:
        print(f"error when {verb}")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # extract("ir", 'był', 'byli')
    # extract("ser", 'szedł', 'szli')
    # extract("estar", 'był', 'byli')
    # extract("dormir", 'spał', 'spali')
    # extract("vestir", 'nosił', 'nosili')
    # extract("volver", 'wracał', 'wracali')
    # extract("comer", 'jadł', 'jedli')
    # extract("salir", 'wyszedł', 'wyszli')
    # extract("comprar", 'kupił', 'kupili')
    # extract("limpiar", 'czyścił', 'czyścili')
    # extract("preparar", 'przygotował', 'przygotowali')
    # extract("acabar", 'skończył', 'skończyli')
    # extract("acostarse", 'położył', 'położyli', True)
    # extract("levantarse", 'wstał', 'wstali')
    # extract("ver", 'oglądał', 'oglądali')
    # extract("empezar", 'zaczynał', 'zaczynali')
    # extract("escribir", 'pisał', 'pisali')
    # extract("despertarse", 'budził', 'budzili', True)
    # extract("llamarse", 'nazywał', 'nazywali', True)
    # extract("saber", 'myślał', 'myśleli', True)
    extract("vestirse", "", "")
    extract("conocer", "", "")
    extract("lavarse", "", "")
    extract("poder", "", "")
    extract("cerrar", "", "")
    extract("dar", "", "")
    extract("repetir", "", "")
    extract("pensar", "", "")
    extract("preferir", "", "")
    extract("sentir", "", "")
    extract("querer", "", "")


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
