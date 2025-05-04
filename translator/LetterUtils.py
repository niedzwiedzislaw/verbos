from typing import List, Optional


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
