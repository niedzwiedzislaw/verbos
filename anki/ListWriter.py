import csv
from typing import List, Iterable

from anki import Card, person_abbr_with_accents, case_names
from settings import separator


class ListWriter:

    @staticmethod
    def filter_and_write_by_time(persons: List[str], times: List[str], cards: Iterable[Card], if_matches, prefx = ""):
        persons_names = ", ".join([person_abbr_with_accents[person] for person in persons])
        for t in times:
            deck_name = f'Spanish::conjugación::{prefx}{case_names[t]}: {persons_names}'
            ListWriter.write_list(deck_name, [card for card in cards if card.verify_type(persons, [t])], if_matches)

    @staticmethod
    def write_list(deck_name: str, cards: Iterable[Card], if_matches):
        with open("lists/" + ListWriter.__generate_file_name(deck_name), 'w', encoding='utf-8', newline='') as f:
            f.write(f'#separator:{separator}' + '\n')
            f.write(f'#html:true' + '\n')
            f.write(f'#if matches:{if_matches}' + '\n')
            f.write(f'#notetype:Spanish Conjugation' + '\n')
            f.write(f'#deck:{deck_name}' + '\n')
            f.write('#columns:' + Card.get_headers() + '\n')
            w = csv.writer(f, delimiter=separator)
            for c in cards:
                w.writerow(c.values())

    __update_modes = ["keep both", "keep current", "update current"]

    @staticmethod
    def __generate_file_name(deck_name: str) -> str:
        return (deck_name.removeprefix("Spanish::conjugación::")
                .replace('::', '; ')
                .replace(': ', ' - ') + ".csv")
