from extractor import Tense
from params import TensTranslationBase
from translator import Translator, substitute, substitute_end, append, TranslatedTense, Translation
from translator.LetterUtils import self_ending


class IndefinidoTranslator:

    @staticmethod
    def translate_past_with_root(verb, trans: Tense, translation_base: TensTranslationBase) -> TranslatedTense:
        się = self_ending(verb, translation_base)
        root_sg = translation_base.singular
        root_pl = translation_base.plural or root_sg

        def sg_1():
            return root_sg + f"em" + się if root_sg else ''

        def sg_2():
            return root_sg + f"eś" + się if root_sg else ''

        def sg_3():
            match root_pl:
                case '':
                    return ''
                case _:
                    return (
                            substitute(root_sg, 'mogł', 'mógł') or
                            append(root_sg, '', '')
                    ) + się

        def pl_1():
            return root_pl + f"śmy" + się if root_pl else ''

        def pl_2():
            return root_pl + f"ście" + się if root_pl else ''

        def pl_3():
            return root_pl + f"" + się if root_pl else ''

        return TranslatedTense(
            yo=Translation(trans.yo.conjugation, sg_1(), trans.yo.irregular),
            tu=Translation(trans.tu.conjugation, sg_2(), trans.tu.irregular),
            el=Translation(trans.el.conjugation, sg_3(), trans.el.irregular),
            ns=Translation(trans.ns.conjugation, pl_1(), trans.ns.irregular),
            vs=Translation(trans.vs.conjugation, pl_2(), trans.vs.irregular),
            ellos=Translation(trans.ellos.conjugation, pl_3(), trans.ellos.irregular),
        )
