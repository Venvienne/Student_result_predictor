# Quick Start - Separated Frontend & Backend

## What Changed?

Your application is now split into:
- **Frontend** (HTML/CSS/JS) → Deploy to **Vercel**
- **Backend** (Flask API) → Deploy to **Render**

## Files Created

### Frontend (in `frontend/` folder):
- `index.html` - Prediction form
- `result.html` - Results page  
- `style.css` - Styling
- `vercel.json` - Vercel config
- `README.md` - Frontend instructions

### Backend (in root):
- `backend_api.py` - Flask API with CORS
- `render.yaml` - Render config
- `requirements.txt` - Updated with Flask-CORS and gunicorn

### Documentation:
- `DEPLOYMENT_GUIDE.md` - Complete step-by-step guide
- `QUICK_START.md` - This file

---

## Deployment Steps (Simple Version)

### Step 1: Deploy Backend to Render (5 minutes)

1. Go to [render.com](https://render.com) and sign up
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn backend_api:app`
5. Click "Create Web Service"
6. **COPY YOUR BACKEND URL** (e.g., `https://student-predictor-api.onrender.com`)

### Step 2: Update Frontend API URL (1 minute)

1. Open `frontend/index.html`
2. Find line ~97: `const API_URL = 'http://localhost:5000';`
3. Replace with: `const API_URL = 'https://YOUR-RENDER-URL.onrender.com';`
4. Save and commit the change

### Step 3: Deploy Frontend to Vercel (2 minutes)

1. Go to [vercel.com](https://vercel.com) and sign up
2. Click "Add New" → "Project"
3. Import your repository
4. Set **Root Directory** to `frontend`
5. Click "Deploy"

### Step 4: Test! 🎉

Visit your Vercel URL and try making a prediction!

---

## Important Notes

⚠️ **You MUST update the API_URL in `frontend/index.html` before deploying to Vercel!**

⚠️ **Make sure `model/dt_model.joblib` exists in your repository before deploying to Render!**

If the model file is missing, run:
```bash
py train_model.py
```

---

## Testing Locally

### Backend:
```bash
py backend_api.py
```
Runs on `http://localhost:5000`

### Frontend:
1. Set `API_URL` to `http://localhost:5000` in `frontend/index.html`
2. Open `frontend/index.html` in browser

---

## Need Help?

See `DEPLOYMENT_GUIDE.md` for detailed instructions and troubleshooting!

---

## Why This Approach?

✅ **Solves the Vercel 404 issue** - Vercel hosts static files (what it's best at)
✅ **Better performance** - Render is optimized for Python/Flask apps  
✅ **Easier to debug** - Frontend and backend are separate
✅ **More scalable** - Can update frontend/backend independently
✅ **Free tier available** - Both Vercel and Render have free tiers
