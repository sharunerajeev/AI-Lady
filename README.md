# 🤖 AI Insurance Assistant (AI Lady)

An AI-powered insurance assistant chatbot built with FastAPI and modern web technologies. This POC demonstrates customer support capabilities for insurance companies with a beautiful, responsive UI.

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🌟 Features

### Current Implementation

- ✅ **Modern Web UI**

  - Beautiful, responsive interface with Google Material Icons
  - Light/Dark theme support
  - Real-time chat with typing indicators
  - Quick action buttons for common queries
  - Session management with conversation history
  - Live system status monitoring

- ✅ **AI-Powered Chat**

  - Multi-provider support (Ollama, Azure OpenAI, Fallback)
  - Natural language understanding
  - Context-aware responses using RAG (Retrieval Augmented Generation)
  - Conversation history tracking
  - Response metadata (provider, model, processing time)

- ✅ **Backend API**
  - RESTful API with FastAPI
  - Async database operations
  - Health monitoring endpoints
  - Provider fallback system
  - SQLite storage for conversations

### Future Phases (Roadmap)

- 🔜 Smart Recommendations (Product suggestions)
- 🔜 Claims Assist (OCR-based claim filing)
- 🔜 Personalized Alerts (Renewals, payments)
- 🔜 AI Document Assistant (Policy summarization)

## 🏗️ Architecture

```
┌─────────────────────────┐
│   Modern Web UI         │  (HTML/CSS/JS)
│   (static/index.html)   │  Served at Port 8000
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│   FastAPI Backend       │  (Port 8000)
│   (RESTful API)         │
└────────┬────────────────┘
         │
    ┌────┴────┬──────────┬──────────┐
    ▼         ▼          ▼          ▼
┌────────┐ ┌───────┐ ┌────────┐ ┌──────┐
│ Ollama │ │Vector │ │SQLite  │ │Mock  │
│ /Azure │ │Store  │ │   DB   │ │FAQ   │
└────────┘ └───────┘ └────────┘ └──────┘
```

### UI Architecture

The modern web interface is built with:

- **HTML5** - Clean, semantic markup
- **CSS3** - Modular styles with CSS variables for theming
- **Vanilla JavaScript** - No framework dependencies, lightweight and fast
- **Google Material Icons** - Consistent, professional iconography
- **Responsive Design** - Works seamlessly on desktop and mobile

## 📋 Prerequisites

- Python 3.11 or higher
- AI Provider (choose one):
  - Ollama (local, recommended for development)
  - Azure OpenAI (cloud-based)
  - Or use the built-in fallback mode (no API required)
- Docker (optional - for containerized deployment)

## 🚀 Quick Start

**📖 Detailed Guides:**

- [DEPLOYMENT.md](DEPLOYMENT.md) - Complete deployment instructions
- [ACCURACY_AND_SECURITY_GUIDE.md](ACCURACY_AND_SECURITY_GUIDE.md) - Improve AI & add guardrails
- [knowledge_base/README.md](knowledge_base/README.md) - Add company knowledge
- [RAG_SYSTEM.md](RAG_SYSTEM.md) - Understanding our RAG implementation

### Option 1: Local Development (Recommended)

1. **Clone or navigate to the project directory**

2. **Set up environment variables**

   ```bash
   cp .env.example .env
   # Edit .env and configure your AI provider
   # For Ollama: Set MODEL_PROVIDER=ollama
   # For Azure: Set AZURE_OPENAI_API_KEY and other Azure settings
   # For fallback: Set MODEL_PROVIDER=fallback
   ```

3. **Run the startup script**

   **Linux/Mac:**

   ```bash
   chmod +x start.sh
   ./start.sh
   ```

   **Windows:**

   ```cmd
   start.bat
   ```

4. **Access the application**
   - Web UI: <http://localhost:8000/static/index.html>
   - API Documentation: <http://localhost:8000/docs>
   - API Health: <http://localhost:8000/api/v1/health>

### Option 2: Docker Deployment

1. **Set up environment variables**

   ```bash
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
   ```

2. **Build and run with Docker Compose**

   ```bash
   docker-compose up -d
   ```

3. **Access the application**

   - Web UI: <http://localhost:8000/static/index.html>
   - API: <http://localhost:8000>

4. **View logs**

   ```bash
   docker-compose logs -f
   ```

5. **Stop services**

   ```bash
   docker-compose down
   ```

### Option 3: Manual Setup

1. **Create virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variables**

   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

4. **Start the API server**

   ```bash
   python main.py
   ```

5. **Access the Web UI**

   Open your browser and navigate to: <http://localhost:8000/static/index.html>

   The UI is now integrated into the FastAPI application - no separate frontend server needed!

