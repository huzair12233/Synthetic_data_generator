from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from datetime import datetime, timedelta
from typing import Optional, List
from config import Config

class Database:
    """Database connection manager"""
    
    def __init__(self):
        self.client: Optional[AsyncIOMotorClient] = None
        self.database = None
    
    async def connect(self):
        """Connect to MongoDB"""
        self.client = AsyncIOMotorClient(Config.MONGODB_URL)
        self.database = self.client[Config.DATABASE_NAME]
        print("✅ Connected to MongoDB")
    
    async def disconnect(self):
        """Disconnect from MongoDB"""
        if self.client:
            self.client.close()
            print("✅ Disconnected from MongoDB")
    
    def get_collection(self, collection_name: str):
        """Get a collection from the database"""
        return self.database[collection_name]

# Database instance
db = Database()

# Collections
def get_users_collection():
    return db.get_collection("users")

def get_files_collection():
    return db.get_collection("files")

def get_generations_collection():
    return db.get_collection("generations")

# User model
class User:
    def __init__(self, email: str, username: str, hashed_password: str):
        self.email = email
        self.username = username
        self.hashed_password = hashed_password
        self.created_at = datetime.utcnow()
        self.is_active = True
    
    def to_dict(self):
        return {
            "email": self.email,
            "username": self.username,
            "hashed_password": self.hashed_password,
            "created_at": self.created_at,
            "is_active": self.is_active
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        user = cls(
            email=data["email"],
            username=data["username"],
            hashed_password=data["hashed_password"]
        )
        user.created_at = data.get("created_at", datetime.utcnow())
        user.is_active = data.get("is_active", True)
        return user

# File model
class GeneratedFile:
    def __init__(self, user_id: str, filename: str, file_path: str, 
                 file_type: str, data_type: str, model_type: str = None,
                 num_samples: int = 1, file_size: int = 0):
        self.user_id = user_id
        self.filename = filename
        self.file_path = file_path
        self.file_type = file_type  # json, csv
        self.data_type = data_type  # tabular, chat, email
        self.model_type = model_type  # ecommerce, education, etc.
        self.num_samples = num_samples
        self.file_size = file_size
        self.created_at = datetime.utcnow()
        self.download_count = 0
    
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "filename": self.filename,
            "file_path": self.file_path,
            "file_type": self.file_type,
            "data_type": self.data_type,
            "model_type": self.model_type,
            "num_samples": self.num_samples,
            "file_size": self.file_size,
            "created_at": self.created_at,
            "download_count": self.download_count
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        file_obj = cls(
            user_id=data["user_id"],
            filename=data["filename"],
            file_path=data["file_path"],
            file_type=data["file_type"],
            data_type=data["data_type"],
            model_type=data.get("model_type"),
            num_samples=data.get("num_samples", 1),
            file_size=data.get("file_size", 0)
        )
        file_obj.created_at = data.get("created_at", datetime.utcnow())
        file_obj.download_count = data.get("download_count", 0)
        return file_obj

# Generation history model
class GenerationHistory:
    def __init__(self, user_id: str, generation_type: str, 
                 model_type: str = None, domain: str = None,
                 topic: str = None, num_samples: int = 1,
                 status: str = "completed"):
        self.user_id = user_id
        self.generation_type = generation_type  # tabular, chat, email
        self.model_type = model_type
        self.domain = domain
        self.topic = topic
        self.num_samples = num_samples
        self.status = status
        self.created_at = datetime.utcnow()
    
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "generation_type": self.generation_type,
            "model_type": self.model_type,
            "domain": self.domain,
            "topic": self.topic,
            "num_samples": self.num_samples,
            "status": self.status,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        history = cls(
            user_id=data["user_id"],
            generation_type=data["generation_type"],
            model_type=data.get("model_type"),
            domain=data.get("domain"),
            topic=data.get("topic"),
            num_samples=data.get("num_samples", 1),
            status=data.get("status", "completed")
        )
        history.created_at = data.get("created_at", datetime.utcnow())
        return history 