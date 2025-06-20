from typing import List, Optional

from params import TensTranslationBase


def substitute(root: str, postfix: str | List[str], substitution: str) -> Optional[str]:
    postfixes = [postfix] if type(postfix) == str else postfix
    for p in postfixes:
        if root.endswith(p) and len(p) == len(root):
            return root[:-len(p)] + substitution
    else:
        return None

def substitute_end(root: str, postfix: str | List[str], substitution: str) -> Optional[str]:
    postfixes = [postfix] if type(postfix) == str else postfix
    for p in postfixes:
        if root.endswith(p) and len(p) < len(root):
            return root[:-len(p)] + substitution
    else:
        return None


def append(root: str, postfix: str | List[str], substitution: str) -> Optional[str]:
    postfixes = [postfix] if type(postfix) == str else postfix
    for p in postfixes:
        if root.endswith(p):
            return root + substitution
    else:
        return None


def self_ending(verb: str, translation_base: TensTranslationBase):
    match translation_base.zwrotny:
        case None:
            return ' się' if verb.endswith("se") else ''
        case True:
            return ' się'
        case False:
            return ''
        case _:
            raise Exception()