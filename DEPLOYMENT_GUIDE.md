# 🚀 IntelliVest AI - Render Deployment Guide

This guide will walk you through deploying your IntelliVest AI Streamlit application to Render for free hosting.

## 📋 Prerequisites

1. **GitHub Account**: Your code must be on GitHub
2. **Render Account**: Sign up at [render.com](https://render.com)
3. **API Keys**: You'll need the following API keys:
   - Google API Key (for Gemini)
   - Groq API Key
   - OpenAI API Key (optional)
   - Tavily API Key (for web search)

## 🔧 Step 1: Prepare Your Repository

Your repository should now contain these deployment files:
- ✅ `render.yaml` - Render configuration
- ✅ `.streamlit/config.toml` - Streamlit configuration
- ✅ `runtime.txt` - Python version specification
- ✅ `Procfile` - Alternative deployment config
- ✅ `requirements.txt` - Dependencies

## 🚀 Step 2: Deploy to Render

### 2.1 Connect to Render
1. Go to [render.com](https://render.com) and sign in
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account if not already connected

### 2.2 Configure Your Service
1. **Repository**: Select your IntelliVest AI repository
2. **Name**: `intellivest-ai` (or your preferred name)
3. **Environment**: `Python 3`
4. **Build Command**: `pip install -r requirements.txt`
5. **Start Command**: `streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true`

### 2.3 Set Environment Variables
In the Render dashboard, add these environment variables:

#### Required API Keys:
```
GOOGLE_API_KEY=your_google_api_key_here
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

#### Optional API Keys:
```
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_API_BASE=https://api.openai.com/v1
```

#### System Variables:
```
PYTHONPATH=.
PLAYWRIGHT_BROWSERS_PATH=0
```

### 2.4 Deploy
1. Click **"Create Web Service"**
2. Render will automatically build and deploy your app
3. Wait for the build to complete (usually 5-10 minutes)

## 🔍 Step 3: Verify Deployment

1. **Check Build Logs**: Ensure all dependencies installed correctly
2. **Health Check**: Your app should respond at the provided URL
3. **Test Functionality**: Try the basic features of your app

## 📱 Step 4: Access Your App

- **URL**: `https://your-app-name.onrender.com`
- **Custom Domain**: You can add your own domain in Render settings
- **SSL**: Automatically provided by Render

## ⚠️ Important Notes

### Free Tier Limitations:
- **Sleep after 15 minutes** of inactivity
- **512 MB RAM** available
- **Shared CPU** resources
- **Build time**: 5-10 minutes for first deployment

### Performance Tips:
1. **Optimize Dependencies**: Remove unused packages from requirements.txt
2. **Memory Management**: Monitor memory usage in your app
3. **Caching**: Use Streamlit's caching for expensive operations

## 🛠️ Troubleshooting

### Common Issues:

#### 1. Build Failures
- Check `requirements.txt` for compatibility
- Ensure Python 3.11 compatibility
- Verify all dependencies are available

#### 2. Runtime Errors
- Check environment variables are set correctly
- Review Render logs for error details
- Ensure API keys are valid

#### 3. Memory Issues
- Monitor memory usage in Render dashboard
- Consider upgrading to paid plan if needed
- Optimize your app's memory usage

### Debug Commands:
```bash
# Check app locally first
streamlit run streamlit_app.py --server.port 8501

# Test with production settings
STREAMLIT_SERVER_HEADLESS=true streamlit run streamlit_app.py
```

## 🔄 Updating Your App

1. **Push Changes**: Commit and push to GitHub
2. **Auto-Deploy**: Render automatically redeploys on push
3. **Manual Deploy**: Use "Manual Deploy" in Render dashboard if needed

## 📊 Monitoring

- **Logs**: Available in Render dashboard
- **Metrics**: CPU, memory, and response time
- **Health Checks**: Automatic monitoring of your app

## 🎉 Success!

Once deployed, your IntelliVest AI app will be accessible to anyone with an internet connection!

**Your app URL**: `https://your-app-name.onrender.com`

---

## 🆘 Need Help?

- **Render Documentation**: [docs.render.com](https://docs.render.com)
- **Streamlit Deployment**: [docs.streamlit.io](https://docs.streamlit.io)
- **GitHub Issues**: Check your repository for known issues

---

*Happy Investing with IntelliVest AI! 🚀📈* 