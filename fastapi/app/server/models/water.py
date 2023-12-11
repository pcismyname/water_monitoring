from typing import Optional , List
from pydantic import BaseModel, Field
from datetime import datetime


class HeightSchema(BaseModel):
    height: List[float]
    class Config:
        schema_extra = {
            "example": {
                "height":[121.1, 130.2, 125.5]
            }
        }

class UpdateHeightModel(BaseModel):
    height: Optional[float]
    class Config:
        schema_extra = {
            "example": {
                "height":[121.1, 130.2, 125.5]
            }
        }

def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}


