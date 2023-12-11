from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from server.database import (
    add_height,
    delete_height,
    retrieve_height,
    retrieve_heights,
    retrieve_last_five_heights,
    update_height
)
from server.models.water import (
    ErrorResponseModel,
    ResponseModel,
    HeightSchema,
    UpdateHeightModel,
)

router = APIRouter()

# @router.post("/", response_description="Height data added into the database")
# async def add_height_data(height: HeightSchema = Body(...)):
#     height = jsonable_encoder(height)
#     new_height = await add_height(height)
#     return ResponseModel(new_height, "Height added successfully.")

@router.post("/", response_description="Height data from station 1 added into the database")
async def add_height_data(height: HeightSchema = Body(...)):
    new_height = await add_height(height)
    return ResponseModel(new_height, "Height from station 1 added successfully.")


@router.get("/", response_description="Heights retrieved")
async def get_heights():
    heights = await retrieve_last_five_heights()
    if heights:
        return ResponseModel(heights, "Heights data  retrieved successfully")
    return ResponseModel(heights, "Empty list returned")


@router.get("/{id}", response_description="Height data retrieved")
async def get_height_data(id):
    height = await retrieve_height(id)
    if height:
        return ResponseModel(height, "Height data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Student doesn't exist.")

@router.put("/{id}")
async def update_height_data(id: str, req: UpdateHeightModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_height = await update_height(id, req)
    if updated_height:
        return ResponseModel(
            "Height with ID: {} name update is successful".format(id),
            "Height name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the height data.",
    )


@router.delete("/{id}", response_description="Height data deleted from the database")
async def delete_height_data(id: str):
    deleted_height = await delete_height(id)
    if deleted_height:
        return ResponseModel(
            "Height with ID: {} removed".format(id), "Height deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Height with id {0} doesn't exist".format(id)
    )
