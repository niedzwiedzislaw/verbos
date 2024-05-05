# This is a sample Python script.
import sys
import csv
from dataclasses import dataclass, astuple, asdict
from typing import List

import pandas as pd
import requests
from bs4 import BeautifulSoup


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


@dataclass
class Tens:
    yo: str
    tu: str
    el: str
    ns: str
    vs: str
    ellos: str


@dataclass
class Translation:
    es: str
    pl: str

@dataclass
class TranslatedTens:
    yo: Translation
    tu: Translation
    el: Translation
    ns: Translation
    vs: Translation
    ellos: Translation


@dataclass
class Verb:
    infinitivo: str
    english: str
    polish: str

    present: TranslatedTens
    past: TranslatedTens

def translate_present_with_root(verb: str, trans, root_sg: str, root_pl: str) -> TranslatedTens:
    def persona_pl_1():
        match root_sg:
            case r if root_sg.endswith('e'): #sieje
                return root_sg[:-1] + 'ę'
            case r if root_sg.endswith('y'): #kończy
                return root_sg[:-1] + 'ę'
            case r if root_sg.endswith('a'): #zna
                return root_sg + 'm'
            case r if root_sg.endswith('si'): #nosi
                return root_sg[:-2] + 'szę'
            case r if root_sg.endswith('i'): #śpi
                return root_sg[:-1] + 'ę'
            case r if root_sg.endswith('ści'): #czyści
                return root_sg[:-3] + 'szczę'
            case r if root_sg.endswith('dzie'): #kładzie
                return root_sg[:-4] + 'dę'
            case r:
                return root_sg + "em"

    się = ' się' if verb.endswith("se") else ''
    return TranslatedTens(
        yo=Translation(trans.yo, f"{persona_pl_1()}{się}"),
        tu=Translation(trans.tu, root_sg + f"sz{się}"),
        el=Translation(trans.el, root_sg + f"{się}"),
        ns=Translation(trans.ns, root_pl + f"my{się}"),
        vs=Translation(trans.vs, root_pl + f"cie{się}"),
        ellos=Translation(trans.ellos, root_pl + f"ą{się}"),
    )
def translate_past_with_root(verb, trans, root_sg, root_pl) -> TranslatedTens:
    się = ' się' if verb.endswith("se") else ''
    return TranslatedTens(
        yo=Translation(trans.yo, root_sg + f"em{się}"),
        tu=Translation(trans.tu, root_sg + f"eś{się}"),
        el=Translation(trans.el, root_sg + f"{się}"),
        ns=Translation(trans.ns, root_pl + f"śmy{się}"),
        vs=Translation(trans.vs, root_pl + f"ście{się}"),
        ellos=Translation(trans.ellos, root_pl + f"{się}"),
    )


def extract_present_indicative(soup: BeautifulSoup) -> Tens:
    div = soup.find('div', {'id': 'present-indicative'})
    table = div.find('table')
    c = table.find_all('td', {'class': 'spanish-conjugation'})
    return Tens(*[i.text.strip() for i in c])

def extract_preterite(soup: BeautifulSoup) -> Tens:
    div = soup.find('div', {'id': 'preterite-indicative'})
    table = div.find('table')
    c = table.find_all('td', {'class': 'spanish-conjugation'})
    return Tens(*[i.text.strip() for i in c])

def extract(verb, polish_root_sg='', polish_root_pl='', present_root_sg='', present_root_pl=''):
    się = ' się' if verb.endswith("se") else ''
    present_root_pl = present_root_pl or present_root_sg
    try:
        f = open(f'cache/{verb}.html', encoding='utf-8').read()
    except:
        f = requests.get(f"https://ellaverbs.com/spanish-verbs/{verb}-conjugation/").text
        with open(f'cache/{verb}.html', 'w', encoding='utf-8') as h:
            h.write(f)

    soup = BeautifulSoup(f, 'html.parser')
    present = extract_present_indicative(soup)
    pr = translate_present_with_root(verb, present, present_root_sg, present_root_pl)
    past = extract_preterite(soup)
    pa = translate_past_with_root(verb, past, polish_root_sg, polish_root_pl)
    # translations = present + past
    # print(pa)
    v = Verb(verb, '', '', pr, pa)
    df = pd.json_normalize(asdict(x) for x in [v])
    print(df)
    print(df.to_csv(index=False))
    with open("Spanish__conjuBuild passed after gación.txt", "a", encoding='utf-8') as f:
        w = csv.writer(f, delimiter='\t')
        df.to_csv(f, index=False, header=False)

    # with open("../Spanish__conjuBuild passed after gación.txt", "a", encoding='utf-8') as f:
    #     f.write(f'{translations[0]}	{verb}	yo	pretérito indefinido		{polish_root_sg}em{się}\n')
    #     f.write(f'{translations[1]}	{verb}	tú	pretérito indefinido		{polish_root_sg}eś{się}\n')
    #     f.write(f'{translations[2]}	{verb}	él / ella / usted	pretérito indefinido		{polish_root_sg}{się}\n')
    #     f.write(f'{translations[3]}	{verb}	nosotros	pretérito indefinido		{polish_root_pl}śmy{się}\n')
    #     f.write(f'{translations[4]}	{verb}	vosotros	pretérito indefinido		{polish_root_pl}ście{się}\n')
    #     f.write(f'{translations[5]}	{verb}	ellos / ellas / ustedes	pretérito indefinido		{polish_root_pl}{się}\n')

def try_extract(verb, polish_root_sg='', polish_root_pl=''):
    try:
        extract(verb, polish_root_sg, polish_root_pl)
    except:
        print(f"error when {verb}")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    extract("ir", 'był', 'byli', 'jest')
    extract("ser", 'szedł', 'szli', 'id')
    extract("estar", 'był', 'byli', 'jest')
    extract("dormir", 'spał', 'spali', 'śpi')
    extract("vestir", 'nosił', 'nosili', 'nosi')
    extract("volver", 'wracał', 'wracali', 'wraca')
    extract("comer", 'jadł', 'jedli', 'je')
    extract("salir", 'wyszedł', 'wyszli', 'wyszedł')
    extract("comprar", 'kupił', 'kupili', 'kupuje')
    extract("limpiar", 'czyścił', 'czyścili', 'czyści')
    extract("preparar", 'przygotował', 'przygotowali', 'przygotowuje')
    extract("acabar", 'skończył', 'skończyli', 'kończy')
    extract("acostarse", 'położył', 'położyli', 'kładzie')
    extract("levantarse", 'wstał', 'wstali', 'wstaje')
    extract("ver", 'oglądał', 'oglądali', 'ogląda')
    extract("empezar", 'zaczynał', 'zaczynali', 'zaczyna')
    extract("escribir", 'pisał', 'pisali', 'pisze')
    extract("despertarse", 'budził', 'budzili', 'budzi')
    extract("llamarse", 'nazywał', 'nazywali', 'nazywa')
    extract("saber", 'myślał', 'myśleli', 'myśli')
    extract("vestirse", "", "", '')
    extract("conocer", "znał", "znali", 'zna')
    extract("lavarse", "", "", '')
    extract("poder", "", "", '')
    extract("cerrar", "", "", '')
    extract("dar", "", "", '')
    extract("repetir", "", "", '')
    extract("pensar", "", "", '')
    extract("preferir", "", "", '')
    extract("sentir", "", "", '')
    extract("querer", "chciał", "chcieli", 'chce')


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
