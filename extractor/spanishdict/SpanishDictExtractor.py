import requests
from bs4 import BeautifulSoup, Tag

from model import VerbData, Tense, Verb, TranslatedImperativo, ConjugationData
from model import VerbData
from reader import CsvInputRow
from translator import Translator


class SpanishDictExtractor:

    @classmethod
    def parse_conjugation(cls, item) -> ConjugationData:
        irregular = item.find('span', {'class': 'conj-irregular'})
        if irregular:
            tag = BeautifulSoup().new_tag("em")
            tag.string = irregular.text
            item.find('span', {'class': 'conj-irregular'}).replaceWith(tag)
        inner = item.find('div').find('div').find('div').find('a').find('div')
        # text = inner.decode_contents().replace("\n", "").strip()
        text = inner.text.replace("\n", "").strip()
        return ConjugationData(text, irregular is not None)

    @classmethod
    def extract_presente(cls, soup: BeautifulSoup) -> Tense:
        tbody = soup.findAll('tbody')[1]
        cells = [row.findAll('td')[1] for row in tbody.findAll('tr')[1:]]
        return Tense(*[cls.parse_conjugation(i) for i in cells])

    @classmethod
    def extract_pret_indefinido(cls, soup: BeautifulSoup) -> Tense:
        tbody = soup.findAll('tbody')[1]
        cells = [row.findAll('td')[2] for row in tbody.findAll('tr')[1:]]
        return Tense(*[cls.parse_conjugation(i) for i in cells])

    @classmethod
    def extract_pret_perfecto(cls, soup: BeautifulSoup) -> Tense:
        tbody = soup.findAll('tbody')[5]
        cells = [row.findAll('td')[1] for row in tbody.findAll('tr')[1:]]
        return Tense(*[cls.parse_conjugation(i) for i in cells])

    @classmethod
    def extract_verb_data(cls, verb) -> VerbData:
        try:
            f = open(f'cache/spanishdict/{verb}.html', encoding='utf-8').read()
        except:
            f = requests.get(f"https://www.spanishdict.com/conjugate/{verb}").text
            with open(f'cache/spanishdict/{verb}.html', 'w', encoding='utf-8') as h:
                h.write(f)

        try:
            soup = BeautifulSoup(f, 'html.parser')
            ingles = soup.find('div', id="quickdef1-es").text.strip()
            presente = cls.extract_presente(soup)
            pret_indefinido = cls.extract_pret_indefinido(soup)
            pret_perfecto = cls.extract_pret_perfecto(soup)
        except Exception as e:
            print(f'Problem with {verb}')
            print(f"URL: https://www.spanishdict.com/conjugate/{verb}")
            raise e
        else:
            return VerbData(verb, ingles, presente, pret_indefinido, pret_perfecto)

    @classmethod
    def extract_with_translation(cls, input_data: CsvInputRow) -> Verb:
        verb_data = cls.extract_verb_data(input_data.verb)

        present_translation = Translator.translate_present_with_root(
            input_data.verb, verb_data.presente, input_data.present)
        past_translation = Translator.translate_past_with_root(
            input_data.verb, verb_data.pret_indefinido, input_data.past)

        v = Verb(verb_data.infinitivo, input_data.polski, verb_data.ingles, present_translation, past_translation,
                 verb_data.pret_perfecto, TranslatedImperativo.empty())
        return v
