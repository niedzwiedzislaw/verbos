# This is a sample Python script.
import csv

from streamable import Stream
from tqdm import tqdm

from extractor.spanishdict import SpanishDictExtractor
from anki import Card
from params import CsvInputRow
from settings import separator
from translator import Translator, TranslatedVerbConjugation


def prepare_conjugation(params: CsvInputRow) -> TranslatedVerbConjugation:
    verb_data = SpanishDictExtractor.extract_verb_data(params.verb)
    return Translator.add_translations(verb_data, params.translation_params)


def main():
    with open('input.csv', encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=',', quotechar='"')
        results = [prepare_conjugation(CsvInputRow(*row)) for row in tqdm(list(rows))]

    cards: Stream[Card] = Stream(lambda: results).map(Card.create_cards).flatten()
    with open('verbos_conjugacion.csv', 'w', encoding='utf-8') as f:
        f.write(f'#separator:{separator}' + '\n')
        f.write(f'#html:true' + '\n')
        f.write(f'#if matches:keep current' + '\n')
        f.write(f'#notetype:Spanish Conjugation' + '\n')
        f.write(f'#deck:Spanish::conjugación' + '\n')
        f.write('#columns:' + Card.get_headers() + '\n')
        w = csv.writer(f, delimiter=separator)
        for c in cards:
            w.writerow(c.values())

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
