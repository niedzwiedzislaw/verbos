from extractor import Tense
from params import TensTranslationBase
from translator import TranslatedTense, Translation
from translator.IndefinidoTranslator import IndefinidoTranslator


# has +ido
class PerfectoTranslator:

    prefix = 'niedawno'

    @staticmethod
    def add_translation(perfecto, indefinido: Translation):
        if indefinido.pl:
            return Translation(perfecto.conjugation, f"{PerfectoTranslator.prefix} {indefinido.pl}", perfecto.irregular)
        else:
            return Translation.no_translation(perfecto.conjugation,  perfecto.irregular)



    @staticmethod
    def translate_past_with_root(verb, perfecto: Tense, indefinido: TranslatedTense) -> TranslatedTense:
        return TranslatedTense(
            yo=    PerfectoTranslator.add_translation(perfecto.yo, indefinido.yo),
            tu=    PerfectoTranslator.add_translation(perfecto.tu, indefinido.tu),
            el=    PerfectoTranslator.add_translation(perfecto.el, indefinido.el),
            ns=    PerfectoTranslator.add_translation(perfecto.ns, indefinido.ns),
            vs=    PerfectoTranslator.add_translation(perfecto.vs, indefinido.vs),
            ellos= PerfectoTranslator.add_translation(perfecto.ellos, indefinido.ellos),
        )
