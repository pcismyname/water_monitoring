from fastapi import FastAPI

from server.routes.water import router as WaterRouter
from server.mqtt.sensor_data import router as MqttRouter
from server.routes.predict import router as PredictRouter

app = FastAPI()

####router api part

app.include_router(MqttRouter, tags=["MQTT"],prefix="/mqtt")
app.include_router(WaterRouter, tags=["Height_S1"], prefix="/height")
app.include_router(PredictRouter, tags=["Height_S3"], prefix="/predict")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "My REST API server!"}