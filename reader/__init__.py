from dataclasses import dataclass, field


@dataclass
class TensTranslationBase:
    singular: str
    plural: str


@dataclass
class CsvInputRow:
    verb: str
    polski: str
    conj_root_past_sg: str = field(default='')
    conj_root_past_pl: str = field(default='')
    conj_root_present_sg: str = field(default='')
    conj_root_present_pl: str = field(default='')
    present: TensTranslationBase = field(init=False, repr=False)
    past: TensTranslationBase = field(init=False, repr=False)

    def __post_init__(self):
        self.conj_root_present_pl = self.conj_root_present_pl or self.conj_root_present_sg
        self.present = TensTranslationBase(self.conj_root_present_sg, self.conj_root_present_pl)
        self.past = TensTranslationBase(self.conj_root_past_sg, self.conj_root_past_pl)
