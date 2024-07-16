from dataclasses import dataclass, field


@dataclass
class TensTranslationBase:
    singular: str
    plural: str


@dataclass
class TranslationParams:
    polski: str
    present: TensTranslationBase
    past: TensTranslationBase


@dataclass
class CsvInputRow:
    verb: str
    __polski: str
    __conj_root_past_sg: str = field(default='')
    __conj_root_past_pl: str = field(default='')
    __conj_root_present_sg: str = field(default='')
    __conj_root_present_pl: str = field(default='')
    translation_params: TranslationParams = field(init=False, repr=False)

    def __post_init__(self):
        self.conj_root_present_pl = self.__conj_root_present_pl or self.__conj_root_present_sg
        self.translation_params = TranslationParams(
            self.__polski,
            TensTranslationBase(self.__conj_root_present_sg, self.__conj_root_present_pl),
            TensTranslationBase(self.__conj_root_past_sg, self.__conj_root_past_pl)
        )
