# This is a sample Python script.
import csv
import multiprocessing
import time
from concurrent.futures import ThreadPoolExecutor
from itertools import chain
from typing import Iterator, List, Iterable

from tqdm import tqdm

from anki import Card, tense_names, ListWriter, case_names, person_abbr_with_accents
from extractor.spanishdict import SpanishDictExtractor
from params import CsvInputRow
from translator import Translator, TranslatedVerbConjugation


def prepare_conjugation(row: list[str]) -> TranslatedVerbConjugation:
    params = CsvInputRow(*row)
    verb_data = SpanishDictExtractor.extract_verb_data(params.verb)
    return Translator.add_translations(verb_data, params.translation_params)



def main():
    with ThreadPoolExecutor(8) as p:
        with open('input/verbs.csv', encoding='utf-8') as f:
            rows = list(csv.reader(f, delimiter=',', quotechar='"'))
            results = tqdm(p.map(prepare_conjugation, rows), desc='Gathering data', total=len(rows))

        with(open('input/basic_verbs_filter.csv', 'r', encoding='utf-8')) as f:
            basic_infinitivos = [v.strip() for v in f.readlines()]


        card_factory = Card.create_card_factory(basic_infinitivos)
        cards: Iterable[Card] = tqdm(list(chain.from_iterable(p.map(card_factory, results))), desc='Creating cards')

        ListWriter.write_list('Spanish::conjugación::All verbs::all', cards, "update current")
        ListWriter.write_list('Spanish::conjugación::All verbs::irregulares', [card for card in cards if card.irregular], "keep both")
        ListWriter.filter_and_write_by_time(["yo", "tu", "el"], tense_names.keys(), cards, "keep both", "All verbs::")
        ListWriter.filter_and_write_by_time(["tu"], ["imperativo"], cards, "keep both", "All verbs::")


        basic_cards = [card for card in cards if Card.Tags.basic_verb in card.tags]
        prefix = "Basic verbs"
        ListWriter.write_infinitivos_list("Spanish::verbos", cards)
        ListWriter.write_list(f'Spanish::conjugación::{prefix}::all', basic_cards, "keep both")
        ListWriter.write_list(f'Spanish::conjugación::{prefix}::irregulares', [card for card in basic_cards if card.irregular],
                              "keep both")
        ListWriter.filter_and_write_by_time(["yo", "tu", "el"], tense_names.keys(), basic_cards, "keep both", f"{prefix}::")
        ListWriter.filter_and_write_by_time(["tu"], ["imperativo"], basic_cards, "keep both", f"{prefix}::")


    # new_words = pd.json_normalize([asdict(v) for v in results])
    # new_words.set_index('infinitivo')
    # # print('df')
    # # print(type(df))
    # # print(dir(df.columns))
    # # print(df)
    #
    # with open("Spanish__verbos.txt", "r", encoding='utf-8') as f:
    #     existing_words = pd.read_csv(f, sep=',', header=None, names=new_words.columns, skip_blank_lines=True, dtype='str')
    #     existing_words.set_index('infinitivo')
    #
    # with open("Spanish__verbos__upd.csv", "w", encoding='utf-8') as f:
    #     print('existing_df')
    #     print(type(existing_words))
    #     print(existing_words)
    #     existing_words.update(new_words, join='left')
    #     # existing_df.merge(df, how='outer', on=['infinitivo'])
    #     print('merged')
    #     print(existing_words)
    #     # existing_words.to_csv(f, index=False, header=True, sep=',')
    #     new_words.to_csv(f, index=False, header=False, sep=',')


if __name__ == '__main__':
    main()