## 📁 Project Structure

```
ai-insurance-assistant/
├── app/
│   ├── __init__.py
│   ├── config.py              # Configuration management
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py          # API endpoints
│   │   └── schemas.py         # Pydantic models
│   ├── models/
│   │   ├── __init__.py
│   │   └── database.py        # SQLAlchemy models
│   └── services/
│       ├── __init__.py
│       ├── ai_service.py      # AI provider integration
│       ├── database_service.py # Database operations
│       └── vector_service.py  # Vector store & FAQ search
├── data/
│   ├── __init__.py
│   └── insurance_faq.py       # Insurance FAQ knowledge base
├── static/                    # Modern Web UI (NEW!)
│   ├── index.html             # Main HTML structure
│   ├── styles.css             # All CSS styles with theming
│   └── script.js              # Client-side JavaScript
├── tests/                     # Test files
│   ├── __init__.py
│   └── test_api.py
├── .env.example               # Environment template
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── main.py                    # FastAPI application
├── requirements.txt
├── start.sh                   # Linux/Mac startup script
├── start.bat                  # Windows startup script
└── README.md
```

### Key Changes in v2.0

- **New Modern UI**: Custom HTML/CSS/JS interface with integrated backend
- **Integrated Frontend**: UI served directly from FastAPI (no separate server)
- **Modular Code**: Separated CSS and JavaScript into dedicated files
- **Better UX**: Material Icons, theme switching, responsive design

## 🔧 Configuration

### Environment Variables

| Variable                  | Description           | Default                                      |
| ------------------------- | --------------------- | -------------------------------------------- |
| `MODEL_PROVIDER`          | AI provider to use    | ollama (fallback, ollama, azure)             |
| `OLLAMA_BASE_URL`         | Ollama server URL     | http://localhost:11434                       |
| `AZURE_OPENAI_API_KEY`    | Azure OpenAI API key  | Required for Azure provider                  |
| `AZURE_OPENAI_ENDPOINT`   | Azure OpenAI endpoint | Required for Azure provider                  |
| `AZURE_OPENAI_DEPLOYMENT` | Azure deployment name | Required for Azure provider                  |
| `APP_NAME`                | Application name      | AI Insurance Assistant                       |
| `DEBUG`                   | Debug mode            | True                                         |
| `HOST`                    | API host              | 0.0.0.0                                      |
| `PORT`                    | API port              | 8000                                         |
| `DATABASE_URL`            | SQLite database path  | sqlite+aiosqlite:///./insurance_assistant.db |
| `MAX_TOKENS`              | Max response tokens   | 500                                          |
| `TEMPERATURE`             | Response creativity   | 0.7                                          |

### Provider Configuration

**Ollama (Recommended for Local Development)**

```bash
MODEL_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=phi3:mini
```

**Azure OpenAI**

```bash
MODEL_PROVIDER=azure
AZURE_OPENAI_API_KEY=your_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=your-deployment-name
```

**Fallback (No API Required)**

```bash
MODEL_PROVIDER=fallback
```

## 📚 API Documentation

Once the application is running, visit:

- **Swagger UI**: <http://localhost:8000/docs>
- **ReDoc**: <http://localhost:8000/redoc>

### Key Endpoints

- `GET /api/v1/health` - Health check and provider status
- `POST /api/v1/chat` - Send chat message
- `GET /api/v1/conversations/{session_id}` - Get conversation history
- `POST /api/v1/conversations/{conversation_id}/rate` - Rate a response

## 💬 Sample Questions

Try asking the AI Lady:

- "What is term life insurance?"
- "How do I file an insurance claim?"
- "What does homeowners insurance cover?"
- "What is the difference between HMO and PPO?"
- "How much life insurance do I need?"
- "What is comprehensive auto insurance?"

## 🧪 Testing

### Using the Web UI

1. Start the application
2. Open <http://localhost:8000/static/index.html>
3. Try the quick action buttons or type your own questions
4. Use the theme toggle to switch between light/dark modes
5. Hover over bot messages to see provider details

### API Testing

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Send a chat message
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is life insurance?"}'
```

### Running Tests

```bash
# Activate virtual environment
source venv/bin/activate

# Run tests
pytest

