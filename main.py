# This is a sample Python script.
import csv
from dataclasses import asdict

from streamable import Stream

from extractor.ellaverbs import Extractor
from extractor.spanishdict import SpanishDictExtractor
from model import create_cards, Card
from reader import CsvInputRow

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    with open('input.csv', encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=',', quotechar='"')
        results = [SpanishDictExtractor.extract_with_translation(CsvInputRow(*row)) for row in rows]

    cards: Stream[Card] = Stream(lambda: results).map(create_cards).flatten()
    with open('verbos_conjugacion.csv', 'w', encoding='utf-8') as f:
        f.write('#separator:;' + '\n')
        f.write('#columns:' + Card.get_headers() + '\n')
        for c in cards:
            f.write(c.to_line() + '\n')

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
