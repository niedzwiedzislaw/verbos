import requests
from bs4 import BeautifulSoup

from model import VerbData, Tense, Verb, TranslatedImperativo, ConjugationData
from translator import Translator


class Extractor:

    @staticmethod
    def parse_conjugation(item) -> ConjugationData:
        irregular = item.find_all('span', {'class': 'bg-red-600'})
        return ConjugationData(item.text.strip(), len(irregular) > 0)

    @staticmethod
    def extract_presente(soup: BeautifulSoup) -> Tense:
        div = soup.find('div', {'id': 'present-indicative'})
        table = div.find('table')
        c = table.find_all('td', {'class': 'spanish-conjugation'})

        return Tense(*[Extractor.parse_conjugation(i) for i in c])

    @staticmethod
    def extract_pret_indefinido(soup: BeautifulSoup) -> Tense:
        div = soup.find('div', {'id': 'preterite-indicative'})
        table = div.find('table')
        c = table.find_all('td', {'class': 'spanish-conjugation'})
        return Tense(*[Extractor.parse_conjugation(i) for i in c])

    @staticmethod
    def extract_pret_perfecto(soup: BeautifulSoup) -> Tense:
        div = soup.find('div', {'id': 'present-perfect-indicative'})
        table = div.find('table')
        c = table.find_all('td', {'class': 'spanish-conjugation'})
        return Tense(*[Extractor.parse_conjugation(i) for i in c])

    @staticmethod
    def extract_verb_data(verb) -> VerbData:
        try:
            f = open(f'cache/{verb}.html', encoding='utf-8').read()
        except:
            f = requests.get(f"https://ellaverbs.com/spanish-verbs/{verb}-conjugation/").text
            with open(f'cache/{verb}.html', 'w', encoding='utf-8') as h:
                h.write(f)

        soup = BeautifulSoup(f, 'html.parser')
        presente = Extractor.extract_presente(soup)
        pret_indefinido = Extractor.extract_pret_indefinido(soup)
        pret_perfecto = Extractor.extract_pret_perfecto(soup)
        return VerbData(verb, presente, pret_indefinido, pret_perfecto)

    @staticmethod
    def extract_with_translation(verb: str, polski='', past_root_sg='', past_root_pl='', present_root_sg='', present_root_pl='') -> Verb:
        present_root_pl = present_root_pl or present_root_sg

        verb_data = Extractor.extract_verb_data(verb)

        present_translation = Translator.translate_present_with_root(
            verb, verb_data.presente, present_root_sg, present_root_pl)
        past_translation = Translator.translate_past_with_root(
            verb, verb_data.pret_indefinido, past_root_sg, past_root_pl)
        v = Verb(verb_data.infinitivo, polski, '', present_translation, past_translation, verb_data.pret_perfecto, TranslatedImperativo.empty())
        return v