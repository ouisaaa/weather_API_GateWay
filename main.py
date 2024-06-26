from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from config import Config

#실행: uvicorn main:app --port 5000
app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 Origin 허용, 필요에 따라 원하는 Origin을 명시할 수 있습니다.
    #allow_credentials=True, #자격증명 사용여부
    allow_methods=["GET"],
    allow_headers=["*"],
)


config=Config()
#
# @app.get("/")
# async def read_root():
#     return"This is root path from MyAPI"

import httpx
import asyncio
from datetime import datetime, timedelta

@app.get("/getCurrent")
async def request_location(x: float=130,y: float=63):
    async with httpx.AsyncClient() as client:
        response = await client.get(f'{config.DATA_DOMAIN}:4001/location?x={x}&y={y}')
        return response.json()

@app.get("/getSrtFcst")
async def request_SrtFcst(city: str,district: str,neighborhood: str):
    today = datetime.today()
    formatted_date = today.strftime('%Y%m%d')

    now = datetime.now()
    current_time = now.hour

    if now.minute < 30:
        current_time -= 1

    if (int(current_time) < 10):
        current_time = str("0" + str(current_time))

    async with httpx.AsyncClient() as client:
        response = await client.get(f'{config.DATA_DOMAIN}:4002/weather/getUltraSrtFcst?city={city}&district={district}&neighborhood={neighborhood}&nowDate={formatted_date}&nowTime={str(current_time)+"30"}')
        return response.json()

@app.get("/getSrtNcst")
async def request_SrtNcst(city: str,district: str,neighborhood: str):
    today = datetime.today()
    formatted_date = today.strftime('%Y%m%d')

    now = datetime.now()
    current_time = now.hour

    if now.minute < 30:
        current_time -= 1

    if (int(current_time)<10):
        current_time = str("0"+str(current_time))

    async with httpx.AsyncClient() as client:
        response = await client.get(f'{config.DATA_DOMAIN}:4003/weather/getSrtNcst?city={city}&district={district}&neighborhood={neighborhood}&nowDate={formatted_date}&nowTime={str(current_time)+"00"}')
        return response.json()

import logging
@app.get("/getVliageFcst")
async def request_VliageFcst(city: str,district: str,neighborhood: str):
    today= datetime.today()
    formatted_date = today.strftime('%Y%m%d')

    direction=[2,5,8,11,14,17,20,23]

    now = datetime.now()
    current_time = now.hour
    temp_time = current_time

    if current_time < 2:
        delta = timedelta(days=1)
        temp_date= today-delta
        formatted_date=temp_date.strftime('%Y%m%d')
        temp_time=str(direction[-1])
    else:
        for i in direction:
            if(i<current_time):
                temp_time=str(i)
                continue
            elif i==current_time and now.minute>10:
                temp_time = str(i)
                continue
            else:
                break

    async with httpx.AsyncClient() as client:
        response = await client.get(f'{config.DATA_DOMAIN}:4004/weather/getVliageFcst?city={city}&district={district}&neighborhood={neighborhood}&nowDate={formatted_date}&nowTime={temp_time+"00"}')
        return response.json()

@app.get("/districtList")
async def request_dis(city: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f'{config.DATA_DOMAIN}:4005/weather/districtList?city={city}')
        temp=response.text[1:-1].split(", ") #리스트 형태로 데이터를 전송
        temp[0]="-"
        return temp

@app.get("/neighborhoodList")
async def request_nei(dis: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f'{config.DATA_DOMAIN}:4005/weather/neighborhoodList?district={dis}')
        temp = response.text[1:-1].split(", ")  # 리스트 형태로 데이터를 전송
        temp[0] = "-"
        return temp

@app.get("/CtprvnRltmMesureDnsty")
async def request_CRMD(city: str, nei: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f'{config.DATA_DOMAIN}:4006/CtprvnRltmMesureDnsty?city={city}&nei={nei}')
        return response.json()

@app.get("/CtprvnRltmMesureDnsty/total")
async def request_CRMD_total(city: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f'{config.DATA_DOMAIN}:4006/CtprvnRltmMesureDnsty/total?city={city}')
        return response.json()