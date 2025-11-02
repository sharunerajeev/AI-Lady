# Changelog

All notable changes to the AI Insurance Assistant project.

## [2.1.0] - November 2, 2025

### 🎯 AI Accuracy & Security Improvements

#### Added

- **Enhanced Azure OpenAI Prompts**

  - Structured system prompts with CRITICAL RULES section
  - Few-shot examples showing correct response patterns
  - Response quality standards (length, tone, format)
  - Explicit knowledge base citation instructions
  - Better context building with top 5 FAQs (up from 3)
  - Relevance scores included in context
  - Priority weighting for high-importance knowledge

- **Security Guardrails**

  - Prompt injection detection (blocks malicious attempts)
  - Topic validation (ensures insurance-related queries)
  - Off-topic redirection with helpful messaging
  - Input sanitization with regex patterns
  - Blocked patterns: ignore instructions, system commands, code injection

- **Knowledge Base Management System**

  - New `knowledge_base/` directory for company-specific content
  - JSON-based knowledge format (easy to edit)
  - Support for multiple knowledge sources:
    - `company_info.json` - Company details and contact
    - `products/*.json` - Product-specific information
    - `policies/*.json` - Process and policy documentation
  - Automatic loading of custom knowledge on startup
  - Admin API endpoints:
    - `POST /api/v1/admin/knowledge/reload` - Reload without restart
    - `GET /api/v1/admin/knowledge/stats` - View knowledge statistics

- **Documentation**
  - New `ACCURACY_AND_SECURITY_GUIDE.md` - Complete guide for:
    - Azure OpenAI accuracy optimization
    - Knowledge base management
    - Security guardrails and testing
  - Updated `knowledge_base/README.md` - Knowledge authoring guide
  - Enhanced `.gitignore` to protect company-specific knowledge

#### Changed

- **AI Service (`ai_service.py`)**

  - Added `_validate_insurance_query()` for input validation
  - Enhanced `_build_context_prompt()` with structured format
  - Increased FAQ context from 3 to 5 items
  - Added priority-based ranking in search results

- **Vector Service (`vector_service.py`)**

  - Added JSON knowledge file loading
  - Support for priority field (`high`, `medium`, `low`)
  - Multi-source knowledge aggregation
  - `reload_knowledge_base()` method for hot-reload

- **API Routes (`routes.py`)**
  - Added admin knowledge management endpoints
  - Knowledge stats endpoint for monitoring

#### Security

- **Threat Protection**
  - Blocked: prompt injection, system commands, code execution
  - Validated: all queries checked for insurance relevance
  - Redirected: off-topic queries with helpful guidance
- **Response Boundaries**
  - AI instructed to refuse political/controversial topics
  - No code execution or calculations unrelated to insurance
  - Explicit boundaries in system prompts

#### Technical Details

- Knowledge base auto-loads from `knowledge_base/` on startup
- Default FAQs combined with custom knowledge
- Priority boosting: high (+0.15), medium (+0.05), low (+0.0)
- Security validation happens before AI processing
- Graceful fallback on validation failures

---

## [2.0.0] - November 2, 2025

### 🎨 Major UI Overhaul

#### Added

- **Modern Web Interface**
  - Custom HTML/CSS/JavaScript replacing Gradio
  - Integrated directly into FastAPI (no separate frontend server)
  - Modular code structure with separated concerns
- **Design System**

  - Light/Dark theme support with smooth transitions
  - Google Material Icons throughout the interface
  - Uniform Noto Sans typography
  - CSS variables for consistent theming
  - Increased border radius for modern, softer look

- **User Experience Enhancements**

  - Quick action buttons for common queries
  - Live system status monitoring with hover tooltips
  - Typing indicators during AI processing
  - Metadata tooltips on bot messages (provider, model, time, cost)
  - Generic user icon for better professionalism
  - Responsive design for mobile and desktop
  - Smooth animations and transitions

- **Layout Improvements**
  - Compact header (reduced by ~20%)
  - Professional footer with links
  - Quick actions repositioned above chat input
  - Better contrast in light mode for improved readability

#### Changed

- **Architecture**
  - Frontend now served from `/static/` directory
  - UI accessible at `http://localhost:8000/static/index.html`
  - Single server deployment (FastAPI serves both API and UI)
- **Code Organization**

  - Separated CSS into `static/styles.css` (~750 lines)
  - Separated JavaScript into `static/script.js` (~400 lines)
  - Clean HTML structure in `static/index.html` (~175 lines)

- **Documentation**
  - Updated README.md with v2.0 features
  - Added new UI architecture diagrams
  - Updated configuration guide for multi-provider support
  - Improved troubleshooting section

#### Removed

- Removed redundant documentation files:
  - `UI_MIGRATION_GUIDE.md`
  - `TESTING_SUMMARY.md`
  - `UI_REFACTOR_SUMMARY.md`
  - `frontend.py.backup`

#### Technical Details

- **Frontend Stack**

  - HTML5 with semantic markup
  - CSS3 with custom properties (variables)
  - Vanilla JavaScript (no framework dependencies)
  - Google Material Icons
  - Fully responsive design

- **Provider Support**
  - Ollama (local LLM)
  - Azure OpenAI (cloud-based)
  - Fallback mode (rule-based)

---

## [1.0.0] - November 2025

### Initial Release

#### Added

- FastAPI backend with RESTful API
- Gradio-based web interface
- OpenAI integration for AI responses
- SQLite database for conversation storage
- RAG-based FAQ retrieval system
- Session management
- Docker support
- Conversation history tracking
- Response rating system

#### Features

- Customer support FAQ chatbot
- Natural language understanding
- Context-aware responses
- Multi-turn dialogue support
- Health check endpoints
- API documentation (Swagger/ReDoc)

---

## Migration Notes

### From v1.0 to v2.0

**UI Changes:**

- Old Gradio UI (port 7860) → New HTML UI (served from port 8000)
- Access URL changed: `http://localhost:7860` → `http://localhost:8000/static/index.html`
- No separate frontend server needed

**Configuration:**

- Multi-provider support added
- New environment variables:
  - `MODEL_PROVIDER` (ollama, azure, fallback)
  - `OLLAMA_BASE_URL`
  - `AZURE_OPENAI_*` settings

**Removed:**

- Dependency on Gradio library (frontend.py still available but deprecated)
- Separate frontend server requirement

**Preserved:**

- All API endpoints remain unchanged
- Database schema unchanged
- Docker deployment process unchanged
- All backend functionality preserved

---

## Known Issues

None reported for v2.0.0

## Upcoming Features

- [ ] File upload support for policy documents
- [ ] Voice input/output
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Export conversation history
- [ ] Custom themes and branding
