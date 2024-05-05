# This is a sample Python script.
import sys
import csv
from dataclasses import dataclass, astuple, asdict, fields
from typing import List

import pandas as pd
import requests
from bs4 import BeautifulSoup

from data_extraction import extract
from model import *


def write_single_tense(t: TranslatedTense, verb, polish_root_sg, polish_root_pl, się):
    with open("Spanish__verbos__upd.txt", "a", encoding='utf-8') as f:
        f.write(f'{t[0]}	{verb}	yo	pretérito indefinido		{polish_root_sg}em{się}\n')
        f.write(f'{t[1]}	{verb}	tú	pretérito indefinido		{polish_root_sg}eś{się}\n')
        f.write(f'{t[2]}	{verb}	él / ella / usted	pretérito indefinido		{polish_root_sg}{się}\n')
        f.write(f'{t[3]}	{verb}	nosotros	pretérito indefinido		{polish_root_pl}śmy{się}\n')
        f.write(f'{t[4]}	{verb}	vosotros	pretérito indefinido		{polish_root_pl}ście{się}\n')
        f.write(f'{t[5]}	{verb}	ellos / ellas / ustedes	pretérito indefinido		{polish_root_pl}{się}\n')


def try_extract(verb, polish_root_sg='', polish_root_pl=''):
    try:
        return extract(verb, polish_root_sg, polish_root_pl)
    except:
        print(f"error when discovering verb {verb}")
        return None


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    results = [
        extract("ir", 'był', 'byli', 'jest'),
        extract("ser", 'szedł', 'szli', 'id'),
        extract("estar", 'był', 'byli', 'jest'),
        extract("dormir", 'spał', 'spali', 'śpi'),
        extract("vestir", 'nosił', 'nosili', 'nosi'),
        extract("vestirse", 'ubiera', 'ubierał', 'ubierali'),
        extract("volver", 'wracał', 'wracali', 'wraca'),
        extract("comer", 'jadł', 'jedli', 'je'),
        extract("salir", 'wyszedł', 'wyszli', 'wyszedł'),
        extract("comprar", 'kupił', 'kupili', 'kupuje'),
        extract("limpiar", 'czyścił', 'czyścili', 'czyści'),
        extract("preparar", 'przygotował', 'przygotowali', 'przygotowuje'),
        extract("acabar", 'skończył', 'skończyli', 'kończy'),
        extract("acostarse", 'położył', 'położyli', 'kładzie'),
        extract("levantarse", 'wstał', 'wstali', 'wstaje'),
        extract("ver", 'oglądał', 'oglądali', 'ogląda'),
        extract("empezar", 'zaczynał', 'zaczynali', 'zaczyna'),
        extract("escribir", 'pisał', 'pisali', 'pisze'),
        extract("despertarse", 'budził', 'budzili', 'budzi'),
        extract("llamarse", 'nazywał', 'nazywali', 'nazywa'),
        extract("saber", 'myślał', 'myśleli', 'myśli'),
        extract("vestirse", "", "", ''),
        extract("conocer", "znał", "znali", 'zna'),
        extract("lavarse", "", "", ''),
        extract("poder", "", "", ''),
        extract("cerrar", "", "", ''),
        extract("dar", "", "", ''),
        extract("repetir", "", "", ''),
        extract("pensar", "", "", ''),
        extract("preferir", "", "", ''),
        extract("sentir", "", "", ''),
        extract("querer", "chciał", "chcieli", 'chce'),
        extract("nacer", "rodził", "rodzili", 'rodzi'),
    ]

    df = pd.json_normalize([asdict(v) for v in results])
    df.set_index('infinitivo')

    with open("Spanish__verbos.txt", "r", encoding='utf-8') as f:
        # existing_df = pd.read_csv(f, sep=',', header=[0], skip_blank_lines=True)
        print(df.columns.names)
        existing_df = pd.read_csv(f, sep=',', header=None, names=df.columns.names, skip_blank_lines=True)

    with open("Spanish__verbos__upd.txt", "w", encoding='utf-8') as f:
        existing_df.set_index('infinitivo')
        print('df')
        print(type(df))
        print(df)
        print('existing_df')
        print(type(existing_df))
        print(existing_df)
        existing_df.update(df, join='left')
        # existing_df.merge(df, how='outer', on=['infinitivo'])
        print('merged')
        print(existing_df)
        existing_df.to_csv(f, index=False, header=True, sep=',')
