# 🚀 Quick Setup Guide

## Prerequisites

- Python 3.11 or higher installed
- Git (optional)
- OpenAI API key (optional, has fallback mode)

## Step-by-Step Setup

### 1. Initial Setup

```bash
# Navigate to project directory
cd "AI Lady"

# Create .env file
cp .env.example .env

# (Optional) Edit .env and add your OpenAI API key
# nano .env  # or use any text editor
```

### 2. Running the Application

#### Option A: Using Startup Script (Recommended)

```bash
# Make script executable (Linux/Mac only, already done)
chmod +x start.sh

# Run the startup script
./start.sh

# On Windows, run:
# start.bat
```

#### Option B: Manual Setup

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Start API (in one terminal)
python main.py

# Start Frontend (in another terminal)
python frontend.py
```

#### Option C: Using Docker

```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### 3. Access the Application

- **Gradio UI**: http://localhost:7860
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/v1/health

## Troubleshooting

### Issue: Port already in use

```bash
# Find and kill process on port 8000
lsof -ti:8000 | xargs kill -9  # Linux/Mac
# netstat -ano | findstr :8000  # Windows

# Find and kill process on port 7860
lsof -ti:7860 | xargs kill -9  # Linux/Mac
```

### Issue: Missing dependencies

```bash
# Update pip
pip install --upgrade pip

# Reinstall requirements
pip install -r requirements.txt
```

### Issue: OpenAI API key not working

- Check if key is correctly set in `.env` file
- The app works in fallback mode without OpenAI API key
- Responses will use vector similarity search instead

## Testing

### Test API

```bash
# Check health
curl http://localhost:8000/api/v1/health

# Send a message
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is life insurance?"}'
```

### Run Tests

```bash
# Activate virtual environment first
source venv/bin/activate

# Run pytest
pytest tests/
```

## Next Steps

1. **Configure OpenAI** (Optional)

   - Get API key from https://platform.openai.com/api-keys
   - Add to `.env` file: `OPENAI_API_KEY=sk-...`

2. **Try Sample Questions**

   - What is term life insurance?
   - How do I file a claim?
   - What does homeowners insurance cover?

3. **Explore API Documentation**

   - Visit http://localhost:8000/docs
   - Try different endpoints

4. **Customize**
   - Add more FAQs in `data/insurance_faq.py`
   - Modify UI in `frontend.py`
   - Adjust AI behavior in `app/services/ai_service.py`

## Support

For issues or questions:

- Check README.md for detailed documentation
- Review troubleshooting section above
- Check API logs for errors

---

**Happy Insurance Assisting! 🎉**
