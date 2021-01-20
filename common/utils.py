from typing import Dict
import bson


async def generate_id() -> str:

    return str(bson.objectid.ObjectId())


async def serialize_to_mongo(data: Dict) -> Dict:
    data["_id"] = await generate_id()
    return data
