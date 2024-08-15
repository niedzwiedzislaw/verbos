from dataclasses import dataclass


@dataclass
class ConjugationData:
    conjugation: str
    irregular: bool


@dataclass
class Tense:
    yo: ConjugationData
    tu: ConjugationData
    el: ConjugationData
    ns: ConjugationData
    vs: ConjugationData
    ellos: ConjugationData


@dataclass
class VerbData:
    infinitivo: str
    gerundio: str
    participio: str
    ingles: str
    presente: Tense
    pret_indefinido: Tense
    pret_perfecto: Tense
    presente_progresivo: Tense
