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
    list_result = list(collection.find({"name": name}, {"_id": 0}))
    if len(list_result) != 0:
        data = []
        for result in list_result:
            data.append(result)
        return data
    else:
        raise HTTPException(404, f"Couldn't find menu with name: {name}'")


@app.get("reservation/by-table/{table}")
def get_reservation_by_table(table: int):
    list_result = list(collection.find({"table_number": table}, {"_id": 0}))
    if len(list_result) != 0:
        data = []
        for result in list_result:
            data.append(result)
        return data
    else:
        raise HTTPException(404, f"Couldn't find menu with name: {table}'")


@app.post("/reservation")
def reserve(reservation: Reservation):
    find = collection.find_one({"time": reservation.time}, {"table_number": reservation.table_number})
    if find != None:
        return {
            "result": "Failed"
        }
    else:
        if reservation.table_number > 12:
            return {
                "result": "Failed"
            }
        else:
            res_encode = jsonable_encoder(reservation)
            collection.insert_one(res_encode)
            return {
                "result": "done"
            }


@app.put("/reservation/update/")
def update_reservation(reservation: Reservation):
    find = collection.find_one({"time": reservation.time}, {"table_number": reservation.table_number})
    if find == None:
        return {
            "result": "Failed"
        }
    else:
        new_value = {
            "$set": {"name": reservation.name, "time": reservation.time, "table_number": reservation.table_number}}
        collection.update_one(collection.find(), new_value)
        res_encode = jsonable_encoder(reservation)
        collection.update_one(res_encode)
        return {
            "result": "done"
        }


@app.delete("/reservation/delete/{name}/{table_number}")
def cancel_reservation(name: str, table_number: int):
    find = collection.find_one({"name": name, "table_number": table_number})
    if find == None:
        return {
            "result": "Failed"
        }
    else:
        collection.delete_one()
        return {
            "result": "done"
        }
