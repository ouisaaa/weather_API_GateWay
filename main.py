from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

#
# @app.get("/")
# async def read_root():
#     return"This is root path from MyAPI"

import httpx
import asyncio

@app.get("/getCurrent")
async def request_location(x: float=130,y: float=63):
    async with httpx.AsyncClient() as client:
        response = await client.get('http://localhost:3030/location?x={x}&y={y}')
        return response.json()

@app.get("/getSrtFcst")
async def request_SrtFcst(city: str,district: str,neighborhood: str):
    response = await client.get(f'http://localhost:4001/weather/getUltraSrtFcst?city={city}&district={district}&neighborhood={neighborhood}')
    return response.json()

@app.get("/getSrtNcst")
async def request_SrtFcst(city: str,district: str,neighborhood: str):
    response = await client.get(f'http://localhost:4002/weather/getSrtNcst?city={city}&district={district}&neighborhood={neighborhood}')
    return response.json()

@app.get("/getVliageFcst")
async def request_VliageFcst(city: str,district: str,neighborhood: str):
    response = await client.get(f'http://localhost:4003/weather/getVliageFcst?city={city}&district={district}&neighborhood={neighborhood}')
    return response.json()