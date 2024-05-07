from dataclasses import dataclass


@dataclass
class Ficha:
    infinitivo
    person
    tense

    def index(self):
        return self.infinitivo + self.person + self.tens
