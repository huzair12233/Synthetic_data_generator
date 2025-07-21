from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import FileResponse
from typing import List, Optional
import os
import sys
from pathlib import Path
from datetime import datetime
from bson import ObjectId

# Add parent directory to path for imports
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from auth import get_current_user
from database import User, get_files_collection, GeneratedFile, get_generations_collection
from config import Config

router = APIRouter(prefix="/files", tags=["File Management"])

@router.get("/health")
async def health_check():
    """Health check endpoint for files API"""
    try:
        # Test database connection
        files_collection = get_files_collection()
        generations_collection = get_generations_collection()
        
        # Simple database test
        files_count = await files_collection.count_documents({})
        generations_count = await generations_collection.count_documents({})
        
        return {
            "success": True,
            "message": "Files API is healthy",
            "database": {
                "files_collection": "accessible",
                "generations_collection": "accessible",
                "files_count": files_count,
                "generations_count": generations_count
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Files API health check failed: {str(e)}",
            "timestamp": datetime.utcnow().isoformat()
        }

@router.get("/test")
async def test_files_endpoint():
    """Test endpoint to check if files API is working"""
    return {
        "success": True,
        "message": "Files API is working",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/stats-simple")
async def get_simple_stats():
    """Simple stats endpoint without authentication for testing"""
    try:
        files_collection = get_files_collection()
        generations_collection = get_generations_collection()
        
        # Get all files
        try:
            cursor = files_collection.find({})
            files = await cursor.to_list(length=None)
        except Exception as e:
            print(f"Error fetching files: {e}")
            files = []
        
        # Get all generations
        try:
            gen_cursor = generations_collection.find({})
            generations = await gen_cursor.to_list(length=None)
        except Exception as e:
            print(f"Error fetching generations: {e}")
            generations = []
        
        # Calculate statistics
        total_downloads = sum(file_data.get("download_count", 0) for file_data in files)
        total_generations = len(generations)
        
        print(f"Simple stats - Downloads: {total_downloads}, Generations: {total_generations}")
        
        return {
            "success": True,
            "stats": {
                "total_downloads": total_downloads,
                "total_generations": total_generations,
                "total_files": len(files),
                "message": "Simple stats endpoint working"
            }
        }
        
    except Exception as e:
        print(f"Error in simple stats: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "error": str(e),
            "stats": {
                "total_downloads": 0,
                "total_generations": 0,
                "total_files": 0
            }
        }

@router.get("/")
async def get_user_files(current_user: User = Depends(get_current_user)):
    """Get all files for the current user"""
    try:
        files_collection = get_files_collection()
        
        # Get files for current user
        cursor = files_collection.find({"user_id": current_user.email})
        files = await cursor.to_list(length=None)
        
        # Convert to list of file objects
        file_list = []
        for file_data in files:
            file_obj = GeneratedFile.from_dict(file_data)
            file_list.append({
                "id": str(file_data.get("_id")),
                "filename": file_obj.filename,
                "file_type": file_obj.file_type,
                "data_type": file_obj.data_type,
                "model_type": file_obj.model_type,
                "num_samples": file_obj.num_samples,
                "file_size": file_obj.file_size,
                "created_at": file_obj.created_at.isoformat(),
                "download_count": file_obj.download_count
            })
        
        return {
            "success": True,
            "files": file_list,
            "total_files": len(file_list)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving files: {str(e)}"
        )

@router.get("/download/{file_id}")
async def download_file(file_id: str, current_user: User = Depends(get_current_user)):
    """Download a specific file"""
    try:
        files_collection = get_files_collection()
        
        # Convert string ID to ObjectId
        try:
            object_id = ObjectId(file_id)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file ID format"
            )
        
        # Find the file
        file_data = await files_collection.find_one({"_id": object_id, "user_id": current_user.email})
        
        if not file_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="File not found"
            )
        
        file_obj = GeneratedFile.from_dict(file_data)
        file_path = Path(file_obj.file_path)
        
        if not file_path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="File not found on disk"
            )
        
        # Update download count
        await files_collection.update_one(
            {"_id": object_id},
            {"$inc": {"download_count": 1}}
        )
        
        return FileResponse(
            path=str(file_path),
            filename=file_obj.filename,
            media_type='application/octet-stream'
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error downloading file: {str(e)}"
        )

@router.delete("/{file_id}")
async def delete_file(file_id: str, current_user: User = Depends(get_current_user)):
    """Delete a specific file"""
    try:
        files_collection = get_files_collection()
        
        # Convert string ID to ObjectId
        try:
            object_id = ObjectId(file_id)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file ID format"
            )
        
        # Find the file
        file_data = await files_collection.find_one({"_id": object_id, "user_id": current_user.email})
        
        if not file_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="File not found"
            )
        
        file_obj = GeneratedFile.from_dict(file_data)
        file_path = Path(file_obj.file_path)
        
        # Delete file from disk
        if file_path.exists():
            file_path.unlink()
        
        # Delete from database
        await files_collection.delete_one({"_id": object_id})
        
        return {
            "success": True,
            "message": f"File '{file_obj.filename}' deleted successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting file: {str(e)}"
        )

@router.get("/stats")
async def get_file_stats(current_user: User = Depends(get_current_user)):
    """Get file statistics for the current user"""
    try:
        files_collection = get_files_collection()
        generations_collection = get_generations_collection()
        
        # Get all files for user with error handling
        try:
            cursor = files_collection.find({"user_id": current_user.email})
            files = await cursor.to_list(length=None)
        except Exception as e:
            print(f"Error fetching files: {e}")
            files = []
        
        # Get all generations for user with error handling
        try:
            gen_cursor = generations_collection.find({"user_id": current_user.email})
            generations = await gen_cursor.to_list(length=None)
        except Exception as e:
            print(f"Error fetching generations: {e}")
            generations = []
        
        # Calculate statistics with safe defaults
        total_downloads = sum(file_data.get("download_count", 0) for file_data in files)
        total_generations = len(generations)
        
        # Count by data type
        data_type_counts = {}
        for file_data in files:
            data_type = file_data.get("data_type", "unknown")
            data_type_counts[data_type] = data_type_counts.get(data_type, 0) + 1
        
        # Count by file type
        file_type_counts = {}
        for file_data in files:
            file_type = file_data.get("file_type", "unknown")
            file_type_counts[file_type] = file_type_counts.get(file_type, 0) + 1
        
        print(f"Stats calculated - Downloads: {total_downloads}, Generations: {total_generations}")
        
        return {
            "success": True,
            "stats": {
                "total_downloads": total_downloads,
                "total_generations": total_generations,
                "data_type_distribution": data_type_counts,
                "file_type_distribution": file_type_counts
            }
        }
        
    except Exception as e:
        print(f"Error in get_file_stats: {str(e)}")
        import traceback
        traceback.print_exc()
        # Return default stats instead of throwing error
        return {
            "success": True,
            "stats": {
                "total_downloads": 0,
                "total_generations": 0,
                "data_type_distribution": {},
                "file_type_distribution": {}
            }
        } 