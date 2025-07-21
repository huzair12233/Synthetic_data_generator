# SmartSynth - AI-Powered Synthetic Data Generation Platform

A comprehensive synthetic data generation system that supports both structured data (using SDV) and text-based data (using Google Gemini AI) with a beautiful React frontend and FastAPI backend.

## 🚀 Features

### 🔐 User Authentication
- **Sign up/Login**: Secure user registration and authentication
- **JWT Tokens**: Stateless authentication with automatic token refresh
- **User Dashboard**: Personalized experience with user-specific data

### 📊 Structured Data Generation
- **Ecommerce**: Product data, customer transactions, inventory
- **Education**: Student records, course data, academic performance
- **Finance**: Financial transactions, market data, customer profiles
- **Medical**: Patient records, medical procedures, healthcare data

### 💬 Text-Based Data Generation
- **Chat Conversations**: Customer support, chatbot training
- **Emails**: Spam detection, business communication

### 📁 File Management
- **Download History**: Track all generated files
- **Multiple Formats**: CSV, JSON, Excel export options
- **File Persistence**: Files saved per user with download tracking

## 🏗️ Project Structure

```
smartsynth/
├── backend/                    # FastAPI Backend
│   ├── __init__.py
│   ├── main.py                # Main FastAPI application
│   ├── config.py              # Configuration settings
│   ├── database.py            # MongoDB models and connection
│   ├── auth.py                # Authentication logic
│   ├── api/                   # API endpoints
│   │   ├── __init__.py
│   │   ├── auth.py           # Authentication endpoints
│   │   ├── generation.py     # Data generation endpoints
│   │   └── files.py          # File management endpoints
│   └── generators/           # Data generation modules
│       ├── __init__.py
│       ├── chat_generator.py # Chat/email generation
│       └── tabular_generator.py # Tabular data generation
├── frontend/                  # React Frontend
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/       # Reusable components
│   │   ├── contexts/         # React contexts
│   │   ├── pages/           # Page components
│   │   ├── App.js
│   │   └── index.js
│   ├── package.json
│   ├── tailwind.config.js
│   └── postcss.config.js
├── data/                     # Data storage
│   ├── real/                # Real datasets for training
│   └── synthetic/           # Generated synthetic data
│       ├── chatbased/       # Text-based data
│       └── tabular/         # Tabular data
├── models/                   # Trained SDV models
├── train/                    # Training scripts
│   ├── Ecommerce_train/
│   ├── Education_train/
│   ├── Finance_train/
│   └── Medical_train/
├── requirements.txt          # Python dependencies
├── env_example.txt          # Environment variables template
└── README.md
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- MongoDB (local or cloud)
- Google Gemini API key

### 1. Clone the Repository
```bash
git clone <repository-url>
cd smartsynth
```

### 2. Backend Setup

#### Install Python Dependencies
```bash
pip install -r requirements.txt
```

#### Set Up Environment Variables
```bash
# Copy the example environment file
cp env_example.txt .env

# Edit .env and add your configuration
nano .env
```

Required environment variables:
```env
# Google Gemini API Key
GEMINI_API_KEY=your_gemini_api_key_here

# MongoDB Connection
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=smartsynth

# JWT Secret (generate a secure random string)
SECRET_KEY=your-secret-key-here

# Optional: Override defaults
DEBUG=True
```

#### Start MongoDB
```bash
# Local MongoDB
mongod

# Or use MongoDB Atlas (cloud)
# Update MONGODB_URL in .env
```

#### Run Backend Server
```bash
cd backend
python main.py
```

The backend will be available at:
- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### 3. Frontend Setup

#### Install Node.js Dependencies
```bash
cd frontend
npm install
```

#### Start Development Server
```bash
npm start
```

The frontend will be available at:
- **Application**: http://localhost:3000

## 🎯 Usage

### 1. User Registration & Login
1. Visit http://localhost:3000
2. Click "Sign up" to create an account
3. Fill in your email, username, and password
4. Login with your credentials

### 2. Dashboard
After login, you'll see the SmartSynth dashboard with:
- Welcome message
- Quick stats
- Navigation to different generation types

### 3. Tabular Data Generation
1. Click "Tabular Data" in the navigation
2. Select a model (Ecommerce, Education, Finance, Medical)
3. Choose number of rows to generate
4. Select output format (CSV, JSON, Excel)
5. Click "Generate Data"
6. Download your generated file

### 4. Chat-Based Data Generation
1. Click "Chat Data" in the navigation
2. Choose data type (Chat Conversations or Emails)
3. Select domain and topic
4. Configure generation parameters
5. Click "Generate Data"
6. View results and download files

### 5. File Management
1. Click "My Files" to view all generated files
2. Download files anytime
3. View generation history
4. Track download statistics

## 🔧 API Endpoints

### Authentication
- `POST /api/v1/auth/signup` - Register new user
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/auth/me` - Get current user info

