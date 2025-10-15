# Student Result Predictor - Vercel Deployment

This Flask application predicts student results using machine learning and is configured for deployment on Vercel.

## 🚀 Quick Deploy to Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/Venvienne/Student_result_predictor)

## 📁 Project Structure for Vercel

```
student_result_predictor/
├── api/
│   └── index.py          # Main Flask application for Vercel
├── static/
│   └── style.css         # CSS styles
├── templates/
│   ├── index.html        # Main prediction form
│   └── result.html       # Results display page
├── model/
│   └── dt_model.joblib   # Trained ML model
├── vercel.json           # Vercel configuration
├── requirements.txt      # Python dependencies
├── package.json          # Node.js metadata
├── build.py              # Build script for model
└── .vercelignore         # Files to ignore during deployment
```

## 🛠️ Manual Deployment Steps

### 1. Prerequisites
- [Vercel CLI](https://vercel.com/docs/cli) installed
- Git repository with your code

### 2. Install Vercel CLI
```bash
npm i -g vercel
```

### 3. Login to Vercel
```bash
vercel login
```

### 4. Deploy
```bash
# From the project root directory
vercel

# For production deployment
vercel --prod
```

## ⚙️ Configuration Files

### vercel.json
- Configures Python runtime for Flask app
- Sets up routing for static files and API endpoints
- Defines build process

### requirements.txt
- Lists all Python dependencies
- Includes Flask, scikit-learn, pandas, joblib, numpy

### .vercelignore
- Excludes development files from deployment
- Reduces deployment size and build time

## 🔧 Environment Setup

The application automatically:
1. Loads the pre-trained ML model
2. Serves static CSS files
3. Handles Flask routing for prediction endpoints

## 📱 Features

- **Responsive Design**: Works on desktop and mobile
- **ML Prediction**: Uses Decision Tree algorithm
- **Beautiful UI**: Custom CSS with gradients and animations
- **Real-time Results**: Instant prediction with confidence scores
- **Study Recommendations**: Personalized tips based on results

## 🌐 Live Demo

After deployment, your app will be available at:
- Main form: `https://your-app.vercel.app/`
- Test result: `https://your-app.vercel.app/test-result`

## 🔍 Troubleshooting

### Common Issues:

1. **Model not loading**
   - Ensure `dt_model.joblib` exists in the `model/` directory
   - Run `python build.py` to create the model if missing

2. **Static files not loading**
   - Check that `vercel.json` routing is correct
   - Verify static files are in the `static/` directory

3. **Template not found**
   - Ensure templates are in the `templates/` directory
   - Check that `api/index.py` has correct template paths

## 📊 Model Information

The ML model predicts student pass/fail based on:
- Study hours per day (0-8)
- Sleep hours per day (4-9)
- Number of absences (0-20)
- Assignments completed (0-20)
- Exam score (40-100)

## 🎨 Customization

- Modify `static/style.css` for design changes
- Update `templates/` files for UI modifications
- Adjust model in `model/dt_model.joblib` for different predictions

## 📈 Performance

- ⚡ Serverless deployment with instant scaling
- 🌍 Global CDN for fast loading
- 💾 Minimal memory footprint
- 🔄 Automatic deployments from Git

---

Built with ❤️ using Flask, scikit-learn, and Vercel