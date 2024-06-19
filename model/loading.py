from dataclasses import dataclass, fields


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
    presente: Tense
    pret_indefinido: Tense
    pret_perfecto: Tense
