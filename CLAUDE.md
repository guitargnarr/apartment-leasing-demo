# CLAUDE.md - apartment-leasing-demo

# Memory System: ~/.claude/memories/

## Project Overview
**Portfolio demonstration project** - Full-stack apartment leasing platform with real-time lead scoring, analytics dashboard, and WebSocket notifications.

**Tech Stack:**
- **Backend:** FastAPI, SQLAlchemy, SQLite, WebSockets
- **Frontend:** React + Vite, TailwindCSS (to be built)
- **Features:** Lead scoring algorithm, analytics engine, real-time updates

## Key Metrics
- **Status:** Active Development
- **Language:** Python 3.14.0 (backend), TypeScript/React (frontend)
- **Started:** October 2025
- **Purpose:** Apartment List job application portfolio piece

---

## ✅ Python Environment (Updated October 22, 2025)

**VERIFIED:** Python 3.14.0 installed and working correctly

### Current Setup

**Python Version:** 3.14.0
- **Location:** `/Library/Frameworks/Python.framework/Versions/3.14/bin/python3`
- **Virtual Environment:** `~/Projects/Portfolio/apartment-leasing-demo/backend/venv`
- **Status:** ✅ Fully operational

### Verification (Run at project start)

```bash
cd ~/Projects/Portfolio/apartment-leasing-demo/backend
source venv/bin/activate
python --version  # Should show: Python 3.14.0
```

**If verification fails:** See global CLAUDE.md (~/.claude/CLAUDE.md) for troubleshooting

---

## Project Structure

```
apartment-leasing-demo/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application entry point
│   │   ├── models.py            # SQLAlchemy ORM models
│   │   ├── schemas.py           # Pydantic schemas
│   │   ├── database.py          # Database configuration
│   │   ├── crud.py              # CRUD operations
│   │   ├── lead_scoring.py      # Lead scoring algorithm
│   │   ├── analytics.py         # Analytics engine
│   │   └── websocket_manager.py # Real-time WebSocket manager
│   ├── tests/                   # Test suite
│   ├── load_seed_data.py        # Seed data generator
│   ├── requirements.txt         # Python dependencies
│   ├── .env                     # Environment configuration
│   └── venv/                    # Virtual environment
└── frontend/                    # React frontend (to be built)
```

---

## Backend Setup Commands

### Start Development Server

```bash
cd ~/Projects/Portfolio/apartment-leasing-demo/backend

# Activate virtual environment
source venv/bin/activate

# IMPORTANT: Unset global DATABASE_URL (PostgreSQL conflict)
unset DATABASE_URL

# Start backend with hot reload
python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Access API Documentation:** http://localhost:8000/docs

### Load Seed Data

```bash
cd ~/Projects/Portfolio/apartment-leasing-demo/backend
source venv/bin/activate
unset DATABASE_URL
python3 load_seed_data.py
```

### Run Tests

```bash
cd ~/Projects/Portfolio/apartment-leasing-demo/backend
source venv/bin/activate
pytest tests/ -v
```

---

## Dependencies (Updated for Python 3.14)

**Core Framework:**
- `fastapi==0.109.0` (works on Python 3.14, upgrade to 0.115.8+ recommended)
- `uvicorn[standard]==0.27.0`
- `python-multipart==0.0.6`

**Database:**
- `sqlalchemy==2.0.44` (upgraded from 2.0.25 for Python 3.14 compatibility)
- `aiosqlite==0.19.0`

**Data Validation:**
- `pydantic==2.12.3` (upgraded from 2.5.3 for Python 3.14 compatibility)
- `pydantic-settings==2.11.0`

**WebSocket & Real-time:**
- `websockets==12.0`

**Testing:**
- `pytest==7.4.4`
- `pytest-asyncio==0.23.3`
- `httpx==0.26.0`

**Configuration:**
- `python-dotenv==1.0.0`

---

## Known Issues & Solutions

### 1. Global DATABASE_URL Override

**Problem:** Global environment variable `DATABASE_URL=postgresql://localhost:5432/fretforge` overrides project's SQLite configuration.

**Solution:**
```bash
# Always run before starting backend
unset DATABASE_URL
```

**Permanent Fix:** Remove global DATABASE_URL from shell config or make it project-specific.

### 2. Package Compatibility with Python 3.14

**Resolved October 22, 2025:**
- Upgraded `pydantic` to 2.12.3 (has Python 3.14 wheels)
- Upgraded `sqlalchemy` to 2.0.44 (Python 3.14 compatible)
- All dependencies now working on Python 3.14.0

---

## API Endpoints

### Leads Management
- `POST /leads/` - Create new lead
- `GET /leads/` - Get all leads (with filtering)
- `GET /leads/{lead_id}` - Get specific lead
- `PUT /leads/{lead_id}` - Update lead
- `DELETE /leads/{lead_id}` - Delete lead

### Tours
- `POST /tours/` - Schedule tour
- `GET /tours/` - Get all tours
- `PUT /tours/{tour_id}` - Update tour status

### Analytics
- `GET /analytics/dashboard` - Get dashboard metrics
- `GET /analytics/lead-distribution` - Get lead score distribution
- `GET /analytics/conversion-funnel` - Get conversion funnel data
- `GET /analytics/trends` - Get weekly trends

### WebSocket
- `WS /ws/updates` - Real-time lead updates

---

## Lead Scoring Algorithm

