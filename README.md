# 🏢 Apartment Leasing Demo
**Real-Time Property Management System**

A production-quality demonstration of modern apartment leasing workflows with real-time data synchronization, automated lead prioritization, and comprehensive analytics.

**Portfolio Project for Apartment List**
Built by Matthew David Scott | [LinkedIn](https://linkedin.com/in/mscott77) | [GitHub](https://github.com/mscott77)

---

## 🎯 Project Overview

This demo showcases technical skills directly relevant to Apartment List's engineering environment:

- **Real-time Data Sync:** WebSocket-based instant updates across all connected clients
- **Automated Lead Scoring:** Rule-based algorithm prioritizing units by lease probability
- **Analytics Engine:** Conversion rates, trends, and KPIs calculated in real-time
- **Enterprise API Design:** FastAPI with automatic OpenAPI documentation
- **Scalable Architecture:** Cloud-ready, stateless design with Docker support

### Business Case Alignment

| **Apartment List Need** | **Demo Feature** | **Value** |
|-------------------------|------------------|-----------|
| Speed & Real-Time | WebSocket updates | Prevents double-bookings, instant UI refresh |
| Automation | Lead scoring (0-100) | Eliminates manual prioritization at scale |
| Data-Driven Decisions | Analytics dashboard | Informs pricing and marketing strategies |
| Integration-Ready | REST API + docs | Easy CRM, payment, background check integration |
| Cloud-First | Stateless design | Horizontally scalable to any cloud provider |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│           Frontend (React + Tailwind)           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │  Unit    │  │ Analytics│  │  Lead    │     │
│  │  List    │  │Dashboard │  │  Score   │     │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘     │
│       └─────────────┴──────────────┘            │
│              WebSocket + API Client             │
└─────────────────────┬───────────────────────────┘
                      │
                ↓ HTTP/WS ↓
                      │
┌─────────────────────┼───────────────────────────┐
│              Backend (FastAPI)                   │
│  ┌────────────┐  ┌────────────┐  ┌───────────┐ │
│  │   REST     │  │ WebSocket  │  │   Lead    │ │
│  │   API      │  │  Manager   │  │  Scoring  │ │
│  └──────┬─────┘  └──────┬─────┘  └─────┬─────┘ │
│         └────────────────┴───────────────┘       │
│                     ↓                            │
│          ┌──────────────────────┐                │
│          │  SQLite Database     │                │
│          │  (SQLAlchemy ORM)    │                │
│          └──────────────────────┘                │
└──────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+ (tested on 3.13)
- Node.js 18+ (for frontend)
- pip (Python package manager)

### Backend Setup

```bash
# Navigate to backend
cd backend

# Install dependencies
pip install -r requirements.txt

# Load seed data (creates database with 5 units)
python3 load_seed_data.py

# Start server
python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Server runs at:** http://localhost:8000
**API Docs:** http://localhost:8000/docs

### Frontend Setup (Coming Soon)

```bash
cd frontend
npm install
npm run dev
```

---

## 📡 API Endpoints

### Units Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/units` | List units (filterable by status, bedrooms, price) |
| GET | `/api/units/{id}` | Get specific unit details |
| POST | `/api/units` | Create new unit (admin) |
| PATCH | `/api/units/{id}` | Update unit (status, price, etc.) |
| DELETE | `/api/units/{id}` | Delete unit (admin) |

### Analytics

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/analytics` | Dashboard metrics (conversion rate, avg days to lease, etc.) |
| GET | `/api/analytics/trends` | Price trends over time |
| GET | `/api/analytics/distribution` | Bedroom/status/city distribution |
| GET | `/api/analytics/performance` | Key performance indicators (KPIs) |

### Lead Scoring

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/leads/score/{unit_id}` | Get lead score with breakdown |
| GET | `/api/leads/prioritized` | Get units sorted by lead score |
| POST | `/api/leads/recalculate` | Recalculate all scores (cron job) |

### Real-Time

| Protocol | Endpoint | Description |
|----------|----------|-------------|
| WebSocket | `/ws/units` | Real-time unit updates broadcast |

### System

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API health check |
| GET | `/health` | System health with database check |

---

## 🤖 Lead Scoring Algorithm

**Rule-Based AI for Unit Prioritization (0-100 Score)**

### Scoring Factors

1. **Price Competitiveness (±20 points)**
   - vs. market average
   - Great deal: +20, Overpriced: -15

2. **Listing Freshness (±15 points)**
   - Days since listed
   - Brand new (<3 days): +15
   - Stale (>45 days): -15

3. **Desirable Features (±20 points)**
   - High-value amenities
   - Parking, washer/dryer, pet-friendly weighted highest

4. **Unit Size Appeal (±15 points)**
   - Bedrooms, bathrooms, price per sq ft
   - 2-3 bedrooms score highest (demand)

5. **Location Desirability (±10 points)**
   - Louisville prime zip codes
   - 40202, 40204, 40206, 40207, 40222

### Example Breakdown

```json
{
  "unit_id": "apt-001",
  "lead_score": 82.5,
  "breakdown": {
    "price_competitiveness": +10,
    "listing_freshness": +15,
    "desirable_features": +18,
    "unit_size_appeal": +12,
    "location_desirability": +10
  },
  "explanation": [
    "Good value pricing",
    "Brand new listing (2 days)",
    "High-demand amenities (parking, washer/dryer)"
  ]
}
```

**Use Case:** Automatically prioritize which units to promote/market first based on likelihood to lease quickly.

---

## 📊 Analytics Metrics

### Dashboard Metrics

- **Total Units:** Inventory count by status
- **Average Days to Lease:** Time from listing to lease
- **Lease Conversion Rate:** % of units successfully leased
- **Average Price:** Market pricing trends
- **Most Popular Features:** Amenities in leased vs available units
- **Price Trends:** Rolling average over time

### Performance KPIs

- **Occupancy Rate:** Leased / Total units
- **Recent Leases (30d):** Velocity metric
- **Average Lead Score:** Overall inventory quality

---

## 🔥 Real-Time Updates

### WebSocket Flow

```
1. User leases unit → Frontend sends PATCH to API
2. Backend updates database → Returns updated unit
3. Backend broadcasts via WebSocket → All connected clients
4. All clients receive update → UI refreshes instantly
```

**Key Advantage:** No polling required, instant synchronization across all users.

### Testing Real-Time

**Terminal 1:** Connect WebSocket client
```bash
websocat ws://localhost:8000/ws/units
```

**Terminal 2:** Update a unit
```bash
curl -X PATCH http://localhost:8000/api/units/apt-001 \
  -H "Content-Type: application/json" \
  -d '{"status": "leased"}'
```

**Terminal 1:** See instant update broadcast!

---

## 🗄️ Database Schema

### Unit Model

| Field | Type | Description |
|-------|------|-------------|
| id | String (UUID) | Primary key |
| property_name | String | Property name |
| unit_number | String | Unit identifier |
| bedrooms | Integer | Number of bedrooms (0-4) |
| bathrooms | Float | Number of bathrooms |
| square_feet | Integer | Square footage |
| price | Integer | Monthly rent price |
| status | Enum | available, pending, leased |
| amenities | JSON Array | List of amenities |
| location | JSON Object | Address, city, state, zip, lat/lng |
| images | JSON Array | Image URLs |
| description | String | Unit description |
| lead_score | Float | Calculated score (0-100) |
| date_listed | DateTime | When unit was listed |
| date_leased | DateTime | When unit was leased (nullable) |

---

## 🛠️ Tech Stack

### Backend
- **FastAPI:** Modern async Python framework
- **SQLAlchemy:** ORM for database operations
- **Pydantic:** Request/response validation
- **WebSockets:** Real-time bidirectional communication
- **SQLite:** Embedded database (prod: PostgreSQL)
- **Uvicorn:** ASGI server

### Frontend (In Progress)
- **React:** Component-based UI
- **Vite:** Fast build tooling
- **Tailwind CSS:** Utility-first styling
- **Chart.js:** Data visualization
- **Axios:** HTTP client

### Infrastructure
- **Docker:** Containerization
- **docker-compose:** Multi-container orchestration
- **Git:** Version control

---

## 📁 Project Structure

```
apartment-leasing-demo/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI app + routes
│   │   ├── models.py               # SQLAlchemy ORM models
│   │   ├── schemas.py              # Pydantic validation schemas
│   │   ├── database.py             # Database connection
│   │   ├── crud.py                 # CRUD operations
│   │   ├── lead_scoring.py         # Lead scoring algorithm
│   │   ├── analytics.py            # Analytics calculations
│   │   └── websocket_manager.py    # WebSocket connection manager
│   ├── data/
│   │   ├── seed_data.json          # Mock apartment units
│   │   └── generate_seed.py        # Seed data generator
│   ├── load_seed_data.py           # Database loader
│   └── requirements.txt            # Python dependencies
├── frontend/                       # React app (coming soon)
├── docs/                           # Documentation
├── README.md                       # This file
├── TESTING.md                      # Testing guide
└── docker-compose.yml              # Container orchestration

```

---

## ✅ Current Status

### Completed (Day 1)
- ✅ FastAPI backend with all endpoints
- ✅ SQLite database with SQLAlchemy ORM
- ✅ WebSocket manager for real-time updates
- ✅ Lead scoring algorithm (rule-based)
- ✅ Analytics engine (8 metric types)
- ✅ CRUD operations with filtering
- ✅ Pydantic validation schemas
- ✅ Seed data (5 Louisville apartments)
- ✅ Git repository initialized
- ✅ Documentation (README, TESTING)

### In Progress (Day 2-3)
- 🔄 React frontend with Tailwind CSS
- 🔄 Real-time UI updates via WebSocket
- 🔄 Analytics dashboard with Chart.js
- 🔄 Docker containerization
- 🔄 Comprehensive unit tests

### Future Enhancements
- 📅 User authentication (JWT)
- 📅 Admin dashboard
- 📅 Email notifications
- 📅 Payment integration simulation
- 📅 Cloud deployment (AWS/Heroku)

---

## 🎓 Key Learning Demonstrations

### For Apartment List Reviewers

1. **Real-Time Systems:** WebSocket architecture prevents race conditions in high-velocity environments
2. **Automation Thinking:** Lead scoring shows understanding of ML workflow (features → weights → predictions)
3. **API Design:** OpenAPI docs, proper HTTP methods, RESTful conventions
4. **Database Design:** Normalized schema, indexes on filtered fields, JSON for flexible data
5. **Business Logic:** Analytics calculations directly support data-driven decision-making
6. **Code Quality:** Type hints, docstrings, clear separation of concerns
7. **Documentation:** Comprehensive, example-driven, assumes technical audience

---

## 📞 Contact

**Matthew David Scott**
- LinkedIn: [linkedin.com/in/mscott77](https://linkedin.com/in/mscott77)
- GitHub: [github.com/mscott77](https://github.com/mscott77)
- Email: matthewdscott7@gmail.com

---

## 📄 License

This is a portfolio demonstration project. Code is provided as-is for evaluation purposes.

**Note:** This demo uses mock data. No real apartment listings or personal information included.

---

*🤖 Generated with Claude Code*
*Co-Authored-By: Claude <noreply@anthropic.com>*
