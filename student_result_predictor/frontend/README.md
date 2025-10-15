# Student Result Predictor - Frontend

## Quick Setup

### 1. Update API URL

Before deploying, open `index.html` and update the API URL (line ~97):

```javascript
const API_URL = 'https://your-backend-url.onrender.com';
```

Replace `your-backend-url.onrender.com` with your actual Render backend URL.

### 2. Deploy to Vercel

#### Using Vercel Dashboard:
1. Go to [vercel.com](https://vercel.com)
2. Import your repository
3. Set **Root Directory** to `frontend`
4. Deploy!

#### Using Vercel CLI:
```bash
cd frontend
vercel --prod
```

## Files

- `index.html` - Main prediction form
- `result.html` - Results display page
- `style.css` - Styling
- `vercel.json` - Vercel configuration

## Local Testing

1. Update `API_URL` in `index.html` to `http://localhost:5000`
2. Make sure backend is running
3. Open `index.html` in your browser

Or use a local server:
```bash
python -m http.server 8000
```

Then visit `http://localhost:8000`
