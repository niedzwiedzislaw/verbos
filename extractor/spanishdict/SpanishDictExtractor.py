import requests
from bs4 import BeautifulSoup

from extractor import *


class SpanishDictExtractor:

    use_em_irregular = True
    limit_english_translations = 1

    @classmethod
    def parse_conjugation(cls, item) -> ConjugationData:
        irregular = item.find('span', {'class': 'conj-irregular'})
        if cls.use_em_irregular:
            if irregular:
                tag = BeautifulSoup().new_tag("em")
                tag.string = irregular.text
                item.find('span', {'class': 'conj-irregular'}).replaceWith(tag)
            inner = item.find('div').find('div').find('div').find('a').find('div')
            text = inner.decode_contents().replace("\n", "").strip()
        else:
            text = item.text.replace("\n", "").strip()
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
    def extract_english(cls, soup: BeautifulSoup) -> str:
        def f(i): return soup.find('div', id=f"quickdef{i}-es")
        translation = f(1)
        i = 1
        results = []
        while translation is not None and i <= cls.limit_english_translations:
            results.append(translation.text.strip())
            translation = soup.find('div', id=f"quickdef{i}-es")
            i += 1
        return ', '.join(results)

    @classmethod
    def extract_infinitivo(cls, soup: BeautifulSoup, verb) -> str:
        header = soup.find('h1')
        return header.text.strip()

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
            infinitivo_con_accentos = cls.extract_infinitivo(soup, verb)
            ingles = cls.extract_english(soup)
            presente = cls.extract_presente(soup)
            pret_indefinido = cls.extract_pret_indefinido(soup)
            pret_perfecto = cls.extract_pret_perfecto(soup)
        except Exception as e:
            print(f'Problem with {verb}')
            print(f"URL: https://www.spanishdict.com/conjugate/{verb}")
            raise e
        else:
            return VerbData(infinitivo_con_accentos, ingles, presente, pret_indefinido, pret_perfecto)
