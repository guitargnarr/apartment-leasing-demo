#!/bin/bash
# Backend verification script

echo "🔍 Testing Apartment Leasing Backend"
echo "===================================="
echo ""

# Check Python version
echo "1️⃣  Checking Python version..."
python3 --version
echo ""

# Check if in correct directory
if [ ! -f "app/main.py" ]; then
    echo "❌ Error: Must run from backend/ directory"
    exit 1
fi

# Check dependencies
echo "2️⃣  Checking Python dependencies..."
python3 -c "
try:
    import fastapi
    import uvicorn
    import sqlalchemy
    import pydantic
    print('✅ All core dependencies installed')
except ImportError as e:
    print(f'❌ Missing dependency: {e}')
    print('Run: pip install -r requirements.txt')
    exit(1)
"
echo ""

# Generate seed data if needed
echo "3️⃣  Checking seed data..."
if [ ! -f "data/seed_data.json" ] || [ $(wc -l < data/seed_data.json) -lt 50 ]; then
    echo "📝 Generating fresh seed data..."
    cd data && python3 generate_seed.py && cd ..
else
    echo "✅ Seed data file exists ($(wc -l < data/seed_data.json) lines)"
fi
echo ""

# Load seed data into database
echo "4️⃣  Loading seed data into database..."
python3 load_seed_data.py <<< "y"
echo ""

# Start server in background
echo "5️⃣  Starting FastAPI server..."
echo "   Server will run at: http://localhost:8000"
echo "   API docs at: http://localhost:8000/docs"
echo "   Press Ctrl+C to stop server"
echo ""

# Run server
python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
