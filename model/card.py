from dataclasses import field, dataclass, fields
from typing import List

from hints import hints
from model import Verb

names = {
    'presente': 'presente',
    'pret_indefinido': 'pret. indefinido',
    'pret_perfecto': 'pret. perfecto',
}


@dataclass
class Card:
    index: str = field(init=False, repr=False)
    infinitivo: str
    polski: str
    english: str
    person: str
    case: str
    conj_spanish: str
    conj_polish: str
    irregular: bool
    hint: str

    def __post_init__(self):
        self.index = f"{self.infinitivo}, {self.person}, {names[self.case]}"

    def to_line(self, sep=";"):
        values = [str(getattr(self, f.name)) for f in fields(self)]
        return sep.join(values)

    @staticmethod
    def get_headers(sep=';'):
        return sep.join(['question', 'infinitivo', 'polski', 'english', 'person', 'case', 'conj_espanol', 'conj_polski', 'irregular', 'hint'])


def create_cards(verb: Verb) -> List[Card]:
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
            card = Card(verb.infinitivo, verb.polish, verb.english, person, tense, conj.conjugation, '', conj.irregular, verb.infinitivo if verb.infinitivo in hints else '')
            cards.append(card)
    return cards
