# 🚀 Deployment Guide

Complete instructions for deploying AI Insurance Assistant on a new system.

## 📋 Prerequisites

### System Requirements

- **OS**: Linux, macOS, or Windows
- **Python**: 3.11 or higher
- **RAM**: 4GB minimum (8GB recommended for Ollama)
- **Disk**: 2GB free space (more if using Ollama models)

### Required Software

- Git (for cloning repository)
- Python 3.11+
- pip (Python package manager)
- AI Provider (choose one):
  - **Ollama** (recommended for local deployment)
  - **Azure OpenAI** (cloud-based)
  - **Fallback mode** (no AI setup needed)

## 📦 Step-by-Step Deployment

### Step 1: Clone/Transfer the Repository

**Option A: Using Git**

```bash
git clone <repository-url>
cd ai-insurance-assistant
```

**Option B: Transfer Files Manually**

```bash
# Create project directory
mkdir ai-insurance-assistant
cd ai-insurance-assistant

# Copy all files from source to this directory
# Make sure to include:
# - app/ folder
# - data/ folder
# - static/ folder
# - tests/ folder
# - main.py
# - requirements.txt
# - .env.example
# - All other files except venv/, __pycache__, *.db
```

### Step 2: Create Virtual Environment

**Linux/macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**

```cmd
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt
```

**If installation fails:**

```bash
# Install system dependencies (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install python3-dev build-essential

# Or on macOS with Homebrew
brew install python@3.11
```

### Step 4: Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your preferred editor
nano .env  # or vim, code, etc.
```

**Basic Configuration (.env):**

```bash
# Application Settings
APP_NAME="AI Insurance Assistant"
DEBUG=True
HOST=0.0.0.0
PORT=8000

# Database
DATABASE_URL=sqlite+aiosqlite:///./insurance_assistant.db

# AI Provider Configuration - Choose ONE:

# Option 1: Ollama (Local, Free)
MODEL_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=phi3:mini

# Option 2: Azure OpenAI (Cloud)
# MODEL_PROVIDER=azure
# AZURE_OPENAI_API_KEY=your_api_key_here
# AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
# AZURE_OPENAI_DEPLOYMENT=your-deployment-name

# Option 3: Fallback (No AI, Rule-based)
# MODEL_PROVIDER=fallback

# Response Settings
MAX_TOKENS=500
TEMPERATURE=0.7
```

### Step 5: Set Up AI Provider

#### Option A: Using Ollama (Recommended for Local)

1. **Install Ollama:**

   ```bash
   # Linux
   curl -fsSL https://ollama.com/install.sh | sh

   # macOS
   brew install ollama

   # Windows: Download from https://ollama.com/download
   ```

2. **Start Ollama service:**

   ```bash
   ollama serve
   ```

3. **Pull a model (in a new terminal):**

   ```bash
   ollama pull phi3:mini
   # or
   ollama pull llama2
   # or
   ollama pull mistral
   ```

4. **Verify Ollama:**
   ```bash
   curl http://localhost:11434/api/tags
   ```

#### Option B: Using Azure OpenAI

1. Get your Azure OpenAI credentials from Azure Portal
2. Update `.env` with:
   ```bash
   MODEL_PROVIDER=azure
   AZURE_OPENAI_API_KEY=your_actual_key
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
   AZURE_OPENAI_DEPLOYMENT=your_deployment_name
   ```

#### Option C: Using Fallback Mode

Simply set in `.env`:

```bash
MODEL_PROVIDER=fallback
```

No additional setup needed!

### Step 6: Initialize Database

The database will be created automatically on first run, but you can test:

```bash
# Test database connection
python -c "from app.services.database_service import init_db; import asyncio; asyncio.run(init_db())"
```

### Step 7: Start the Application

**Using startup scripts (Recommended):**

**Linux/macOS:**

```bash
chmod +x start.sh
./start.sh
```

**Windows:**

```cmd
start.bat
```

**Or start manually:**

```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Start the server
python main.py
```

### Step 8: Verify Deployment

1. **Check server is running:**

   ```bash
   curl http://localhost:8000/api/v1/health
   ```

   Expected response:

   ```json
   {
     "status": "healthy",
     "app_name": "AI Insurance Assistant",
     "version": "1.0.0",
     "model_provider": "ollama",
     "available_providers": {
       "fallback": true,
       "ollama": true,
       "azure": false
     }
   }
   ```

2. **Access the Web UI:**

   - Open browser: http://localhost:8000/static/index.html
   - You should see the AI Lady interface
   - Try the quick action buttons
   - Toggle light/dark theme

3. **Test API endpoints:**
   ```bash
   # Send a test message
   curl -X POST http://localhost:8000/api/v1/chat \
     -H "Content-Type: application/json" \
     -d '{"message": "What is life insurance?"}'
   ```

## 🔧 Configuration for Production

### Security Settings

1. **Disable debug mode:**

   ```bash
   DEBUG=False
   ```

2. **Use proper database:**

   ```bash
   # For production, consider PostgreSQL
   DATABASE_URL=postgresql+asyncpg://user:pass@localhost/dbname
   ```

3. **Add authentication** (if needed):
   - Implement API key authentication
   - Add user management system

### Performance Optimization

1. **Use production ASGI server:**

   ```bash
   pip install gunicorn
   gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

