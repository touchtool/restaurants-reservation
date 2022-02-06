from pymongo import MongoClient

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from fastapi.encoders import jsonable_encoder


class Reservation(BaseModel):
    name: str
    time: int
    table_number: int


client = MongoClient('mongodb://localhost', 27017)

db = client["touch_restaurant"]

collection = db["reservation"]

app = FastAPI()


@app.get("/reservation/by-name/{name}")
def get_reservation_by_name(name: str):
    result = collection.find({"name": name})
    my_result = [r for r in result]
    return {
        "result": my_result
    }


@app.get("reservation/by-table/{table}")
def get_reservation_by_table(table: int):
    result = collection.find({"table_number": table})
    my_result = [r for r in result]
    return {
        "result": my_result
    }


# @app.post("/reservation")
# def reserve(reservation: Reservation):
#     if reservation["table_number"] in collection.find({"table_number": reservation["table_number"]})


@app.put("/reservation/update/")
def update_reservation(reservation: Reservation):
    pass


@app.delete("/reservation/delete/{name}/{table_number}")
def cancel_reservation(name: str, table_number: int):
    pass
