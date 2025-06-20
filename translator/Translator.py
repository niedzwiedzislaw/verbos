from extractor import Tense, VerbData
from params import TensTranslationBase, TranslationParams
from translator import TranslatedTense, Translation, TranslatedImperativo, TranslatedVerbConjugation
from translator import substitute, substitute_end, append
from translator.ImperfectoTranslator import ImperfectoTranslator
from translator.IndefinidoTranslator import IndefinidoTranslator
from translator.PerfectoTranslator import PerfectoTranslator
from translator.PresenteTranslator import PresenteTranslator


class Translator:

    @staticmethod
    def build_root_pl_from_sg(root_sg) -> str:
        return (
                substitute_end(root_sg, 'ił', 'ili') or
                substitute_end(root_sg, 'ciał', 'cieli') or
                substitute_end(root_sg, 'miał', 'mieli') or
                substitute_end(root_sg, 'iał', 'iali') or
                substitute_end(root_sg, 'ał', 'ali')
        )

    @classmethod
    def add_translations(cls, verb_data: VerbData, translation_params: TranslationParams) -> TranslatedVerbConjugation:
        present_translation = PresenteTranslator.translate_present_with_root(
            verb_data.infinitivo, verb_data.presente, translation_params.present)
        indefinido_translation = IndefinidoTranslator.translate_past_with_root(
            verb_data.infinitivo, verb_data.pret_indefinido, translation_params.past)
        imperfecto_translation = ImperfectoTranslator.translate_past_with_root(
            translation_params.polski, verb_data.pret_imperfecto, translation_params)
        perfecto_translation = PerfectoTranslator.translate_past_with_root(
            verb_data.infinitivo, verb_data.pret_perfecto, indefinido_translation)

        return TranslatedVerbConjugation(
            verb_data.infinitivo,
            translation_params.polski,
            verb_data.ingles,

            present_translation,
            indefinido_translation,
            perfecto_translation,
            verb_data.presente_progresivo,
            imperfecto_translation,
            verb_data.futuro_simple,
            verb_data.imperativo_afirmativo,
            verb_data.imperativo_negativo,
        )
