from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from server.database import (
    add_height_s3,
    add_predict_height,
    delete_height_s3,
    retrieve_height_s3,
    retrieve_heights_s3,
    update_height_s3,
)
from server.models.predict import (
    ErrorResponseModel,
    ResponseModel,
    HeightSchema,
    UpdateHeightModel,
)

router = APIRouter()

# @router.post("/", response_description="Height data from station 3 added into the database")
# async def add_height_data_s3(height_s3: HeightSchema = Body(...)):
#     height_s3 = jsonable_encoder(height_s3)
#     new_height_s3 = await add_height_s3(height_s3)
#     return ResponseModel(new_height_s3, "Height from station 3  added successfully.")

@router.post("/", response_description="Height data from station 3 added into the database")
async def add_height_data_s3(predict: HeightSchema = Body(...)):
    predict = await add_predict_height(predict)
    return ResponseModel(predict, "Predict hight added successfully.")

@router.get("/", response_description="Heights from station 3  retrieved")
async def get_heights_s3():
    heights_s3 = await retrieve_heights_s3()
    if heights_s3:
        return ResponseModel(heights_s3, "Heights data from station 3  retrieved successfully")
    return ResponseModel(heights_s3, "Empty list returned")


@router.get("/{id}", response_description="Height data from station 3  retrieved")
async def get_height_data_s3(id):
    height_s3 = await retrieve_height_s3(id)
    if height_s3:
        return ResponseModel(height_s3, "Height data from station 3  retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Student doesn't exist.")

@router.put("/{id}")
async def update_height_s3_data(id: str, req: UpdateHeightModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_height_s3 = await update_height_s3(id, req)
    if updated_height_s3:
        return ResponseModel(
            "Height with ID: {} name update is successful".format(id),
            "Height name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the height data.",
    )


@router.delete("/{id}", response_description="Height data from station 3  deleted from the database")
async def delete_height_s3_data(id: str):
    deleted_height_s3 = await delete_height_s3(id)
    if deleted_height_s3:
        return ResponseModel(
            "Height with ID: {} removed".format(id), "Height from station 3  deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Height with id {0} doesn't exist".format(id)
    )
