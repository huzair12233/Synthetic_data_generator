from fastapi import APIRouter, HTTPException, status, Depends, BackgroundTasks
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import os
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add parent directory to path for imports
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from auth import get_current_user
from database import User, get_files_collection, get_generations_collection, GeneratedFile, GenerationHistory
from generators.chat_generator import ChatBasedGenerator
from generators.tabular_generator import TabularDataGenerator
from config import Config

router = APIRouter(prefix="/generate", tags=["Data Generation"])

# Request/Response models
class ChatGenerationRequest(BaseModel):
    domain: str
    topic: str
    num_samples: int = 1
    num_turns: int = 5
    format: str = "json"

class EmailGenerationRequest(BaseModel):
    domain: str
    topic: str
    email_type: str = "business"
    num_samples: int = 1
    format: str = "json"

class TabularGenerationRequest(BaseModel):
    domain: str
    num_samples: int
    topic: Optional[str] = None
    custom_fields: Optional[Dict[str, Any]] = None
    format: str = "json"

class GenerationResponse(BaseModel):
    success: bool
    message: str
    data: Optional[List[Dict[str, Any]]] = None
    file_info: Optional[Dict[str, Any]] = None
    generated_at: str

# Initialize generators
chat_generator = None
tabular_generator = None

def get_chat_generator():
    global chat_generator
    if chat_generator is None:
        chat_generator = ChatBasedGenerator()
    return chat_generator

def get_tabular_generator():
    global tabular_generator
    if tabular_generator is None:
        tabular_generator = TabularDataGenerator()
    return tabular_generator

@router.get("/domains")
async def get_available_domains():
    """Get available domains for data generation"""
    tabular_generator = TabularDataGenerator()
    
    return {
        "tabular_domains": tabular_generator.get_available_domains(),
        "chat_domains": ["customer_support", "chatbot_training"],
        "email_domains": ["spam_detection", "business_communication"]
    }

@router.get("/test")
async def test_generation():
    """Test endpoint to check if generation API is working"""
    return {
        "success": True,
        "message": "Generation API is working",
        "timestamp": datetime.now().isoformat()
    }

@router.post("/tabular")
async def generate_tabular_data(
    request: TabularGenerationRequest,
    current_user: User = Depends(get_current_user)
):
    """Generate synthetic tabular data"""
    try:
        print(f"Starting tabular data generation for user {current_user.email}, domain: {request.domain}, samples: {request.num_samples}")
        
        generator = TabularDataGenerator()
        print("TabularDataGenerator initialized successfully")
        
        # Generate data
        print("Generating data...")
        result = generator.generate_tabular_data(
            domain=request.domain,
            num_samples=request.num_samples,
            topic=request.topic,
            custom_fields=request.custom_fields
        )
        print(f"Data generation completed, generated {len(result['data'])} records")
        
        # Save to file
        filename = f"tabular_{request.domain}_{request.num_samples}samples"
        print(f"Saving to file: {filename}")
        filepath = generator.save_to_file(
            data=result['data'],
            filename=filename,
            format=request.format,
            user_id=current_user.email
        )
        print(f"File saved to: {filepath}")
        
        # Save file record to database
        print("Saving file record to database...")
        file_record = GeneratedFile(
            user_id=current_user.email,
            filename=filename,
            file_path=filepath,
            file_type=request.format,
            data_type="tabular",
            model_type=request.domain,
            num_samples=request.num_samples,
            file_size=len(str(result['data']))
        )
        
        files_collection = get_files_collection()
        await files_collection.insert_one(file_record.to_dict())
        print("File record saved to database")
        
        # Save generation history
        print("Saving generation history...")
        history_record = GenerationHistory(
            user_id=current_user.email,
            generation_type="tabular",
            model_type=request.domain,
            topic=request.topic,
            num_samples=request.num_samples
        )
        
        generations_collection = get_generations_collection()
        await generations_collection.insert_one(history_record.to_dict())
        print("Generation history saved")
        
        # Return the file for download
        download_filename = f"{filename}.{request.format}"
        print(f"Returning file for download: {download_filename}")
        return FileResponse(filepath, filename=download_filename)
        
    except Exception as e:
        print(f"Error in generate_tabular_data: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating tabular data: {str(e)}"
        )

@router.post("/chat")
async def generate_chat_data(
    request: ChatGenerationRequest,
    current_user: User = Depends(get_current_user)
):
    """Generate synthetic chat conversations"""
    try:
        generator = ChatBasedGenerator()
        
        # Generate data
        results = []
        for i in range(request.num_samples):
            result = generator.generate_chat_conversation(
                domain=request.domain,
                topic=request.topic,
                num_turns=request.num_turns
            )
            results.append(result)
        
        # Save to file
        filename = f"chat_{request.domain}_{request.topic}_{request.num_samples}samples"
        filepath = generator.save_to_file(
            data=results,
            filename=filename,
            format=request.format,
            user_id=current_user.email
        )
        
        # Save file record to database
        file_record = GeneratedFile(
            user_id=current_user.email,
            filename=filename,
            file_path=filepath,
            file_type=request.format,
            data_type="chat",
            model_type="gemini",
            num_samples=request.num_samples,
            file_size=len(str(results))
        )
        
        files_collection = get_files_collection()
        await files_collection.insert_one(file_record.to_dict())
        
        # Save generation history
        history_record = GenerationHistory(
            user_id=current_user.email,
            generation_type="chat",
            domain=request.domain,
            topic=request.topic,
            num_samples=request.num_samples
        )
        
        generations_collection = get_generations_collection()
        await generations_collection.insert_one(history_record.to_dict())
        
        # Return the file for download
        download_filename = f"{filename}.{request.format}"
        return FileResponse(filepath, filename=download_filename)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating chat data: {str(e)}"
        )

@router.post("/email")
async def generate_email_data(
    request: EmailGenerationRequest,
    current_user: User = Depends(get_current_user)
):
    """Generate synthetic emails"""
    try:
        generator = ChatBasedGenerator()
        
        # Generate data
        results = []
        for i in range(request.num_samples):
            result = generator.generate_email(
                domain=request.domain,
                topic=request.topic,
                email_type=request.email_type
            )
            results.append(result)
        
        # Save to file
        filename = f"email_{request.domain}_{request.topic}_{request.num_samples}samples"
        filepath = generator.save_to_file(
            data=results,
            filename=filename,
            format=request.format,
            user_id=current_user.email
        )
        
        # Save file record to database
        file_record = GeneratedFile(
            user_id=current_user.email,
            filename=filename,
            file_path=filepath,
            file_type=request.format,
            data_type="email",
            model_type="gemini",
            num_samples=request.num_samples,
            file_size=len(str(results))
        )
        
        files_collection = get_files_collection()
        await files_collection.insert_one(file_record.to_dict())
        
        # Save generation history
        history_record = GenerationHistory(
            user_id=current_user.email,
            generation_type="email",
            domain=request.domain,
            topic=request.topic,
            num_samples=request.num_samples
        )
        
        generations_collection = get_generations_collection()
        await generations_collection.insert_one(history_record.to_dict())
        
        # Return the file for download
        download_filename = f"{filename}.{request.format}"
        return FileResponse(filepath, filename=download_filename)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating email data: {str(e)}"
        ) 