from dataclasses import dataclass, fields
from typing import Dict

from extractor import Tense, Imperativo


@dataclass
class Translation:
    es: str
    pl: str
    irregular: bool

    @staticmethod
    def empty():
        return Translation('', '', False)

    @staticmethod
    def no_translation(es: str, irregular: bool):
        return Translation(es, '', irregular)


@dataclass
class TranslatedTense:
    yo: Translation
    tu: Translation
    el: Translation
    ns: Translation
    vs: Translation
    ellos: Translation

    def __getitem__(self, item: int):
        return getattr(self, fields(self)[item].name)

    @classmethod
    def empty(cls):
        return cls(*[Translation.empty() for i in fields(cls)])


@dataclass
class TranslatedImperativo:
    tu: Translation
    el: Translation
    ns: Translation
    vs: Translation
    ellos: Translation

    def __getitem__(self, item: int):
        return getattr(self, fields(self)[item].name)

    @classmethod
    def empty(cls):
        return cls(*[Translation.empty() for i in fields(cls)])


@dataclass
class TranslatedVerbConjugation:
    infinitivo: str
    polish: str
    english: str

    presente: TranslatedTense
    pret_indefinido: TranslatedTense
    pret_perfecto: Tense
    presente_progresivo: Tense
    pret_imperfecto: Tense
    futuro_simple: Tense
    imperativo: Imperativo

    def translated_tenses(self) -> Dict[str, TranslatedTense]:
        return {
            'presente': self.presente,
            'pret_indefinido': self.pret_indefinido,
        }

    def bare_tenses(self) -> Dict[str, Tense]:
        return {
            'pret_perfecto': self.pret_perfecto,
            'presente_progresivo': self.presente_progresivo,
            'pret_imperfecto': self.pret_imperfecto,
            'imperativo': self.imperativo,
            'futuro_simple': self.futuro_simple,
        }
