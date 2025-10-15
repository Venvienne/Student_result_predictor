# Student Result Predictor - Deployment Guide

## Architecture Overview

This application is split into two parts:
- **Frontend**: HTML/CSS/JavaScript (deployed on Vercel)
- **Backend**: Flask API (deployed on Render)

---

## Part 1: Deploy Backend to Render

### Step 1: Prepare Your Repository

Make sure these files are in your repository root:
- `backend_api.py` - Main Flask API
- `requirements.txt` - Python dependencies
- `render.yaml` - Render configuration
- `model/dt_model.joblib` - Trained ML model

### Step 2: Create Render Account

1. Go to [render.com](https://render.com)
2. Sign up with GitHub (recommended)
3. Authorize Render to access your repositories

### Step 3: Deploy on Render

1. **Click "New +" → "Web Service"**

2. **Connect your repository**
   - Select your `Student_result_predictor` repository

3. **Configure the service**:
   - **Name**: `student-predictor-api` (or your choice)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn backend_api:app`
   - **Plan**: Free (or your choice)

4. **Click "Create Web Service"**

5. **Wait for deployment** (usually 2-5 minutes)

6. **Copy your API URL**
   - It will look like: `https://student-predictor-api.onrender.com`
   - **SAVE THIS URL** - you'll need it for the frontend!

### Step 4: Test Your Backend

Visit these URLs (replace with your actual URL):
- `https://your-app.onrender.com/` - Should show API info
- `https://your-app.onrender.com/health` - Should show health status

---

## Part 2: Deploy Frontend to Vercel

### Step 1: Update API URL in Frontend

Before deploying, you MUST update the API URL in `frontend/index.html`:

1. Open `frontend/index.html`
2. Find this line (around line 97):
   ```javascript
   const API_URL = 'http://localhost:5000';
   ```
3. Replace it with your Render URL:
   ```javascript
   const API_URL = 'https://your-app.onrender.com';
   ```
4. Save the file

### Step 2: Deploy to Vercel

#### Option A: Using Vercel Dashboard (Easiest)

1. Go to [vercel.com](https://vercel.com)
2. Sign up/Login with GitHub
3. Click "Add New" → "Project"
4. Import your repository
5. **Configure Project**:
   - **Framework Preset**: Other
   - **Root Directory**: `frontend`
   - **Build Command**: (leave empty)
   - **Output Directory**: (leave empty)
6. Click "Deploy"
7. Wait for deployment (usually 30 seconds)

#### Option B: Using Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Navigate to frontend folder
cd frontend

# Login to Vercel
vercel login

# Deploy
vercel --prod
```

### Step 3: Test Your Frontend

1. Visit your Vercel URL (e.g., `https://your-app.vercel.app`)
2. Fill out the prediction form
3. Submit and check if you get results

---

## Testing the Complete Application

### Test Checklist:

1. ✅ **Backend Health Check**
   - Visit: `https://your-backend.onrender.com/health`
   - Should return: `{"status": "healthy", "model_loaded": true}`

2. ✅ **Frontend Loads**
   - Visit your Vercel URL
   - Form should display correctly

3. ✅ **Make a Prediction**
   - Fill out the form with test data:
     - Study hours: 6
     - Sleep hours: 7
     - Absences: 2
     - Assignments: 15
     - Exam score: 85
   - Click "Predict"
   - Should redirect to results page

4. ✅ **Results Display**
   - Should show prediction (Pass/Fail)
   - Should show confidence percentage
   - Should show input summary

---

## Troubleshooting

### Issue: "Failed to connect to the server"

**Cause**: Frontend can't reach backend API

**Solutions**:
1. Check that you updated the `API_URL` in `frontend/index.html`
2. Verify your Render backend is running (visit the health endpoint)
3. Check browser console for CORS errors
4. Make sure you redeployed frontend after updating API_URL

### Issue: Backend shows "Application failed to respond"

**Cause**: Backend deployment failed

**Solutions**:
1. Check Render logs for errors
2. Verify `model/dt_model.joblib` exists in repository
3. Check that all dependencies in `requirements.txt` installed correctly
4. Try redeploying the backend

### Issue: CORS Error in Browser Console

**Cause**: CORS not properly configured

**Solution**: The backend already has CORS enabled. If you still see this:
1. Make sure you're using HTTPS URLs (not HTTP)
2. Check that Flask-CORS is installed
3. Redeploy the backend

### Issue: Model not loading

**Cause**: Model file missing or path incorrect

**Solutions**:
1. Verify `model/dt_model.joblib` exists in your repository
2. Run `py train_model.py` to generate the model if missing
3. Commit and push the model file
4. Redeploy backend on Render

---

## Environment Variables (Optional)

If you want to make the API URL configurable:

### On Vercel:
1. Go to your project settings
2. Add environment variable:
   - Name: `VITE_API_URL`
   - Value: `https://your-backend.onrender.com`

### On Render:
No additional environment variables needed for basic setup.

---

## Local Development

### Running Backend Locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the backend
py backend_api.py
```

Backend will run on `http://localhost:5000`

### Running Frontend Locally:

1. Make sure `API_URL` in `frontend/index.html` is set to `http://localhost:5000`
2. Open `frontend/index.html` in your browser
3. Or use a local server:
   ```bash
   cd frontend
   python -m http.server 8000
   ```
   Then visit `http://localhost:8000`

---

## File Structure

```
student_result_predictor/
├── frontend/                    # Frontend (deploy to Vercel)
│   ├── index.html              # Main form page
│   ├── result.html             # Results page
│   ├── style.css               # Styling
│   └── vercel.json             # Vercel config
├── backend_api.py              # Flask API (deploy to Render)
├── requirements.txt            # Python dependencies
├── render.yaml                 # Render config
├── model/
│   └── dt_model.joblib         # ML model
└── DEPLOYMENT_GUIDE.md         # This file
```

---

## URLs to Remember

After deployment, save these URLs:

- **Frontend (Vercel)**: `https://your-app.vercel.app`
- **Backend (Render)**: `https://your-backend.onrender.com`
- **API Health Check**: `https://your-backend.onrender.com/health`
- **API Predict Endpoint**: `https://your-backend.onrender.com/predict`

---

## Next Steps

1. ✅ Deploy backend to Render
2. ✅ Copy backend URL
3. ✅ Update `API_URL` in `frontend/index.html`
4. ✅ Deploy frontend to Vercel
5. ✅ Test the application
6. 🎉 Share your app!

---

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review Render logs for backend errors
3. Check browser console for frontend errors
4. Verify all files are committed and pushed to Git

**Note**: Render free tier may have cold starts (15-30 seconds delay on first request after inactivity). This is normal!
