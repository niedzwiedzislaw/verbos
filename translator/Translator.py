from model import TranslatedTense, VerbData, TranslatedImperativo, Translation, Tense
from translator.LetterUtils import substitute, append


class Translator:

    @staticmethod
    def translate_present_with_root(verb: str, trans: Tense, root_sg: str, root_pl: str = None) -> TranslatedTense:
        się = ' się' if verb.endswith("se") else ''

        def persona_sg_1():
            return '' if root_sg == '' else (
                    substitute(root_sg, 'si', 'szę') or
                    substitute(root_sg, 'ści', 'szczę') or
                    substitute(root_sg, 'dzie', 'dę') or
                    substitute(root_sg, ['e', 'y'], 'ę') or
                    substitute(root_sg, 'bi', 'bię') or
                    substitute(root_sg, 'wi', 'wię') or
                    substitute(root_sg, 'i', 'ę') or
                    append(root_sg, 'a', 'm') or
                    append(root_sg, '', 'em')
            )

        def persona_sg_2():
            return '' if root_sg == '' else (
                    substitute(root_sg, 'st', 'steś') or
                    append(root_sg, '', 'sz')
            )

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
            return '' if root_sg == '' else (
                append(root_sg, '', 'cie')
            )

        def persona_pl_3():
            return '' if root_sg == '' else (
                    substitute(root_sg, 'jest', 'są') or
                    substitute(root_sg, 'dzie', 'dą') or
                    substitute(root_sg, 'dzi', 'dzą') or
                    substitute(root_sg, 'e', 'ą') or
                    append(root_sg, '', 'ą')
            )

        return TranslatedTense(
            yo=Translation(trans.yo.conjugation, persona_sg_1() + się, trans.yo.irregular),
            tu=Translation(trans.tu.conjugation, persona_sg_2() + się, trans.tu.irregular),
            el=Translation(trans.el.conjugation, persona_sg_3() + się, trans.el.irregular),
            ns=Translation(trans.ns.conjugation, persona_pl_1() + się, trans.ns.irregular),
            vs=Translation(trans.vs.conjugation, persona_pl_2() + się, trans.vs.irregular),
            ellos=Translation(trans.ellos.conjugation, persona_pl_3() + się, trans.ellos.irregular),
        )

    @staticmethod
    def translate_past_with_root(verb, trans: Tense, root_sg, root_pl: str = None) -> TranslatedTense:
        się = ' się' if verb.endswith("se") else ''
        root_pl = root_pl or root_sg

        def sg_1(): return root_sg + f"em{się}" if root_sg else ''

        def sg_2(): return root_sg + f"eś{się}" if root_sg else ''

        def sg_3(): return root_sg + f"{się}" if root_sg else ''

        def pl_1(): return root_pl + f"śmy{się}" if root_pl else ''

        def pl_2(): return root_pl + f"ście{się}" if root_pl else ''

        def pl_3(): return root_pl + f"{się}" if root_pl else ''

        return TranslatedTense(
            yo=Translation(trans.yo.conjugation, sg_1() + się, trans.yo.irregular),
            tu=Translation(trans.tu.conjugation, sg_2() + się, trans.tu.irregular),
            el=Translation(trans.el.conjugation, sg_3() + się, trans.el.irregular),
            ns=Translation(trans.ns.conjugation, pl_1() + się, trans.ns.irregular),
            vs=Translation(trans.vs.conjugation, pl_2() + się, trans.vs.irregular),
            ellos=Translation(trans.ellos.conjugation, pl_3() + się, trans.ellos.irregular),
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