**Inputs:**
- Move-in urgency (0-30 days = high score)
- Budget alignment (closer to property rent = higher score)
- Contact method (phone > email > web form)
- Tour scheduling (scheduled > not scheduled)

**Output:** Score 0-100
- **Hot (80-100):** Immediate follow-up required
- **Warm (50-79):** Follow-up within 24 hours
- **Cold (0-49):** Standard follow-up

**Implementation:** `app/lead_scoring.py`

---

## Project-Specific Rules

### Code Style
- FastAPI async patterns for all endpoints
- Pydantic schemas for data validation
- SQLAlchemy ORM for database operations
- Type hints on all functions
- Docstrings for all public functions

### Testing Requirements
- Test all CRUD operations
- Test lead scoring algorithm
- Test analytics calculations
- Test WebSocket connections
- Maintain >80% code coverage

### Database
- SQLite for local development
- Seed data includes realistic apartment leads
- Database file: `apartment_leasing.db`

---

## Development Workflow

### 1. Environment Setup (First Time)
```bash
cd ~/Projects/Portfolio/apartment-leasing-demo/backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Daily Development
```bash
cd ~/Projects/Portfolio/apartment-leasing-demo/backend
source venv/bin/activate
unset DATABASE_URL
python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Before Committing
```bash
# Run tests
pytest tests/ -v

# Check code quality (if installed)
black app/
flake8 app/

# Update requirements if needed
pip freeze > requirements.txt
```

---

## Next Steps (TODO)

- [ ] Build React frontend with Vite
- [ ] Implement analytics dashboard visualizations
- [ ] Add authentication (optional for demo)
- [ ] Docker containerization
- [ ] Deployment documentation
- [ ] Final demo video/screenshots

---

## Performance & Security Notes

**Performance:**
- SQLite is sufficient for demo purposes
- WebSocket manager handles concurrent connections
- Analytics queries optimized with proper indexing

**Security:**
- CORS configured for local development
- Input validation via Pydantic schemas
- SQL injection prevention via SQLAlchemy ORM
- For production: Add authentication, rate limiting, HTTPS

---

## 🎓 Project-Specific Lessons Learned (October 22, 2025)

### Critical Issue Resolved: DATABASE_URL Global Override

**Problem Encountered:**
- Backend failed to start with "ModuleNotFoundError: No module named 'psycopg2'"
- Despite `.env` file correctly set to SQLite, app tried connecting to PostgreSQL

**Root Cause:**
- Global `DATABASE_URL` variable in `~/.zshrc` (line 137) was overriding project's `.env` file
- Variable set for different project (fretforge) remained in global environment

**Solution:**
```bash
# Line 137 in ~/.zshrc now commented out
# export DATABASE_URL='postgresql://localhost:5432/fretforge'

# Workaround for existing sessions:
unset DATABASE_URL  # Run before starting backend
```

**Lesson:**
- Global environment variables ALWAYS override `.env` files in Python
- Before debugging database connection errors, check: `echo $DATABASE_URL`
- Never set project-specific variables globally - use project activation scripts

---

### Python 3.14 Package Compatibility Success

**Packages Upgraded for Python 3.14:**
- `pydantic` 2.5.3 → 2.12.3 (original version lacked Python 3.14 wheels)
- `sqlalchemy` 2.0.25 → 2.0.44 (compatibility improvement)

**Result:**
✅ All dependencies installed successfully with Python 3.14.0
✅ Backend starts and runs without errors
✅ Seed data loads correctly
✅ API endpoints functional

**Takeaway:**
- Python 3.14 is viable for modern FastAPI projects
- May need to upgrade pinned package versions for Python 3.14 compatibility
- Always test `pip install -r requirements.txt` after Python version changes

---

### Seed Data Loading Success Pattern

**Working Command:**
```bash
cd ~/Projects/Portfolio/apartment-leasing-demo/backend
source venv/bin/activate
unset DATABASE_URL  # Critical: unset global override
python3 load_seed_data.py
```

**Output:**
```
Creating database tables...
✅ Tables created
Loading seed data from .../data/seed_data.json...
✅ Successfully loaded 5 units into database
   📊 Available: 3
   ⏳ Pending: 1
   ✅ Leased: 1
```

**Key Success Factors:**
1. Virtual environment activated
2. Global DATABASE_URL unset
3. Python 3.14 with upgraded packages
4. SQLite path correctly specified in .env

---

### Startup Checklist for This Project

**Every time you start working on this project:**

```bash
# 1. Navigate and activate
cd ~/Projects/Portfolio/apartment-leasing-demo/backend
source venv/bin/activate

# 2. Clear global variable override
unset DATABASE_URL

# 3. Verify Python environment
python --version  # Should show: Python 3.14.0

# 4. Start backend
python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Access: http://localhost:8000/docs
```

**If backend fails to start:**
- Check DATABASE_URL: `echo $DATABASE_URL` (should be empty)
- Verify venv: `which python` (should point to venv/bin/python)
- Check .env file exists: `ls -la .env`
- Verify database file: `ls -la apartment_leasing.db`

---

**Documentation Status:** ✅ Complete
**Last Updated:** October 22, 2025 (Evening - Added Lessons Learned)
**Python Environment:** ✅ Verified working (Python 3.14.0)
**Backend Status:** ✅ Running successfully
**Frontend Status:** 🔄 To be built
**Critical Issues:** ✅ All resolved (DATABASE_URL fixed)
