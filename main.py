from fastapi import FastAPI, Request, Response, Form, Cookie, Query, File, Header, UploadFile, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, PlainTextResponse, StreamingResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from jinja2 import environment
from fastapi.security import APIKeyCookie, OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBearer, OAuth2AuthorizationCodeBearer
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from typing import Callable, Iterator, Union, Optional, Annotated, List
import pandas as pd
import sqlite3
from datetime import datetime, timedelta, timezone
import aiosqlite
import json, re
from io import BytesIO, StringIO
from fastapi.middleware.wsgi import WSGIMiddleware
import uvicorn
from pathlib import Path
from pydantic import BaseModel
from enum import Enum


app = FastAPI()


origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
    "http://localhost:8050",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Non è necessario usare Pydantic con
# questa applicazione
#
# class dataset(BaseModel):
#     date: datetime
#     restaurant: str
#     planned_hours: float
#     actual_hours: float
#     budget: float
#     sells: float
#     hours: float
#     amount: float

class OrdName(str, Enum):
    desc = "DESC"
    asc = "ASC"


@app.post("/uploadfile/")
async def create_upload_file(request: Request, file: UploadFile):
    contents = await file.read()
    buffer = StringIO(contents.decode('utf-8'))
    df = pd.read_csv(buffer, dtype={'planned_hours':float, 'actual_hours':float, 'budget':float, 'sells':float})
    if df.columns[5]=='selles':
        names = ['date','restaurant','planned_hours','actual_hours','budget','sells']
        df = df[names]
    df['hours'] = df['planned_hours'] - df['actual_hours']
    df['amount'] = df['budget'] - df['sells']
    with sqlite3.connect('test_app.db') as conn:
        df.to_sql('ristoranti', conn, if_exists='replace')
    buffer.close()
    await file.close()
    return {"filename": file.filename}

@app.get("/ristoranti/{name}")
async def read_restaurant(name: str):
    with sqlite3.connect('test_app.db') as conn:
        df = pd.read_sql(f"SELECT * FROM ristoranti WHERE restaurant = '{name}'", conn)
    #return df.to_dict(orient='records')
    return Response(df.to_json(orient="records"), media_type="application/json")

@app.get("/ristoranti/{name}/{date}")
async def get_restaurant_by_date(
    name: str, 
    order_by: str,
    _ord: OrdName = OrdName.asc,
    date: str | None = None, 
    date__lte: str | None = None, 
    date__gte: str | None = None):
    with sqlite3.connect('test_app.db') as conn:
        if date and not(date__lte or date__gte):
            df = pd.read_sql(f"""SELECT date, restaurant, hours, amount, SUM(budget) AS totbudget, SUM(sells) AS totsells
                         FROM ristoranti WHERE restaurant = '{name}' AND date = '{date}' ORDER BY {order_by} {_ord} """, conn)
        elif date__lte and not(date or date__gte):
            df = pd.read_sql(f"""SELECT date, restaurant, hours, amount, SUM(budget) AS totbudget, SUM(sells) AS totsells
                         FROM ristoranti WHERE restaurant = '{name}' AND date <= '{date__lte}' ORDER BY {order_by} {_ord} """, conn)
        elif date__gte and not(date or date__lte):
            df = pd.read_sql(f"""SELECT date, restaurant, hours, amount, SUM(budget) AS totbudget, SUM(sells) AS totsells
                         FROM ristoranti WHERE restaurant = '{name}' AND date >= '{date__gte}' ORDER BY {order_by} {_ord}""", conn)
    return Response(df.to_json(orient="records"), media_type="application/json")


# Start the FastAPI server
if __name__ == "__main__":
    uvicorn.run(app)