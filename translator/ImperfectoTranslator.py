from extractor import Tense
from params import TensTranslationBase, TranslationParams
from translator import Translator, substitute, substitute_end, append, TranslatedTense, Translation
from translator.LetterUtils import self_ending


class ImperfectoTranslator:

    prefix = {
        "yo": "zwykłem",
        "tu": "zwykłeś",
        "el": "zwykł",
        "ns": "zwykliśmy",
        "vs": "zwykliście",
        "ellos": "zwykli",
    }

    @staticmethod
    def add_prefix(person, infinitivo, zwrotny) -> str:
        return f"{ImperfectoTranslator.prefix[person]} {infinitivo}{self_ending(infinitivo, zwrotny)}"

    @staticmethod
    def translate_past_with_root(infinitivo, trans, zwrotny:  TranslationParams) -> TranslatedTense:
        return TranslatedTense(
            yo=Translation(trans.yo.conjugation,       ImperfectoTranslator.add_prefix("yo", infinitivo, zwrotny),    trans.yo.irregular),
            tu=Translation(trans.tu.conjugation,       ImperfectoTranslator.add_prefix("tu", infinitivo, zwrotny),    trans.tu.irregular),
            el=Translation(trans.el.conjugation,       ImperfectoTranslator.add_prefix("el", infinitivo, zwrotny),    trans.el.irregular),
            ns=Translation(trans.ns.conjugation,       ImperfectoTranslator.add_prefix("ns", infinitivo, zwrotny),    trans.ns.irregular),
            vs=Translation(trans.vs.conjugation,       ImperfectoTranslator.add_prefix("vs", infinitivo, zwrotny),    trans.vs.irregular),
            ellos=Translation(trans.ellos.conjugation, ImperfectoTranslator.add_prefix("ellos", infinitivo, zwrotny), trans.ellos.irregular),
        )
