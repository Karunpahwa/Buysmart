# BuySmart Assistant

A web application to help buyers search and negotiate on OLX India. Built with React, FastAPI, PostgreSQL, and AI-powered features.

## 🚀 Features

- **Smart Requirement Management**: Create and track buying requirements
- **OLX Integration**: Automated scraping and listing discovery
- **AI-Powered Analysis**: Intelligent listing evaluation and recommendations
- **Messaging System**: Direct communication with sellers
- **Negotiation Assistant**: AI-powered negotiation support
- **Real-time Updates**: Live notifications and status tracking

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **PostgreSQL**: Primary database (Supabase)
- **Redis**: Caching and background jobs
- **SQLAlchemy**: ORM for database operations
- **Playwright**: Web scraping for OLX
- **OpenAI API**: AI-powered features
- **JWT**: Authentication

### Frontend
- **React**: UI framework
- **TypeScript**: Type safety
- **TailwindCSS**: Styling
- **React Router**: Navigation
- **Axios**: HTTP client
- **Vite**: Build tool

## 📁 Project Structure

```
Buysmart/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── models/         # Database models
│   │   ├── services/       # Business logic
│   │   └── main.py         # FastAPI app
│   ├── tests/              # Backend tests
│   └── requirements.txt    # Python dependencies
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   └── App.tsx         # Main app
│   └── package.json        # Node dependencies
├── docs/                   # Documentation
└── deploy/                 # Deployment configs
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL database (Supabase recommended)

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Buysmart
   ```

2. **Set up Python environment**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your database URL and API keys
   ```

4. **Run the backend**
   ```bash
   python -m uvicorn app.main:app --reload
   ```

### Frontend Setup

1. **Install dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Start development server**
   ```bash
   npm run dev
   ```

3. **Open in browser**
   ```
   http://localhost:5173
   ```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the `backend` directory:

```env
# Database
DATABASE_URL=postgresql://user:password@host:port/database

# JWT
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OpenAI
OPENAI_API_KEY=your-openai-api-key

# App Settings
DEBUG=true
ENVIRONMENT=development
```

### Supabase Setup

1. Create a Supabase project
2. Get your database connection string
3. Update `DATABASE_URL` in `.env`
4. Run the setup script:
   ```bash
   python setup_supabase.py
   ```

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 🚀 Deployment

### Vercel Deployment

1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Deploy**
   ```bash
   ./deploy.sh
   ```

### Manual Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## 📚 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Check the documentation in `/docs`
- Review the deployment guide

## 🔄 Development Workflow

1. **Feature Development**
   - Create feature branch
   - Implement backend API
   - Add frontend components
   - Write tests
   - Update documentation

2. **Testing**
   - Run backend tests: `pytest`
   - Run frontend tests: `npm test`
   - Manual testing

3. **Deployment**
   - Test on staging
   - Deploy to production
   - Monitor logs

## 📊 Project Status

- ✅ Backend API (FastAPI)
- ✅ Database models (PostgreSQL)
- ✅ Frontend (React + TypeScript)
- ✅ Authentication (JWT)
- ✅ Basic UI components
- 🔄 OLX scraping integration
- 🔄 AI-powered features
- 🔄 Deployment automation

## 🎯 Roadmap

- [ ] Complete OLX scraping
- [ ] AI listing analysis
- [ ] Messaging system
- [ ] Negotiation assistant
- [ ] Mobile app
- [ ] Advanced analytics 