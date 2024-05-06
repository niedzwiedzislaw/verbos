from typing import List, Optional

from model import Translation, TranslatedTense


def translate_present_with_root(verb: str, trans, root_sg: str, root_pl: str) -> TranslatedTense:
    się = ' się' if verb.endswith("se") else ''

    def substitute(root: str, postfix: str | List[str], substitution: str) -> Optional[str]:
        postfixes = [postfix] if type(postfix) == str else postfix
        for p in postfixes:
            if root.endswith(p):
                return root[:-len(p)] + substitution + się
        else:
            return None

    def append(root: str, postfix: str | List[str], substitution: str) -> Optional[str]:
        postfixes = [postfix] if type(postfix) == str else postfix
        for p in postfixes:
            if root.endswith(p):
                return root + substitution + się
        else:
            return None

    def persona_sg_1():
        return '' if root_sg == '' else (
                substitute(root_sg, 'si', 'szę') or
                substitute(root_sg, 'ści', 'szczę') or
                substitute(root_sg, ['e', 'y'], 'ę') or
                substitute(root_sg, 'dzie', 'dę') or
                substitute(root_sg, 'i', 'ię') or
                append(root_sg, 'a', 'm') or
                append(root_sg, '', 'em')
        )

    def persona_sg_2():
        match root_sg:
            case '':
                return ''
            case x:
                return x + "sz" + się

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
            case x:
                return x + "cie" + się

    def persona_pl_3():
        match root_sg:
            case '':
                return ''
            case r if root_sg.endswith('e'):  # sieje
                return root_sg[:-1] + 'ą' + się
            case x:
                return x + się

    return TranslatedTense(
        yo=Translation(trans.yo, persona_sg_1()),
        tu=Translation(trans.tu, persona_sg_2()),
        el=Translation(trans.el, persona_sg_3()),
        ns=Translation(trans.ns, persona_pl_1()),
        vs=Translation(trans.vs, persona_pl_2()),
        ellos=Translation(trans.ellos, persona_pl_3()),
    )


def translate_past_with_root(verb, trans, root_sg, root_pl) -> TranslatedTense:
    się = ' się' if verb.endswith("se") else ''

    def sg_1(): return root_sg + f"em{się}" if root_sg else ''
    def sg_2(): return root_sg + f"eś{się}" if root_sg else ''
    def sg_3(): return root_sg + f"{się}" if root_sg else ''
    def pl_1(): return root_sg + f"śmy{się}" if root_sg else ''
    def pl_2(): return root_sg + f"ście{się}" if root_sg else ''
    def pl_3(): return root_sg + f"{się}" if root_sg else ''

    return TranslatedTense(
        yo=Translation(trans.yo, pl_1()),
        tu=Translation(trans.tu, pl_2()),
        el=Translation(trans.el, pl_3()),
        ns=Translation(trans.ns, pl_1()),
        vs=Translation(trans.vs, pl_2()),
        ellos=Translation(trans.ellos, pl_3()),
    )
