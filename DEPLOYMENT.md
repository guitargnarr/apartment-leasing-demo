# LeaseFlow Deployment Guide

## 🚀 Quick Deploy Options

### Option 1: Vercel (Recommended for Frontend)

#### Via GitHub Integration (Easiest)
1. Go to [vercel.com](https://vercel.com)
2. Click "Import Project"
3. Connect your GitHub repository: `guitargnarr/apartment-leasing-demo`
4. Configure:
   - **Framework Preset:** Vite
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
   - **Environment Variables:**
     - `VITE_API_URL` = Your backend URL (see below)

#### Via CLI
```bash
cd frontend
npm install -g vercel
vercel --prod
```

---

### Option 2: Render.com (Recommended for Backend)

#### Deploy Backend API
1. Go to [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect GitHub repository: `guitargnarr/apartment-leasing-demo`
4. Configure:
   - **Name:** leaseflow-api
   - **Root Directory:** `backend`
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan:** Free
5. Add Environment Variables:
   - `DATABASE_URL` = (Render provides free PostgreSQL, or use SQLite)
   - `PYTHON_VERSION` = `3.11.0`

**Your backend will be at:** `https://leaseflow-api.onrender.com`

#### Deploy Frontend (Alternative)
1. Same process but configure:
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Publish Directory:** `dist`

---

### Option 3: Railway.app (One-Click Deploy)

#### Backend
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template)

1. Click "Deploy on Railway"
2. Connect GitHub: `guitargnarr/apartment-leasing-demo`
3. Railway auto-detects Python app
4. Set root to `backend`
5. Deploy!

---

### Option 4: Netlify (Alternative for Frontend)

#### Via GitHub Integration
1. Go to [netlify.com](https://netlify.com)
2. Click "Add new site" → "Import an existing project"
3. Connect GitHub: `guitargnarr/apartment-leasing-demo`
4. Configure:
   - **Base directory:** `frontend`
   - **Build command:** `npm run build`
   - **Publish directory:** `frontend/dist`
   - **Environment variables:**
     - `VITE_API_URL` = Your backend URL

---

## 📝 Complete Deployment Workflow

### Step 1: Deploy Backend First
```bash
# Option A: Render.com (Recommended)
- Follow Render instructions above
- Note your backend URL: https://leaseflow-api.onrender.com

# Option B: Railway.app
- One-click deploy from dashboard
- Note your backend URL: https://leaseflow-production.up.railway.app
```

### Step 2: Deploy Frontend
```bash
# Update frontend environment variable
cd frontend
echo "VITE_API_URL=https://your-backend-url.onrender.com" > .env.production

# Deploy to Vercel
vercel --prod

# Or deploy via GitHub integration (easier)
```

### Step 3: Load Seed Data
```bash
# SSH into your backend deployment or use local connection
# Render.com provides shell access

# Run seed data script
cd backend
python load_seed_data.py
```

### Step 4: Verify Deployment
```bash
# Test backend
curl https://your-backend-url.onrender.com/health

# Test frontend
open https://your-frontend.vercel.app
```

---

## 🔧 Configuration Files Included

### For Vercel (Frontend)
- ✅ `vercel.json` - Configured with API routing
- ✅ `frontend/package.json` - Build scripts ready
- ✅ `frontend/.env.example` - Environment template

### For Render (Backend)
- ✅ `render.yaml` - Service configuration (see below)
- ✅ `backend/requirements.txt` - Dependencies specified
- ✅ Environment variables documented

### For Railway (Backend)
- ✅ Auto-detected from `requirements.txt`
- ✅ Dockerfile optional (Railway auto-generates)

---

## 🌐 Expected URLs After Deployment

**Production URLs:**
- Frontend: `https://leaseflow.vercel.app`
- Backend API: `https://leaseflow-api.onrender.com`
- API Docs: `https://leaseflow-api.onrender.com/docs`

---

## ⚡ Free Tier Limits

### Vercel (Frontend)
- ✅ 100GB bandwidth/month
- ✅ Unlimited deployments
- ✅ Custom domains
- ✅ Automatic HTTPS

### Render (Backend)
- ✅ 750 hours/month (enough for 1 service)
- ⚠️ Spins down after 15 min inactivity (cold starts)
- ✅ Free PostgreSQL database (90 days)
- ✅ Automatic HTTPS

### Railway (Alternative)
- ✅ $5 free credit/month
- ✅ No cold starts
- ✅ Better for demos

---

## 🐛 Troubleshooting

### Backend not starting on Render
```bash
# Check logs in Render dashboard
# Common issues:
# 1. Port not set correctly → Use $PORT env variable
# 2. Missing dependencies → Verify requirements.txt
# 3. Database connection → Check DATABASE_URL
```

### Frontend can't connect to API
```bash
# Check CORS settings in backend/app/main.py
# Ensure your frontend URL is in allow_origins
# Or use allow_origins=["*"] for testing
```

### Cold starts on Render Free Tier
```bash
# First request after 15 min will be slow (30s+)
# Upgrade to paid tier ($7/month) to eliminate
# Or use Railway for better free tier experience
```

---

## 📊 Monitoring

### Backend Health
- Health endpoint: `https://your-api.onrender.com/health`
- API docs: `https://your-api.onrender.com/docs`
- Logs: Render dashboard → Your service → Logs

### Frontend Analytics
- Vercel provides built-in analytics
- View at: Vercel dashboard → Your project → Analytics

---

## 🔐 Security Notes

**Before deploying to production:**
1. ❌ Remove `allow_origins=["*"]` from CORS
2. ✅ Add specific frontend URL to CORS
3. ✅ Set `ENVIRONMENT=production` env variable
4. ✅ Use strong database credentials (if PostgreSQL)
5. ✅ Review all environment variables
6. ✅ Consider adding rate limiting

---

## 📞 Support

**Deployment Issues:**
- Vercel: [vercel.com/docs](https://vercel.com/docs)
- Render: [render.com/docs](https://render.com/docs)
- Railway: [docs.railway.app](https://docs.railway.app)

**Project Issues:**
- GitHub: https://github.com/guitargnarr/apartment-leasing-demo/issues

---

**🎉 Your LeaseFlow deployment is ready to go live!**
