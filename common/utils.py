#!/usr/bin/python3

from typing import Dict
import bson


async def serialize_to_mongo(data: Dict) -> Dict:
    data["_id"] = str(bson.objectid.ObjectId())
    return data
