from extractor import Tense, VerbData
from params import TensTranslationBase, TranslationParams
from translator import TranslatedTense, Translation, TranslatedImperativo, TranslatedVerbConjugation
from translator import substitute, append


class Translator:

    @staticmethod
    def translate_present_with_root(verb: str, trans: Tense, translation_base: TensTranslationBase) -> TranslatedTense:
        się = ' się' if verb.endswith("se") else ''  # todo - use translation, not verb - sacarse doesn't fit the rule
        root_sg = translation_base.singular

        def persona_sg_1():
            match root_sg:
                case '':
                    return ''
                case _:
                    return (
                            substitute(root_sg, 'wie', 'wiem') or
                            substitute(root_sg, 'oże', 'ogę') or
                            substitute(root_sg, 'si', 'szę') or
                            substitute(root_sg, 'ści', 'szczę') or
                            substitute(root_sg, 'dzie', 'dę') or
                            substitute(root_sg, ['e', 'y'], 'ę') or
                            substitute(root_sg, 'bi', 'bię') or
                            substitute(root_sg, 'wi', 'wię') or
                            substitute(root_sg, 'i', 'ę') or
                            append(root_sg, 'a', 'm') or
                            append(root_sg, '', 'em')
                    ) + się

        def persona_sg_2():

            match root_sg:
                case '':
                    return ''
                case _:
                    return (
                            substitute(root_sg, 'st', 'steś') or
                            append(root_sg, '', 'sz')
                    ) + się

        def persona_sg_3():
            match root_sg:
                case '':
                    return ''
                case x:
                    return x + się

        def persona_pl_1():
            match root_sg:
                case '':
                    return ''
                case x:
                    return x + "my" + się

        def persona_pl_2():
            match root_sg:
                case '':
                    return ''
                case _:
                    return (
                        append(root_sg, '', 'cie')
                    ) + się

        def persona_pl_3():
            match root_sg:
                case '':
                    return ''
                case _:
                    return (
                            substitute(root_sg, 'jest', 'są') or
                            substitute(root_sg, 'dzie', 'dą') or
                            substitute(root_sg, 'dzi', 'dzą') or
                            substitute(root_sg, 'e', 'ą') or
                            substitute(root_sg, 'a', 'ją') or
                            append(root_sg, '', 'ą')
                    ) + się

        return TranslatedTense(
            yo=Translation(trans.yo.conjugation, persona_sg_1(), trans.yo.irregular),
            tu=Translation(trans.tu.conjugation, persona_sg_2(), trans.tu.irregular),
            el=Translation(trans.el.conjugation, persona_sg_3(), trans.el.irregular),
            ns=Translation(trans.ns.conjugation, persona_pl_1(), trans.ns.irregular),
            vs=Translation(trans.vs.conjugation, persona_pl_2(), trans.vs.irregular),
            ellos=Translation(trans.ellos.conjugation, persona_pl_3(), trans.ellos.irregular),
        )

    @staticmethod
    def translate_past_with_root(verb, trans: Tense, translation_base: TensTranslationBase) -> TranslatedTense:
        się = ' się' if verb.endswith("se") else ''
        root_sg = translation_base.singular
        root_pl = translation_base.plural or root_sg

        def sg_1(): return root_sg + f"em" + się if root_sg else ''

        def sg_2(): return root_sg + f"eś" + się if root_sg else ''

        def sg_3(): return root_sg + f"" + się if root_sg else ''

        def pl_1(): return root_pl + f"śmy" + się if root_pl else ''

        def pl_2(): return root_pl + f"ście" + się if root_pl else ''

        def pl_3(): return root_pl + f"" + się if root_pl else ''

        return TranslatedTense(
            yo=Translation(trans.yo.conjugation, sg_1(), trans.yo.irregular),
            tu=Translation(trans.tu.conjugation, sg_2(), trans.tu.irregular),
            el=Translation(trans.el.conjugation, sg_3(), trans.el.irregular),
            ns=Translation(trans.ns.conjugation, pl_1(), trans.ns.irregular),
            vs=Translation(trans.vs.conjugation, pl_2(), trans.vs.irregular),
            ellos=Translation(trans.ellos.conjugation, pl_3(), trans.ellos.irregular),
        )

    @staticmethod
    def build_root_pl_from_sg(root_sg) -> str:
        return (
                substitute(root_sg, 'ił', 'ili') or
                substitute(root_sg, 'ciał', 'cieli') or
                substitute(root_sg, 'miał', 'mieli') or
                substitute(root_sg, 'iał', 'iali') or
                substitute(root_sg, 'ał', 'ali')
        )

    @classmethod
    def add_translations(cls, verb_data: VerbData, translation_params: TranslationParams) -> TranslatedVerbConjugation:
        present_translation = cls.translate_present_with_root(
            verb_data.infinitivo, verb_data.presente, translation_params.present)
        past_translation = cls.translate_past_with_root(
            verb_data.infinitivo, verb_data.pret_indefinido, translation_params.past)

        return TranslatedVerbConjugation(
            verb_data.infinitivo,
            translation_params.polski,
            verb_data.ingles,

            present_translation,
            past_translation,
            verb_data.pret_perfecto,
            verb_data.presente_progresivo,
            verb_data.pret_imperfecto,
            verb_data.futuro_simple,
            verb_data.imperativo
        )
