# 📄 PDF Compressor - Cloud Hosted

Deploy this PDF compressor to the cloud so your team can access it from anywhere!

## 🚀 Deploy to Render (Free)

### Step 1: Create a GitHub Repository

1. Go to [github.com](https://github.com) and sign in
2. Click the **+** button (top right) → **New repository**
3. Name it: `pdf-compressor`
4. Make it **Public** or **Private** (your choice)
5. Click **Create repository**

### Step 2: Upload Your Code to GitHub

Open Terminal and run these commands:

```bash
cd ~/pdf-compressor-cloud

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - PDF Compressor"

# Connect to your GitHub repo (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/pdf-compressor.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 3: Deploy to Render

1. Go to [render.com](https://render.com)
2. Click **Sign Up** (or Sign In if you have an account)
3. Sign up with your **GitHub account**
4. Click **New +** → **Web Service**
5. Click **Connect** next to your `pdf-compressor` repository
6. Fill in:
   - **Name:** `pdf-compressor` (or any name you want)
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Instance Type:** Free
7. Click **Create Web Service**

### Step 4: Wait for Deployment (2-3 minutes)

Render will:
- Install Python
- Install dependencies
- Start your app
- Give you a URL like: `https://pdf-compressor-xxxx.onrender.com`

### Step 5: Share with Your Team! 🎉

Once deployed, share the URL with your team:
- `https://your-app-name.onrender.com`

They can access it from anywhere - no installation needed!

## ⚠️ Important Notes

### Free Tier Limitations:
- **Sleeps after 15 minutes** of inactivity
- First request after sleep takes ~30 seconds to wake up
- **750 hours/month** free (enough for most teams)

### To Keep It Always On:
- Upgrade to paid tier ($7/month) for 24/7 uptime
- Or use a free "ping" service to keep it awake

## 🔧 Troubleshooting

**"Build failed"**
- Check that all files are in the repository
- Verify `requirements.txt` is present

**"Application failed to start"**
- Check Render logs for errors
- Verify `gunicorn` is in requirements.txt

**"502 Bad Gateway"**
- App is still starting (wait 30 seconds)
- Or app crashed (check logs)

## 📝 Files Included

- `app.py` - Flask server with PDF compression
- `index.html` - Web interface
- `requirements.txt` - Python dependencies
- `render.yaml` - Render deployment config
- `README.md` - This file

## 🆘 Need Help?

If you get stuck:
1. Check Render's deployment logs
2. Verify your GitHub repository has all files
3. Make sure you're using the correct build/start commands

---

Made with ❤️ for easy PDF compression
