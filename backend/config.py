import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for SmartSynth Backend"""
    
    # Project paths
    BASE_DIR = Path(__file__).parent.parent
    BACKEND_DIR = Path(__file__).parent
    FRONTEND_DIR = BASE_DIR / "frontend"
    
    # API Configuration
    API_V1_STR = "/api/v1"
    PROJECT_NAME = "SmartSynth"
    VERSION = "1.0.0"
    
    # Server Configuration
    HOST = "0.0.0.0"
    PORT = 8000
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # Database Configuration
    MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "smartsynth")
    
    # Authentication
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    
    # Gemini API Configuration
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    GEMINI_MODEL = "gemini-1.5-pro"
    
    # Generation Settings
    MAX_TOKENS = 2048
    TEMPERATURE = 0.7
    TOP_P = 0.9
    TOP_K = 40
    MAX_NUM_SAMPLES = 1000
    
    # File Storage
    UPLOAD_DIR = BASE_DIR / "uploads"
    SYNTHETIC_DATA_DIR = BASE_DIR / "data" / "synthetic"
    CHATBASED_DATA_DIR = SYNTHETIC_DATA_DIR / "chatbased"
    TABULAR_DATA_DIR = SYNTHETIC_DATA_DIR / "tabular"
    MODELS_DIR = BASE_DIR / "models"
    
    # Ensure directories exist
    UPLOAD_DIR.mkdir(exist_ok=True)
    SYNTHETIC_DATA_DIR.mkdir(exist_ok=True, parents=True)
    CHATBASED_DATA_DIR.mkdir(exist_ok=True, parents=True)
    TABULAR_DATA_DIR.mkdir(exist_ok=True, parents=True)
    MODELS_DIR.mkdir(exist_ok=True, parents=True)
    
    # CORS Settings
    CORS_ORIGINS = [
        "http://localhost:3000",  # React dev server
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
    ]
    
    # Domain-specific prompts for chat-based generation
    DOMAIN_PROMPTS = {
        'customer_support': {
            'description': 'Customer support conversations between customers and support agents',
            'examples': [
                'Product inquiry and troubleshooting',
                'Order status and tracking',
                'Refund and return requests',
                'Technical support issues',
                'Account management questions'
            ]
        },
        'chatbot_training': {
            'description': 'Conversations for training AI chatbots',
            'examples': [
                'FAQ interactions',
                'Intent recognition scenarios',
                'Multi-turn conversations',
                'Error handling dialogues',
                'Task completion flows'
            ]
        },
        'spam_detection': {
            'description': 'Email samples for spam detection training',
            'examples': [
                'Phishing attempts',
                'Marketing spam',
                'Scam emails',
                'Legitimate business emails',
                'Newsletter subscriptions'
            ]
        },
        'business_communication': {
            'description': 'Professional business email communications',
            'examples': [
                'Client proposals',
                'Internal team communications',
                'Meeting scheduling',
                'Project updates',
                'Contract negotiations'
            ]
        }
    }
    
    # Tabular data models
    TABULAR_MODELS = {
        'ecommerce': {
            'name': 'Ecommerce',
            'description': 'Product data, customer transactions, inventory',
            'file_path': 'models/Ecommerce/ecommerce_model.pkl'
        },
        'education': {
            'name': 'Education',
            'description': 'Student records, course data, academic performance',
            'file_path': 'models/Education/education_model.pkl'
        },
        'finance': {
            'name': 'Finance',
            'description': 'Financial transactions, market data, customer profiles',
            'file_path': 'models/Finance/finance_model.pkl'
        },
        'medical': {
            'name': 'Medical',
            'description': 'Patient records, medical procedures, healthcare data',
            'file_path': 'models/Medical/medical_model.pkl'
        }
    } 