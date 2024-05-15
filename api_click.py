#!/usr/bin/python3
# -*- coding: utf-8 -*-
import click
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from pathlib import Path
import sqlite3

# questo programma non lancia la seguente funzione che quindi va eseguita manualmente
def init_db():
    date_today = datetime.now()
    days = pd.date_range(date_today, date_today + timedelta(9), freq='D')
    df = pd.DataFrame(np.random.randint(0,100,size=(100, 4)), columns=['planned_hours','actual_hours', 'budget','sales'])
    df2 = pd.DataFrame({'date': days, 'ristorante': range(1,11)})
    df3 = pd.concat([df2]*10, ignore_index=True)
    df4 = pd.concat([df3,df],axis=1)
    dir = Path.cwd()
    df4.to_csv(dir/'init_db.csv', index=False)

# gruppo per eventuali sviluppi futuri
@click.group()
def cli():
    pass

# opzioni base ma si potrebbero implementare tutte quelle di pd.read_csv()
@click.command()
@click.argument('filename', required=False)
@click.option('--sep')
def upload(filename, sep):
    """
    Importa il file csv in sqlite. Il nome del file è opzionale, se non specificato 
    il programma caricherà il file 'dataset.csv' in sqlite. NON indicare l'estensione del file.
    Il separatore è opzionale e serve per il file di output, se non specificato il programma utilizzerà il separatore di default della libreria pandas.
    """
    if not filename:
        filename = 'dataset'
    else:
        filename = filename
    if not sep:
        sep = ','
    df = pd.read_csv(f'{filename}.csv')
    df['hours'] = df['planned_hours'] - df['actual_hours']
    df['amount'] = df['budget'] - df['selles']
    with sqlite3.connect('test_app.db') as conn:
        df.to_sql('ristoranti_da console', conn, if_exists='replace')
    df.to_csv('dataset_output.csv', sep=sep, index=False)
    return None

    
cli.add_command(upload)

if __name__ == '__main__':
    cli()

