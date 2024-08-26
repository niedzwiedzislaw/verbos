import requests
import tqdm
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
    def extract_preterito_imperfecto(cls, soup: BeautifulSoup) -> Tense:
        tbody = soup.findAll('tbody')[1]
        cells = [row.findAll('td')[3] for row in tbody.findAll('tr')[1:]]
        return Tense(*[cls.parse_conjugation(i) for i in cells])

    @classmethod
    def extract_imperativo(cls, soup: BeautifulSoup) -> Imperativo:
        tbody = soup.findAll('tbody')[3]
        tr = tbody.findAll('tr')
        # cells = [row.findAll(['th', 'td'])[1] for row in tr[2:]]
        cells = [row.findAll('td')[0] for row in tr[2:]]
        return Imperativo(*[cls.parse_conjugation(i) for i in cells])

    @classmethod
    def extract_presente_progresivo(cls, soup: BeautifulSoup) -> Tense:
        tbody = soup.findAll('tbody')[4]
        cells = [row.findAll('td')[1] for row in tbody.findAll('tr')[1:]]
        return Tense(*[cls.parse_conjugation(i) for i in cells])

    @classmethod
    def extract_pret_perfecto(cls, soup: BeautifulSoup) -> Tense:
        tbody = soup.findAll('tbody')[5]
        cells = [row.findAll('td')[1] for row in tbody.findAll('tr')[1:]]
        return Tense(*[cls.parse_conjugation(i) for i in cells])

    @classmethod
    def extract_participio(cls, soup: BeautifulSoup) -> str:
        div = soup.find('div', {'id': 'sd-participles-section'})
        tbody = div.find('tbody')
        cell = tbody.findAll('td')[3]
        return cell.text

    @classmethod
    def extract_gerundio(cls, soup: BeautifulSoup) -> str:
        div = soup.find('div', {'id': 'sd-participles-section'})
        tbody = div.find('tbody')
        cell = tbody.findAll('td')[1]
        return cell.text

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
            print(f'Downloading {verb}')
            f = requests.get(f"https://www.spanishdict.com/conjugate/{verb}").text
            with open(f'cache/spanishdict/{verb}.html', 'w', encoding='utf-8') as h:
                h.write(f)

        try:
            soup = BeautifulSoup(f, 'html.parser')
            return VerbData(
                cls.extract_infinitivo(soup, verb),
                cls.extract_gerundio(soup),
                cls.extract_participio(soup),
                cls.extract_english(soup),
                cls.extract_presente(soup),
                cls.extract_pret_indefinido(soup),
                cls.extract_pret_perfecto(soup),
                cls.extract_presente_progresivo(soup),
                cls.extract_preterito_imperfecto(soup),
                cls.extract_imperativo(soup)
            )
        except Exception as e:
            print(f'Problem with {verb}')
            print(f"URL: https://www.spanishdict.com/conjugate/{verb}")
            raise e
