from dataclasses import dataclass, fields


@dataclass
class Tense:
    yo: str
    tu: str
    el: str
    ns: str
    vs: str
    ellos: str


@dataclass
class VerbData:
    infinitivo: str
    present: Tense
    past: Tense


@dataclass
class Translation:
    es: str
    pl: str

    @staticmethod
    def empty():
        return Translation('', '')


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

    @staticmethod
    def empty():
        return TranslatedTense(*[Translation.empty() for i in range(6)])


@dataclass
class Verb:
    infinitivo: str
    english: str
    polish: str

    present: TranslatedTense
    past: TranslatedTense
