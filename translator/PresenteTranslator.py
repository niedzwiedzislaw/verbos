from extractor import Tense
from params import TensTranslationBase
from translator import substitute, substitute_end, append, TranslatedTense, Translation, Translator
from translator.LetterUtils import self_ending


class PresenteTranslator:

    @staticmethod
    def translate_present_with_root(verb: str, trans: Tense, translation_base: TensTranslationBase) -> TranslatedTense:
        się = self_ending(verb, translation_base)
        root_sg = translation_base.singular
        root_pl = translation_base.plural or translation_base.singular

        def persona_sg_1():
            match root_sg:
                case '':
                    return ''
                case _:
                    return (
                            substitute(root_sg, 'je', 'jem') or
                            substitute(root_sg, 'wie', 'wiem') or
                            substitute_end(root_sg, 'oże', 'ogę') or
                            substitute_end(root_sg, 'si', 'szę') or
                            substitute_end(root_sg, 'ści', 'szczę') or
                            substitute_end(root_sg, 'dzie', 'dę') or
                            substitute_end(root_sg, ['e', 'y'], 'ę') or
                            substitute_end(root_sg, 'bi', 'bię') or
                            substitute_end(root_sg, 'wi', 'wię') or
                            substitute_end(root_sg, 'pi', 'pię') or
                            substitute_end(root_sg, 'i', 'ę') or
                            append(root_sg, 'a', 'm') or
                            append(root_sg, '', 'em')
                    ) + się

        def persona_sg_2():

            match root_sg:
                case '':
                    return ''
                case _:
                    return (
                            substitute_end(root_sg, 'st', 'steś') or
                            append(root_sg, '', 'sz')
                    ) + się

        def persona_sg_3():
            match root_sg:
                case '':
                    return ''
                case x:
                    return x + się

        def persona_pl_1():
            match root_pl:
                case '':
                    return ''
                case x:
                    return x + "my" + się

        def persona_pl_2():
            match root_pl:
                case '':
                    return ''
                case _:
                    return (
                        append(root_pl, '', 'cie')
                    ) + się

        def persona_pl_3():
            match root_pl:
                case '':
                    return ''
                case _:
                    return (
                            substitute(root_pl, 'jesteś', 'są') or
                            substitute(root_pl, 'je', 'jedzą') or
                            substitute(root_pl, 'wie', 'wiedzą') or
                            substitute_end(root_pl, 'jest', 'są') or
                            substitute_end(root_pl, 'dzie', 'dą') or
                            substitute_end(root_pl, 'dzi', 'dzą') or
                            substitute_end(root_pl, 'si', 'szą') or
                            substitute_end(root_pl, 'da', 'dają') or
                            substitute_end(root_pl, 'je', 'ją') or
                            substitute_end(root_pl, 'e', 'ą') or
                            # substitute_end(root_pl, 'wa', 'wają') or
                            # substitute_end(root_pl, 'cza', 'czają') or
                            substitute_end(root_pl, 'a', 'ają') or
                            append(root_pl, '', 'ą')
                    ) + się

        return TranslatedTense(
            yo=Translation(trans.yo.conjugation, persona_sg_1(), trans.yo.irregular),
            tu=Translation(trans.tu.conjugation, persona_sg_2(), trans.tu.irregular),
            el=Translation(trans.el.conjugation, persona_sg_3(), trans.el.irregular),
            ns=Translation(trans.ns.conjugation, persona_pl_1(), trans.ns.irregular),
            vs=Translation(trans.vs.conjugation, persona_pl_2(), trans.vs.irregular),
            ellos=Translation(trans.ellos.conjugation, persona_pl_3(), trans.ellos.irregular),
        )
