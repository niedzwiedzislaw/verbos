# This is a sample Python script.
from dataclasses import asdict

import pandas as pd

from data_extraction import extract


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    results = [
        extract("ir", 'być','był', 'byli', 'jest'),
        extract("ser", 'iść','szedł', 'szli', 'idzie'),
        extract("estar", 'być','był', 'byli', 'jest'),
        extract("dormir", 'spać','spał', 'spali', 'śpi'),
        extract("vestir", 'nosić','nosił', 'nosili', 'nosi'),
        extract("vestirse", 'ubierać się','ubiera', 'ubierał', 'ubierali'),
        extract("volver", 'wracać','wracał', 'wracali', 'wraca'),
        extract("comer", 'jeść','jadł', 'jedli', 'je'),
        extract("salir", 'wychodzić', 'wyszedł', 'wyszli', 'wyszedł'),
        extract("comprar", 'kupować','kupił', 'kupili', 'kupuje'),
        extract("limpiar", 'czyścić', 'czyścił', 'czyścili', 'czyści'),
        extract("preparar", 'przygotowywać','przygotował', 'przygotowali', 'przygotowuje'),
        extract("acabar", 'kończyć', 'skończył', 'skończyli', 'kończy'),
        extract("acostarse", 'położyć się', 'położył', 'położyli', 'kładzie'),
        extract("levantarse", 'wstać; obudzić się', 'wstał', 'wstali', 'wstaje'),
        extract("ver", 'oglądać','oglądał', 'oglądali', 'ogląda'),
        extract("empezar", 'zaczynać','zaczynał', 'zaczynali', 'zaczyna'),
        extract("escribir", 'pisać', 'pisał', 'pisali', 'pisze'),
        extract("despertarse", 'budzić się','budził', 'budzili', 'budzi'),
        extract("llamarse", 'nazywać się', 'nazywał', 'nazywali', 'nazywa'),
        extract("saber", 'myśleć', 'myślał', 'myśleli', 'myśli'),
        extract("conocer", 'znać', "znał", "znali", 'zna'),
        extract("lavarse", 'myć się',"", "", ''),
        extract("poder", 'móc',"", "", ''),
        extract("cerrar", 'zamykać',"", "", ''),
        extract("dar", 'dać', "dał", "dali", 'daje'),
        extract("repetir", 'powtarzać',"", "", ''),
        extract("pensar", 'myśleć',"", "", ''),
        extract("preferir", 'preferować', "", "", ''),
        extract("sentir", 'czuć',"", "", ''),
        extract("decir", 'mówić',"", "", ''),
        extract("preparar", 'przygotować',"", "", ''),
        extract("limpiar", 'myć',"", "", ''),
        extract("querer", 'chcieć',"chciał", "chcieli", 'chce'),
        extract("nacer", 'urodzić się',"rodził", "rodzili", 'rodzi'),
        extract("conseguir", 'zyskać',"zyskał", "zyskali", ''),
        extract("descubrir", 'odkryć',"odkrył", "odkryli", ''),
    ]

    new_words = pd.json_normalize([asdict(v) for v in results])
    new_words.set_index('infinitivo')
    # print('df')
    # print(type(df))
    # print(dir(df.columns))
    # print(df)

    with open("Spanish__verbos.txt", "r", encoding='utf-8') as f:
        existing_words = pd.read_csv(f, sep=',', header=None, names=new_words.columns, skip_blank_lines=True, dtype='str')
        existing_words.set_index('infinitivo')

    with open("Spanish__verbos__upd.csv", "w", encoding='utf-8') as f:
        print('existing_df')
        print(type(existing_words))
        print(existing_words)
        existing_words.update(new_words, join='left')
        # existing_df.merge(df, how='outer', on=['infinitivo'])
        print('merged')
        print(existing_words)
        # existing_words.to_csv(f, index=False, header=True, sep=',')
        new_words.to_csv(f, index=False, header=False, sep=',')
