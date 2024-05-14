#!/usr/bin/python3
# -*- coding: utf-8 -*-
import click
from datetime import datetime
import pandas as pd
import numpy as np
from pathlib import Path

# questo programma non lancia la seguente funzione che quindi va eseguita manualmente
def init_db():
    df = pd.DataFrame(np.random.randint(0,100,size=(100, 6)), columns=['data','ristorante','planned_hours','actual_hours', 'budget','sales'])
    dir = Path.cwd()
    df.to_csv(dir/'init_db.csv', index=False)

# gruppo per eventuali sviluppi futuri
@click.group()
def cli():
    pass

# opzioni base ma si potrebbero implementare tutte quelle di pd.read_csv()
@click.command()
@click.argument('filename', required=False)
@click.option('--sep')
@click.option('--dir')
def upload(filename, sep, dir):
    """
    Importa il file csv sulla directory scelta. Il nome del file è opzionale, se non specificato 
    il programma caricherà il file 'db_caricato.csv' nella directory corrente. NON indicare l'estensione del file.
    Il separatore è opzionale, se non specificato il programma utilizzerà il separatore di default della libreria pandas.
    """
    if not filename:
        filename = 'db_caricato'
    else:
        filename = filename
    if not dir:
        dir = Path.cwd()
    else:
        Path(dir).mkdir(parents=True, exist_ok=True)
    if not sep:
        sep = ','
    df = pd.read_csv('init_db.csv')
    df['hours'] = df['planned_hours'] - df['actual_hours']
    df['amount'] = df['budget'] - df['sales']
    df.to_csv(f'{dir}/{filename}.csv', sep=sep, index=False)
    return None

    
cli.add_command(upload)

if __name__ == '__main__':
    cli()

