import motor.motor_asyncio
from bson.objectid import ObjectId
from server.models.predict import HeightSchema

MONGO_DETAILS = "mongodb://tesarally:contestor@mongoDB:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.water_data


sensor_collection = database.get_collection("sensor_collection")
height_collection = database.get_collection("height_collection")
height_s3_collection = database.get_collection("height_s3_collection")
predict_collection = database.get_collection("predict_data")


def height_helper(height) -> dict:
    return {
        "id" : str(height["_id"]),
        "height" : height["height"]
    }

# Retrieve all height data present in the database
async def retrieve_heights():
    heights = []
    async for height in height_collection.find():
        heights.append(height_helper(height))
    return heights

async def retrieve_last_five_heights():
    heights = []
    async for height in height_collection.find().sort("_id", 1).limit(5):
        heights.append(height_helper(height))
    return heights

# Retrieve a height data with a matching ID
async def retrieve_height(id: str) -> dict:
    height = await height_collection.find_one({"_id": ObjectId(id)})
    if height:
        return height_helper(height)

# Add a new height data  into to the database
# async def add_height(height_data: dict) -> dict:
#     height = await height_collection.insert_one(height_data)
#     new_height = await height_collection.find_one({"_id": height.inserted_id})
#     return height_helper(new_height)

async def add_height(height_data: HeightSchema) -> dict:
    for h in height_data.height:
        data_to_insert = {
            "height": h
        }
        await height_s3_collection.insert_one(data_to_insert)
    
    # Retrieve the newly inserted data (you may choose to return something else)
    new_height = await height_s3_collection.find_one({"height": height_data.height[-1]})
    return height_helper(new_height)


# Update a height of water with a matching ID
async def update_height(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    height = await height_collection.find_one({"_id": ObjectId(id)})
    if height:
        updated_height = await height_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_height:
            return True
        return False

# Delete height of water from the database
async def delete_height(id: str):
    height = await height_collection.find_one({"_id": ObjectId(id)})
    if height:
        await height_collection.delete_one({"_id": ObjectId(id)})
        return True

## MATLAB

def height_s3_helper(height) -> dict:
    return {
        "id" : str(height["_id"]),
        "height" : height["height"]
    }

# Retrieve all height data present in the database 
async def retrieve_heights_s3():
    heights_s3 = []
    async for height in height_s3_collection.find():
        heights_s3.append(height_s3_helper(height))
    return heights_s3

# Retrieve a height data with a matching ID 
async def retrieve_height_s3(id: str) -> dict:
    height_s3 = await height_s3_collection.find_one({"_id": ObjectId(id)})
    if height_s3:
        return height_s3_helper(height_s3)

# Add a new height data  into to the database
async def add_height_s3(height_data: HeightSchema) -> dict:
    for h in height_data.height:
        data_to_insert = {
            # "date": height_data.date,
            "height": h
        }
        await height_s3_collection.insert_one(data_to_insert)
    
    # Retrieve the newly inserted data (you may choose to return something else)
    new_height_s3 = await height_s3_collection.find_one({"height": height_data.height[-1]})
    return height_s3_helper(new_height_s3)


# Update a height of water with a matching ID
async def update_height_s3(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    height_s3 = await height_s3_collection.find_one({"_id": ObjectId(id)})
    if height_s3:
        updated_height_s3 = await height_s3_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_height_s3:
            return True
        return False

# Delete height of water from the database
async def delete_height_s3(id: str):
    height_s3 = await height_s3_collection.find_one({"_id": ObjectId(id)})
    if height_s3:
        await height_s3_collection.delete_one({"_id": ObjectId(id)})
        return True
    

#add data to database
async def add_predict_height(height_data: HeightSchema) -> dict:
    for h in height_data.height:
        data_to_insert = {
            # "date": height_data.date,
            "height": h
        }
        await predict_collection.insert_one(data_to_insert)
    
    # Retrieve the newly inserted data (you may choose to return something else)
    new_height_s3 = await predict_collection.find_one({"height": height_data.height[-1]})
    return height_s3_helper(new_height_s3)

