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
class Conjugation:
    form: str
    irrregular: bool


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
class Verb:
    infinitivo: str
    polish: str
    english: str

    present: TranslatedTense
    past: TranslatedTense
    imp: TranslatedImperativo
