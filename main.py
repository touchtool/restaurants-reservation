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
    result = collection.find_one({"name": name}, {"_id": 0})
    if result != None:
        return {
            "status": "found",
            "result": result
        }
    else:
        raise HTTPException(404, f"Couldn't find menu with name: {name}'")


@app.get("reservation/by-table/{table}")
def get_reservation_by_table(table: int):
    result = collection.find_one({"table_number": table}, {"_id": 0})
    if result != None:
        return {
            "status": "found",
            "result": result
        }
    else:
        raise HTTPException(404, f"Couldn't find menu with name: {table}'")


@app.post("/reservation")
def reserve(reservation: Reservation):
    res_encode = jsonable_encoder(reservation)
    collection.insert_one(res_encode)
    return {
        "result": "done"
    }


@app.put("/reservation/update/")
def update_reservation(reservation: Reservation):
    res_encode = jsonable_encoder(reservation)
    collection.update_one(res_encode)
    return {
        "result": "done"
    }


@app.delete("/reservation/delete/{name}/{table_number}")
def cancel_reservation(name: str, table_number: int):
    result = collection.find({"name": name, "table_number": table_number})
    collection.delete_one(result)
    return {
        "result": "done"
    }
