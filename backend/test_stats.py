#!/usr/bin/env python3
"""
Simple test script to check if the stats endpoint is working
"""

import asyncio
import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from database import db, get_files_collection, get_generations_collection

async def test_stats():
    """Test the stats calculation"""
    try:
        # Connect to database
        await db.connect()
        print("✅ Connected to database")
        
        # Get collections
        files_collection = get_files_collection()
        generations_collection = get_generations_collection()
        
        # Test files collection
        try:
            files_count = await files_collection.count_documents({})
            print(f"✅ Files collection accessible, {files_count} documents found")
        except Exception as e:
            print(f"❌ Error accessing files collection: {e}")
        
        # Test generations collection
        try:
            generations_count = await generations_collection.count_documents({})
            print(f"✅ Generations collection accessible, {generations_count} documents found")
        except Exception as e:
            print(f"❌ Error accessing generations collection: {e}")
        
        # Test stats calculation
        try:
            cursor = files_collection.find({})
            files = await cursor.to_list(length=None)
            total_downloads = sum(file_data.get("download_count", 0) for file_data in files)
            print(f"✅ Stats calculation successful - Total downloads: {total_downloads}")
        except Exception as e:
            print(f"❌ Error calculating stats: {e}")
        
        # Disconnect
        await db.disconnect()
        print("✅ Disconnected from database")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_stats()) 