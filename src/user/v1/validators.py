#!/usr/bin/python3

from config.settings import user_collection


async def validate_login(login: str):
    return await user_collection.find_one({"username": login})
