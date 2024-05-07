from dataclasses import asdict

import pandas as pd
import requests
from bs4 import BeautifulSoup
from pandas import DataFrame

from model import Tense, VerbData, Verb, TranslatedTense, TranslatedImperativo
from translation import translate_present_with_root, translate_past_with_root


def extract_present_indicative(soup: BeautifulSoup) -> Tense:
    div = soup.find('div', {'id': 'present-indicative'})
    table = div.find('table')
    c = table.find_all('td', {'class': 'spanish-conjugation'})
    return Tense(*[i.text.strip() for i in c])


def extract_preterite(soup: BeautifulSoup) -> Tense:
    div = soup.find('div', {'id': 'preterite-indicative'})
    table = div.find('table')
    c = table.find_all('td', {'class': 'spanish-conjugation'})
    return Tense(*[i.text.strip() for i in c])


def extract_verb_data(verb) -> VerbData:
    try:
        f = open(f'cache/{verb}.html', encoding='utf-8').read()
    except:
        f = requests.get(f"https://ellaverbs.com/spanish-verbs/{verb}-conjugation/").text
        with open(f'cache/{verb}.html', 'w', encoding='utf-8') as h:
            h.write(f)

    soup = BeautifulSoup(f, 'html.parser')
    present = extract_present_indicative(soup)
    past = extract_preterite(soup)
    return VerbData(verb, present, past)


def extract(verb, polski='', past_root_sg='', past_root_pl='', present_root_sg='', present_root_pl='') -> Verb:
    present_root_pl = present_root_pl or present_root_sg

    data = extract_verb_data(verb)

    present_translation = translate_present_with_root(
        verb, data.present, present_root_sg, present_root_pl)
    past_translation = translate_past_with_root(
        verb, data.past, past_root_sg, past_root_pl)
    v = Verb(verb, polski, '', present_translation, past_translation, TranslatedImperativo.empty())
    return v
