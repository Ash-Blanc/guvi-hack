# Railway Deployment Guide (NO CREDIT CARD REQUIRED!)

Railway is the **best free alternative** to Render for your use case.

## Why Railway?

✅ **No credit card required** for free tier  
✅ **$5 free credit/month** (enough for hobby projects)  
✅ **Automatic HTTPS**  
✅ **Easy GitHub integration**  
✅ **Supports Python/FastAPI natively**  
✅ **Doesn't sleep** (unlike Render's free tier)

---

## Deployment Steps

### 1. Sign Up
1. Go to [railway.app](https://railway.app)
2. Click "Start a New Project"
3. Sign in with GitHub (no credit card needed!)

### 2. Deploy from GitHub
1. Click **"Deploy from GitHub repo"**
2. Select your repository: `Ash-Blanc/guvi-hack`
3. Railway will auto-detect it's a Python app

### 3. Configure Environment Variables
**CRITICAL:** Your app will crash without these!

1. Click on your service "honey-pot-api"
2. Click the **Variables** tab
3. Click "New Variable" and add:

| Variable Name | Value |
|---------------|-------|
| `MISTRAL_API_KEY` | `key1, key2, key3` (Comma separated) |
| `API_KEY` | `test-key` (or your chosen secure key) |
| `PORT` | `8000` |

*Note: You can use "RAW Editor" to paste `.env` content directly (excluding comments).*

### 4. Configure Start Command
Click **Settings** → **Deploy** → Set start command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### 5. Generate Public Domain
Click **Settings** → **Networking** → **Generate Domain**

Your API will be live at: `https://your-app.up.railway.app`

---

## Testing Your Deployment

```bash
# Update test script to use Railway URL
export API_URL="https://your-app.up.railway.app/analyze"
./test_api.sh vikram
```

---

## Other Alternatives (if Railway doesn't work)

### Option 2: Koyeb
- **Pros:** No credit card, free tier, doesn't sleep
- **Cons:** More complex setup
- **URL:** [koyeb.com](https://koyeb.com)

### Option 3: Fly.io
- **Pros:** Good free tier, excellent docs
- **Cons:** Requires credit card (but won't charge)
- **URL:** [fly.io](https://fly.io)

### Option 4: PythonAnywhere (Console-based)
- **Pros:** True free tier, no credit card
- **Cons:** Manual setup, less automated
- **URL:** [pythonanywhere.com](https://pythonanywhere.com)

---

## Railway vs Render Comparison

| Feature | Railway | Render |
|---------|---------|--------|
| Credit card required | ❌ No | ✅ Yes |
| Free credits | $5/month | 750 hours |
| Sleep behavior | Doesn't sleep | Sleeps after 15min |
| Setup difficulty | Easy | Easy |
| HTTPS | ✅ Auto | ✅ Auto |

**Recommendation: Use Railway** 🚂