# Run with coverage
pytest --cov=app tests/
```

## 🎯 Use Cases Covered

### 1. Customer Support ✅ (Current)

- FAQ responses for policies, products, claims, renewals
- Natural language understanding
- Context-aware conversations
- Multi-turn dialogue support

### 2. Smart Recommendations 🔜 (Future)

- Product recommendations based on customer needs
- Add-on suggestions using predictive modeling

### 3. Claims Assist 🔜 (Future)

- OCR-based claim filing
- Claim status tracking
- Email/SMS notifications

### 4. Personalized Alerts 🔜 (Future)

- Renewal reminders
- Payment notifications
- Policy T&C updates

### 5. AI Document Assistant 🔜 (Future)

- Policy document summarization
- Key information extraction

## 🛠️ Technology Stack

### Frontend

- **HTML5** - Semantic markup
- **CSS3** - Modern styling with CSS variables
- **Vanilla JavaScript** - No framework dependencies
- **Google Material Icons** - Professional iconography

### Backend

- **FastAPI** - High-performance Python web framework
- **SQLAlchemy** - Async ORM for database operations
- **SQLite** - Lightweight database

### AI & ML

- **Ollama** - Local LLM inference (recommended)
- **Azure OpenAI** - Cloud-based AI (alternative)
- **Keyword-based RAG** - FAQ retrieval system
- **Fallback System** - Rule-based responses when AI unavailable

### DevOps

- **Docker & Docker Compose** - Containerization
- **Pytest** - Testing framework
- **Uvicorn** - ASGI server

## 📈 Performance

- **Response Time**: < 2 seconds (with OpenAI API)
- **Fallback Mode**: Instant responses using vector similarity
- **Concurrent Users**: Supports multiple sessions
- **Database**: Async operations for scalability

## 🔒 Security Notes

- Store API keys in `.env` file (never commit)
- Use environment variables for sensitive data
- Implement rate limiting for production
- Add authentication/authorization as needed
- Review data retention policies

## 🐛 Troubleshooting

### Common Issues

1. **"Connection refused" or UI not loading**

   - Ensure the backend is running: `python main.py`
   - Check that port 8000 is not in use
   - Access UI at: <http://localhost:8000/static/index.html>

2. **"Provider unavailable" errors**

   - For Ollama: Ensure Ollama is running (`ollama serve`)
   - For Azure: Check your API keys in `.env`
   - Or switch to fallback mode: `MODEL_PROVIDER=fallback`

3. **"Port already in use"**

   - Kill existing processes: `pkill -f "python main.py"`
   - Or change port in `.env`: `PORT=8001`

4. **UI shows "Offline" status**

   - Check backend logs for errors
   - Verify provider configuration
   - Test API: `curl http://localhost:8000/api/v1/health`

5. **Database locked errors**

   - Ensure only one instance is running
   - Delete `insurance_assistant.db` and restart if corrupted

6. **Dependencies installation fails**
   - Update pip: `pip install --upgrade pip`
   - Install system dependencies if needed

## 🤝 Contributing

This is a POC project. For enhancements:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

MIT License - feel free to use for your projects

## 👥 Contact & Support

For questions or issues:

- Create an issue in the repository
- Contact the development team

## 🗺️ Roadmap

- [x] Phase 1: Customer Support FAQ (Current)
- [ ] Phase 2: Smart Product Recommendations
- [ ] Phase 3: Claims Processing & OCR
- [ ] Phase 4: Personalized Alerts System
- [ ] Phase 5: Document Summarization
- [ ] Phase 6: Voice Integration
- [ ] Phase 7: Multi-language Support

## 📊 Version History

- **v2.0.0** (November 2025) - Major UI Overhaul

  - ✨ Modern web interface with HTML/CSS/JS
  - 🎨 Light/Dark theme support
  - 📱 Fully responsive design
  - 🔄 Multi-provider support (Ollama, Azure, Fallback)
  - 🎯 Google Material Icons integration
  - ⚡ Integrated frontend (no separate server)
  - 📊 Live system status monitoring
  - 🎪 Hover tooltips for metadata

- **v1.0.0** (November 2025) - Initial POC Release
  - Customer Support FAQ chatbot
  - RAG-based responses
  - Basic web UI
  - Docker support

## 🎨 UI Features (v2.0)

### Design Improvements

- **Clean Separation**: HTML, CSS, and JavaScript in separate files
- **Uniform Typography**: Noto Sans font throughout
- **Compact Header**: Reduced navbar size for more chat space
- **Professional Footer**: Copyright and quick links
- **Enhanced Contrast**: Better visibility in light mode
- **Rounded Corners**: Modern, softer appearance
- **Material Icons**: Consistent, professional iconography

### User Experience

- **Quick Actions**: One-click common questions
- **Theme Toggle**: Switch between light/dark modes
- **Status Indicator**: Live system health monitoring
- **Typing Indicator**: Visual feedback during AI processing
- **Metadata Tooltips**: Hover to see provider details
- **Generic User Icon**: Professional account representation
- **Smooth Animations**: Polished interactions

---

## Built with ❤️ for the insurance industry
