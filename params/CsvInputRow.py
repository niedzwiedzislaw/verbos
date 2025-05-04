from dataclasses import dataclass, field
from typing import Optional
from unittest import case


@dataclass
class TensTranslationBase:
    singular: str
    plural: str
    zwrotny: Optional[bool]


@dataclass
class TranslationParams:
    polski: str
    present: TensTranslationBase
    past: TensTranslationBase

def str_to_bool(value: Optional[str]) -> Optional[bool]:
    match value.lower() if value else None:
        case None:
            return None
        case "true":
            return True
        case "false":
            return False
        case _:
            raise Exception(f"Unknown value {value}")


@dataclass
class CsvInputRow:
    verb: str
    __polski: str
    __conj_root_past_sg: str = field(default='')
    __conj_root_past_pl: str = field(default='')
    __conj_root_present_sg: str = field(default='')
    __conj_root_present_pl: str = field(default='')
    __zwrotny: Optional[bool] = field(default=None)
    translation_params: TranslationParams = field(init=False, repr=False)

    def __post_init__(self):
        self.__zwrotny = str_to_bool(self.__zwrotny)
        self.conj_root_present_pl = self.__conj_root_present_pl or self.__conj_root_present_sg
        self.translation_params = TranslationParams(
            self.__polski,
            TensTranslationBase(self.__conj_root_present_sg, self.__conj_root_present_pl, self.__zwrotny),
            TensTranslationBase(self.__conj_root_past_sg, self.__conj_root_past_pl, self.__zwrotny)
        )