### Data Generation
- `POST /api/v1/generation/chat` - Generate chat conversations
- `POST /api/v1/generation/email` - Generate emails
- `POST /api/v1/generation/tabular` - Generate tabular data
- `GET /api/v1/generation/tabular/models` - Get available models

### File Management
- `GET /api/v1/files/my-files` - Get user's files
- `GET /api/v1/files/download/{filename}` - Download file
- `DELETE /api/v1/files/{filename}` - Delete file
- `GET /api/v1/files/history` - Get generation history
- `GET /api/v1/files/stats` - Get user statistics

## 🎨 Frontend Features

### Beautiful UI Components
- **Modern Design**: Clean, professional interface
- **Responsive Layout**: Works on desktop and mobile
- **Dark/Light Mode**: Toggle between themes
- **Loading States**: Smooth user experience
- **Toast Notifications**: Real-time feedback

### User Experience
- **Protected Routes**: Secure access to features
- **Form Validation**: Client-side validation
- **Error Handling**: Graceful error messages
- **File Downloads**: Direct file downloads
- **Progress Indicators**: Generation progress tracking

## 🔒 Security Features

### Authentication & Authorization
- **JWT Tokens**: Secure token-based authentication
- **Password Hashing**: bcrypt password encryption
- **Protected Routes**: Server-side route protection
- **User Isolation**: Data isolation per user

### Data Security
- **Input Validation**: Server-side validation
- **Rate Limiting**: API rate limiting
- **CORS Configuration**: Secure cross-origin requests
- **Environment Variables**: Secure configuration management

## 🚀 Deployment


### Frontend Deployment
```bash
# Build for production
cd frontend
npm run build

# Deploy to static hosting (Netlify, Vercel, etc.)
```

### Environment Setup
- Set production environment variables
- Configure MongoDB connection
- Set up SSL certificates
- Configure CORS origins

## 🧪 Testing

### Backend Testing
```bash
# Run backend tests
cd backend
python -m pytest

# Test API endpoints
curl http://localhost:8000/health
```

### Frontend Testing
```bash
# Run frontend tests
cd frontend
npm test

# Run build test
npm run build
```

## 🔧 Configuration

### Backend Configuration
Key settings in `backend/config.py`:
- `GEMINI_MODEL`: AI model version
- `MAX_TOKENS`: Generation limits
- `TEMPERATURE`: AI creativity level
- `MAX_NUM_SAMPLES`: Batch size limits

### Frontend Configuration
Key settings in `frontend/src/config.js`:
- `API_BASE_URL`: Backend API URL
- `UPLOAD_LIMIT`: File upload limits
- `THEME`: Default theme settings

## 🐛 Troubleshooting

### Common Issues

#### Backend Issues
1. **MongoDB Connection Error**
   - Check MongoDB is running
   - Verify connection string in `.env`
   - Check network connectivity

2. **Gemini API Error**
   - Verify API key is set in `.env`
   - Check API key permissions
   - Monitor API usage limits

3. **Import Errors**
   - Install all dependencies: `pip install -r requirements.txt`
   - Check Python version compatibility
   - Verify virtual environment activation

#### Frontend Issues
1. **Build Errors**
   - Clear node_modules: `rm -rf node_modules && npm install`
   - Check Node.js version compatibility
   - Verify all dependencies are installed

2. **API Connection Errors**
   - Check backend server is running
   - Verify CORS configuration
   - Check network connectivity

3. **Authentication Issues**
   - Clear browser storage
   - Check JWT token expiration
   - Verify backend authentication endpoints

### Getting Help
- Check the API documentation at http://localhost:8000/docs
- Review browser console for frontend errors
- Check server logs for backend errors
- Create an issue with detailed error information

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Submit a pull request


## 🙏 Acknowledgments

- **Google Gemini AI** for text generation capabilities
- **SDV (Synthetic Data Vault)** for structured data generation
- **FastAPI** for the robust backend framework
- **React** for the modern frontend framework
- **Tailwind CSS** for the beautiful UI components

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Review the troubleshooting section

---

**SmartSynth** - Making synthetic data generation accessible and beautiful! 🚀

