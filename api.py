from init_db import init_database
from fastapi import FastAPI, HTTPException, Depends, Query, Body
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from bson import ObjectId
from typing import List
from models import Category, Part
from bson.errors import InvalidId
import os
from dotenv import load_dotenv
from bson import json_util
import json
app = FastAPI()

# Load .env file
load_dotenv()

# Run the initialization script
init_database()

# Configuration variables
mongo_url = os.getenv('MONGO_URL')
database_name = "armin_bolen"
client = AsyncIOMotorClient(mongo_url, uuidRepresentation="standard")
database = client[database_name]


# Middleware for database management
async def get_database():
    yield database


@app.post("/categories/", tags=["Categories"], response_model=Category, response_model_by_alias=False)
async def create_category(category: Category, db: AsyncIOMotorDatabase = Depends(get_database)):
    category_data = category.model_dump(by_alias=True, exclude=["id"])
    result = await db.categories.insert_one(category_data)

    created_category = await db.categories.find_one({"_id": result.inserted_id})
    return created_category


@app.get("/categories/", tags=["Categories"], response_model=List[Category], response_model_by_alias=False)
async def read_categories(db: AsyncIOMotorDatabase = Depends(get_database)):
    categories = await db.categories.find().to_list(length=None)
    return categories


@app.get("/categories/{category_id}", tags=["Categories"], response_model=Category, response_model_by_alias=False)
async def read_category(category_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    try:
        category = await db.categories.find_one({"_id": ObjectId(category_id)})
        if category:
            return category
        else:
            raise HTTPException(status_code=404, detail="Category not found")
    except InvalidId:
        raise HTTPException(status_code=422, detail="Invalid category_id format")


@app.put("/categories/{category_id}", tags=["Categories"], response_model=Category, response_model_by_alias=False)
async def update_category(category_id: str, category: Category, db: AsyncIOMotorDatabase = Depends(get_database)):
    try:
        category_data = dict(category)
        category_data.pop("id", None)

        result = await db.categories.update_one(
            {"_id": ObjectId(category_id)},
            {"$set": category_data}
        )

        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Category not found")

        return await db.categories.find_one({"_id": ObjectId(category_id)})

    except InvalidId:
        raise HTTPException(status_code=422, detail="Invalid category_id format")


@app.delete("/categories/{category_id}", tags=["Categories"], response_model=Category, response_model_by_alias=False)
async def delete_category(category_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    # Get category data based on category_id
    try:
        category = await db.categories.find_one({"_id": ObjectId(category_id)})
    except InvalidId:
        raise HTTPException(status_code=422, detail="Invalid category_id format")

    # Check if the category exists
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    # Check if there are parts assigned to this category
    parts_count = await db.parts.count_documents({"category": category["name"]})
    if parts_count > 0:
        raise HTTPException(status_code=400, detail="Cannot delete category with assigned parts")

    # Check if there are child categories with assigned parts
    child_categories = await db.categories.find({"parent_name": category["name"]}).to_list(length=None)
    for child_category in child_categories:
        child_parts_count = await db.parts.count_documents({"category": str(child_category["name"])})
        if child_parts_count > 0:
            raise HTTPException(status_code=400, detail="Cannot delete category with child categories having assigned parts")

    # Delete category
    deleted_category = await db.categories.find_one_and_delete({"_id": ObjectId(category_id)})
    if deleted_category:
        return deleted_category


@app.post("/parts/", tags=["Parts"], response_model=Part, response_model_by_alias=False)
async def create_part(part: Part, db: AsyncIOMotorDatabase = Depends(get_database)):
    # Check if the category exists
    category = await db.categories.find_one({"name": part.category})
    if not category:
        raise HTTPException(status_code=400, detail="Category does not exist")

    # Check if the category is not a base category
    if not category["parent_name"]:
        raise HTTPException(status_code=400, detail="Cannot assign part to a base category")

    # Save the new part to the database
    part_data = part.model_dump(by_alias=True, exclude=["id"])
    result = await db.parts.insert_one(part_data)

    created_part = await db.parts.find_one({"_id": result.inserted_id})
    return created_part


@app.get("/parts/", tags=["Parts"], response_model=List[Part], response_model_by_alias=False)
async def read_parts(db: AsyncIOMotorDatabase = Depends(get_database)):
    parts = await db.parts.find().to_list(length=None)
    return parts


@app.get("/parts/{part_id}", tags=["Parts"], response_model=Part, response_model_by_alias=False)
async def read_part(part_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    try:
        # Get part data based on part_id
        part = await db.parts.find_one({"_id": ObjectId(part_id)})

        # Check if part exists
        if not part:
            raise HTTPException(status_code=404, detail="Part not found")

        return part

    except InvalidId:
        raise HTTPException(status_code=422, detail="Invalid part_id format")


@app.put("/parts/{part_id}", tags=["Parts"], response_model=Part, response_model_by_alias=False)
async def update_part(part_id: str, part: Part, db: AsyncIOMotorDatabase = Depends(get_database)):
    try:
        # Check if the category exists
        category = await db.categories.find_one({"name": part.category})
        if not category:
            raise HTTPException(status_code=400, detail="Category does not exist")

        # Check if the category is not a base category
        if not category.get("parent_name"):
            raise HTTPException(status_code=400, detail="Cannot assign part to a base category")

        result = await db.parts.update_one({"_id": ObjectId(part_id)}, {"$set": dict(part)})

        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Part not found")

        return await db.parts.find_one({"_id": ObjectId(part_id)})

    except InvalidId:
        raise HTTPException(status_code=422, detail="Invalid part_id format")


@app.delete("/parts/{part_id}", tags=["Parts"], response_model=Part, response_model_by_alias=False)
async def delete_part(part_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    # Get part data based on part_id
    try:
        part = await db.parts.find_one({"_id": ObjectId(part_id)})
    except InvalidId:
        raise HTTPException(status_code=422, detail="Invalid part_id format")

    # Check if part exists
    if not part:
        raise HTTPException(status_code=404, detail="Part not found")

    # Delete part
    deleted_part = await db.parts.find_one_and_delete({"_id": ObjectId(part_id)})
    if deleted_part:
        return deleted_part


@app.get("/parts/search/", tags=["Search"], response_model=List[Part], response_model_by_alias=False)
async def search_parts(
    serial_number: str = Query(None),
    name: str = Query(None),
    description: str = Query(None),
    category: str = Query(None),
    quantity: int = Query(None),
    price: float = Query(None),
    room: str = Query(None),
    bookcase: str = Query(None),
    shelf: str = Query(None),
    cuvette: str = Query(None),
    column: str = Query(None),
    row: str = Query(None),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    # Build a filter dictionary based on provided query parameters
    filter_dict = {}

    for field in ["serial_number", "name", "description", "category"]:
        if locals()[field] is not None:
            filter_dict[field] = {"$regex": f".*{locals()[field]}.*", "$options": "i"}

    for field in ["quantity", "price"]:
        if locals()[field] is not None:
            filter_dict[field] = locals()[field]

    # Handle location based on query parameters
    for field in ["room", "bookcase", "shelf", "cuvette", "column", "row"]:
        if locals()[field] is not None:
            filter_dict[f"location.{field}"] = {"$regex": f".*{locals()[field]}.*", "$options": "i"}

    # Search for parts based on the filter dictionary
    parts = await db.parts.find(filter_dict).to_list(length=None)

    return parts
