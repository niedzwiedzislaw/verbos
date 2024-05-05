from model import Translation, TranslatedTense


def translate_present_with_root(verb: str, trans, root_sg: str, root_pl: str) -> TranslatedTense:
    def persona_pl_1():
        match root_sg:
            case r if root_sg.endswith('e'):  # sieje
                return root_sg[:-1] + 'ę'
            case r if root_sg.endswith('y'):  # kończy
                return root_sg[:-1] + 'ę'
            case r if root_sg.endswith('a'):  # zna
                return root_sg + 'm'
            case r if root_sg.endswith('si'):  # nosi
                return root_sg[:-2] + 'szę'
            case r if root_sg.endswith('i'):  # śpi
                return root_sg[:-1] + 'ę'
            case r if root_sg.endswith('ści'):  # czyści
                return root_sg[:-3] + 'szczę'
            case r if root_sg.endswith('dzie'):  # kładzie
                return root_sg[:-4] + 'dę'
            case r:
                return root_sg + "em"

    się = ' się' if verb.endswith("se") else ''
    return TranslatedTense(
        yo=Translation(trans.yo, f"{persona_pl_1()}{się}"),
        tu=Translation(trans.tu, root_sg + f"sz{się}"),
        el=Translation(trans.el, root_sg + f"{się}"),
        ns=Translation(trans.ns, root_pl + f"my{się}"),
        vs=Translation(trans.vs, root_pl + f"cie{się}"),
        ellos=Translation(trans.ellos, root_pl + f"ą{się}"),
    )


def translate_past_with_root(verb, trans, root_sg, root_pl) -> TranslatedTense:
    się = ' się' if verb.endswith("se") else ''
    return TranslatedTense(
        yo=Translation(trans.yo, root_sg + f"em{się}"),
        tu=Translation(trans.tu, root_sg + f"eś{się}"),
        el=Translation(trans.el, root_sg + f"{się}"),
        ns=Translation(trans.ns, root_pl + f"śmy{się}"),
        vs=Translation(trans.vs, root_pl + f"ście{się}"),
        ellos=Translation(trans.ellos, root_pl + f"{się}"),
    )
