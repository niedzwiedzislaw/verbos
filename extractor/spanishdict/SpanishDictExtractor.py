import requests
from bs4 import BeautifulSoup

from model import VerbData
from reader import CsvInputRow
from translator import Translator


class SpanishDictExtractor:

    @classmethod
    def parse_conjugation(cls, item) -> ConjugationData:
        irregular = item.find_all('span', {'class': 'bg-red-600'})
        return ConjugationData(item.text.strip(), len(irregular) > 0)

    @classmethod
    def extract_presente(cls, soup: BeautifulSoup) -> Tense:
        div = soup.find('div', {'id': 'present-indicative'})
        table = div.find('table')
        c = table.find_all('td', {'class': 'spanish-conjugation'})

        return Tense(*[cls.parse_conjugation(i) for i in c])

    @classmethod
    def extract_pret_indefinido(cls, soup: BeautifulSoup) -> Tense:
        div = soup.find('div', {'id': 'preterite-indicative'})
        table = div.find('table')
        c = table.find_all('td', {'class': 'spanish-conjugation'})
        return Tense(*[cls.parse_conjugation(i) for i in c])

    @classmethod
    def extract_pret_perfecto(cls, soup: BeautifulSoup) -> Tense:
        div = soup.find('div', {'id': 'present-perfect-indicative'})
        table = div.find('table')
        c = table.find_all('td', {'class': 'spanish-conjugation'})
        return Tense(*[cls.parse_conjugation(i) for i in c])

    @classmethod
    def extract_verb_data(cls, verb) -> VerbData:
        try:
            f = open(f'cache/spanishdict/{verb}.html', encoding='utf-8').read()
        except _:
            f = requests.get(f"https://www.spanishdict.com/conjugate/{verb}").text
            with open(f'cache/spanishdict/{verb}.html', 'w', encoding='utf-8') as h:
                h.write(f)

        try:
            soup = BeautifulSoup(f, 'html.parser')
            presente = cls.extract_presente(soup)
            pret_indefinido = cls.extract_pret_indefinido(soup)
            pret_perfecto = cls.extract_pret_perfecto(soup)
        except Exception as e:
            print(f'Problem with {verb}')
            print(f"URL: https://www.spanishdict.com/conjugate/{verb}")
            raise e
        else:
            return VerbData(verb, presente, pret_indefinido, pret_perfecto)

    @classmethod
    def extract_with_translation(cls, input_data: CsvInputRow) -> Verb:
        verb_data = cls.extract_verb_data(input_data.verb)

        present_translation = Translator.translate_present_with_root(
            input_data.verb, verb_data.presente, input_data.present)
        past_translation = Translator.translate_past_with_root(
            input_data.verb, verb_data.pret_indefinido, input_data.past)

        v = Verb(verb_data.infinitivo, input_data.polski, '', present_translation, past_translation,
                 verb_data.pret_perfecto, TranslatedImperativo.empty())
        return v
