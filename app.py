from fastapi import FastAPI
from pydantic import BaseModel
import gpsd  

app = FastAPI()

class GPSData(BaseModel):
    code: str  #codigo do gps

#banco de dados temporario tbm
db = {}

def decode_gps(code):
    gpsd.connect()  #conecta servidor
    packet = gpsd.get_current()  #obetem a parada la gps
    return {
        "Lat": packet.lat,
        "Lon": packet.lon,
        "Vel": f"{packet.hspeed} km/h",
        "Alt": f"{packet.alt} m"
    }

#receber o codigo gps
@app.put("/gps/")
async def update_gps(data: GPSData):
    decoded_data = decode_gps(data.code)  #decode
    db["gps_data"] = decoded_data  #armazem temporario tbm 
    return {"message": "GPS data updated", "data": decoded_data}

@app.get("/gps/")
async def get_gps():
    if "gps_data" in db:
        return {"message": "GPS data retrieved", "data": db["gps_data"]}
    return {"message": "deu merda"}