2. **Enable caching:**

   - Add Redis for session management
   - Cache frequent queries

3. **Database optimization:**
   - Regular backups
   - Index optimization

### Firewall Configuration

```bash
# Allow HTTP traffic
sudo ufw allow 8000/tcp

# Or use nginx reverse proxy
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

## 🐳 Docker Deployment

### Quick Docker Setup

1. **Build and run with Docker Compose:**

   ```bash
   docker-compose up -d
   ```

2. **View logs:**

   ```bash
   docker-compose logs -f
   ```

3. **Stop services:**
   ```bash
   docker-compose down
   ```

### Docker Configuration

Edit `docker-compose.yml` for your environment:

```yaml
environment:
  - MODEL_PROVIDER=ollama
  - OLLAMA_BASE_URL=http://host.docker.internal:11434
  # Or use Azure
  # - MODEL_PROVIDER=azure
  # - AZURE_OPENAI_API_KEY=${AZURE_OPENAI_API_KEY}
```

## 📊 Monitoring

### Health Checks

```bash
# Check API health
curl http://localhost:8000/api/v1/health

# Check database
ls -lh insurance_assistant.db

# Check logs
tail -f logs/app.log
```

### System Monitoring

```bash
# Check process
ps aux | grep python

# Check port
netstat -tuln | grep 8000

# Check resources
top -p $(pgrep -f "python main.py")
```

## 🔄 Updates and Maintenance

### Updating the Application

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Restart application
./start.sh
```

### Database Backups

```bash
# Backup SQLite database
cp insurance_assistant.db backups/insurance_assistant_$(date +%Y%m%d).db

# Restore from backup
cp backups/insurance_assistant_20251102.db insurance_assistant.db
```

## 🆘 Troubleshooting

### Common Issues

**1. "ModuleNotFoundError"**

```bash
# Reinstall dependencies
pip install -r requirements.txt
```

**2. "Port 8000 already in use"**

```bash
# Find and kill process
lsof -ti:8000 | xargs kill -9
# Or change port in .env
PORT=8001
```

**3. "Cannot connect to Ollama"**

```bash
# Check Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama if needed
ollama serve
```

**4. "Database is locked"**

```bash
# Stop all instances
pkill -f "python main.py"
# Remove lock if needed
rm insurance_assistant.db-journal
```

**5. "UI not loading"**

```bash
# Check static files exist
ls -la static/

# Check file permissions
chmod -R 755 static/
```

## 📝 Checklist for New Deployment

- [ ] Python 3.11+ installed
- [ ] Virtual environment created
- [ ] Dependencies installed (`requirements.txt`)
- [ ] `.env` file configured
- [ ] AI provider set up (Ollama/Azure/Fallback)
- [ ] Database initialized
- [ ] Server starts without errors
- [ ] Health endpoint responds
- [ ] Web UI loads correctly
- [ ] Can send chat messages
- [ ] Theme toggle works
- [ ] Firewall configured (if needed)
- [ ] Backups scheduled (for production)

## 🌐 Network Access

### Local Access Only

Default configuration - accessible only from localhost

### LAN Access

```bash
# In .env
HOST=0.0.0.0  # Already set by default
```

Access from other devices: `http://<your-ip>:8000/static/index.html`

### Internet Access (Production)

Use nginx reverse proxy:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 📧 Support

For issues or questions:

1. Check logs: `tail -f logs/app.log`
2. Verify configuration: `cat .env`
3. Test API: `curl http://localhost:8000/api/v1/health`
4. Review documentation: `README.md`, `SETUP.md`

---

**Last Updated**: November 2, 2025
**Version**: 2.0.0
