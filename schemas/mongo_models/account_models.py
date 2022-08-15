from typing import Optional, Tuple
from pydantic import BaseModel
from beanie import Document, Indexed, init_beanie
import asyncio, motor
import pymongo

class MongoCompany(Document):
    company_id : int
    labels : list[str] = []