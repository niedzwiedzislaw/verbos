from dataclasses import dataclass, fields

from model import Verb


@dataclass
class Card:
    infinitivo: str
    person: str
    case: str
    spanish: str
    polish: str
    irregular: bool

    def index(self) -> str:
        return f"{self.infinitivo}, {self.person}, {self.case}"

    def to_line(self, sep=";"):
        values = [str(getattr(self, f.name)) for f in fields(self)]
        return sep.join([self.index()] + values)



def create_cards(verb: Verb):
    cards = []
    tenses = ['present', 'past']
    for tense in tenses:
        translations = getattr(verb, tense)
        for c in fields(translations):
            person = c.name
            conj = getattr(translations, person)
            card = Card(verb.infinitivo, person, tense, conj.es, conj.pl, False)
            cards.append(card)
    return cards
