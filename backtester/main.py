# start service
# required - price port, action port, starting account value, fees type, times repeat, timeframe, ticker
# make sure ticker is supported on both price and action signal
# get prices for this timerange
# get expected input for action (optional for now)
# get actions for each price
# store and calculate results




# TODO: doesnt have swagger, check the other websockets that Kamil send, if its available with swagger, because in nest i think there is swagger for all ports, including websocket




# start
# check progress on one running
# run in past, or keep running in real time

import json
from typing import TypedDict, List, Optional

from fastapi import FastAPI, WebSocket
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from env_loader import load_env
env = load_env(".")
PORT = env.get("PORT")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[f"http://localhost:{PORT}"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


@app.websocket("/history")
async def get_history_params(websocket: WebSocket):
    # get history of all backtests items
    pass


@app.websocket("/history/{timestamp}")
async def get_specific_history_param(websocket: WebSocket, timestamp: int):
    # get one specific run from history (with status)
    pass

@app.websocket("/run")
async def start(websocket: WebSocket):
    
    class Params(TypedDict):
        asset: str
        interval: str
        timeframe_min: int
        timeframe_max: int
        action_probability: List[int]
        fee_fixed: Optional[int]
        fee_minimum: Optional[int]
        fee_percent: Optional[int]
    
    with await websocket.accept():
        params = await websocket.receive_text()
        params: Params = json.loads(params, object_hook=lambda x: Params(**x))
        print(params.asset)
