import builtins
import typing
from dataclasses import field, dataclass, fields
from typing import List
from unittest import case

from hints import hints
from anki import Card
from settings import separator
from translator import TranslatedVerbConjugation

tense_names = {
    'presente': 'presente',
    'pret_indefinido': 'pret. indefinido',
    'pret_perfecto': 'pret. perfecto',
    'presente_progresivo': 'presente progresivo',
    'pret_imperfecto': 'pretérito imperfecto',
    'futuro_simple': 'futuro',
}

mode_names = {
    'imperativo': 'imperativo'
}

case_names = tense_names | mode_names

person_abbr_with_accents = {
    'yo': 'yo',
    'tu': 'tú',
    'el': 'él',
    'ud': 'usted',
    'ns': 'ns',
    'vs': 'vs',
    'ellos': 'ellos',
    'uds': 'ustedes'
}


@dataclass
class Card:
    question: str = field(init=False, repr=False)
    infinitivo: str
    polski: str
    english: str
    person: str
    case: str
    conj_espanol: str
    conj_polski: str
    irregular: bool
    hint: str
    tags: List[str] = field(default_factory=list)

    def __post_init__(self):
        self.question = f'{self.infinitivo}, {person_abbr_with_accents[self.person]}, {case_names[self.case]}'

    def values(self) -> List[str]:
        return [self.__format(getattr(self, f.name)) for f in fields(self)]

    def verify_type(self, persons: List[str], times: List[str]) -> bool:
        return self.person in persons and self.case in times

    def __format(self, f):
        t = type(f)
        match t:
            case builtins.bool:
                return str(f).lower()
            case builtins.list:
                return ",".join(f)
            case _:
                return f


    @staticmethod
    def get_headers(sep=separator):
        return sep.join([f.name for f in fields(Card)])

    @staticmethod
    def create_cards(verb: TranslatedVerbConjugation) -> List['Card']:
        cards = []
        for (tense, translations) in verb.translated_tenses().items():
            for c in fields(translations):
                person = c.name
                conj = getattr(translations, person)
                card = Card(verb.infinitivo, verb.polish, verb.english, person, tense, conj.es, conj.pl, conj.irregular,
                            verb.infinitivo if verb.infinitivo in hints else '')
                cards.append(card)

        for (tense, formas) in verb.bare_tenses().items():
            for c in fields(formas):
                person = c.name
                conj = getattr(formas, person)
                card = Card(verb.infinitivo, verb.polish, verb.english, person, tense, conj.conjugation, '',
                            conj.irregular, verb.infinitivo if verb.infinitivo in hints else '')
                cards.append(card)
        return cards
