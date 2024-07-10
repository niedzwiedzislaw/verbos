from model import Verb
from reader import CsvInputRow


class BaseExtractor:
    @classmethod
    def extract_with_translation(cls, input_data: CsvInputRow) -> Verb:
        pass
