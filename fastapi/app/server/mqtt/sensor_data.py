from fastapi import APIRouter 
#fastapi_mqtt
from fastapi_mqtt.fastmqtt import FastMQTT
from fastapi_mqtt.config import MQTTConfig
from pymongo import MongoClient
from datetime import datetime

mqtt_config = MQTTConfig(host = "192.168.1.2",
    port= 1883,
    keepalive = 60,
    username="TGR_GROUP37",
    password="ZM973R")

fast_mqtt = FastMQTT(config=mqtt_config)

router = APIRouter()

fast_mqtt.init_app(router)

from server.models.water import (
    ErrorResponseModel,
    ResponseModel,
    HeightSchema,
)

@fast_mqtt.on_connect()
def connect(client, flags, rc, properties):
    fast_mqtt.client.subscribe("/tgr2023/Vertiz/#") #subscribing mqtt topic
    print("Connected: ", client, flags, rc, properties)

@fast_mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    print("Received message: ",topic, payload.decode(), qos, properties)
    


@fast_mqtt.subscribe("my/tgr2023/Vertiz/topic/#")
async def message_to_topic(client, topic, payload, qos, properties):
    print("Received message to specific topic: ", topic, payload.decode(), qos, properties)

@fast_mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    print("Disconnected")

@fast_mqtt.on_subscribe()
def subscribe(client, mid, qos, properties):
    print("subscribed", client, mid, qos, properties)

@router.get("/", response_description="test publish to mqtt")
async def publish_hello():
    fast_mqtt.publish("/tgr2023/Vertiz", "Hello from tgr2023_37_Vertiz") #publishing mqtt topic
    return {"result": True,"message":"Published" }


