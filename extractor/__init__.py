from model import Verb
from reader import CsvInputRow


class BaseExtractor:
    @staticmethod
    def extract_with_translation(input_data: CsvInputRow) -> Verb:
        pass
