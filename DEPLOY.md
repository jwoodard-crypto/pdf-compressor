# 🚀 Quick Deploy Guide

## Option 1: Render (Recommended - Easiest)

### 1. Create GitHub Account (if you don't have one)
- Go to [github.com/signup](https://github.com/signup)

### 2. Upload Code to GitHub

```bash
cd ~/pdf-compressor-cloud
git init
git add .
git commit -m "PDF Compressor"

# Replace YOUR_USERNAME with your GitHub username
git remote add origin https://github.com/YOUR_USERNAME/pdf-compressor.git
git branch -M main
git push -u origin main
```

### 3. Deploy on Render
1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Click **New +** → **Web Service**
4. Select your `pdf-compressor` repo
5. Click **Create Web Service**
6. Done! 🎉

**Your URL:** `https://pdf-compressor-xxxx.onrender.com`

---

## Option 2: Railway (Alternative)

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click **New Project** → **Deploy from GitHub repo**
4. Select `pdf-compressor`
5. Done!

---

## Option 3: Fly.io (Alternative)

```bash
cd ~/pdf-compressor-cloud

# Install flyctl
brew install flyctl

# Login
fly auth login

# Deploy
fly launch
```

---

## ✅ After Deployment

Share the URL with your team:
- **Render:** `https://your-app.onrender.com`
- **Railway:** `https://your-app.up.railway.app`
- **Fly.io:** `https://your-app.fly.dev`

They can use it from anywhere! 🌍

---

## 💰 Cost

All three options have **FREE tiers**:
- **Render:** 750 hours/month free
- **Railway:** $5 free credit/month
- **Fly.io:** Free for small apps

Perfect for team tools! 🎯
