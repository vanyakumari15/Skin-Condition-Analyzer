# Quick MongoDB Installation Guide

## 🚀 Quick Start (3 Steps)

### Step 1: Install MongoDB

**Download MongoDB Community Server:**
https://www.mongodb.com/try/download/community

**Or use MongoDB Atlas (Cloud - No installation needed):**
https://www.mongodb.com/cloud/atlas/register

### Step 2: Install Python Dependencies

```bash
pip install pymongo python-dotenv
```

### Step 3: Start MongoDB

**Windows:**
```cmd
net start MongoDB
```

**Mac:**
```bash
brew services start mongodb-community
```

**Linux:**
```bash
sudo systemctl start mongod
```

## ✅ Verify Installation

```bash
mongosh
```

If you see MongoDB shell, you're good to go!

## 🎯 Run Your Application

```bash
python app.py
```

Your app will automatically:
- Connect to MongoDB
- Create `skinanalyzer` database
- Create `users` and `analyses` collections
- Set up indexes

## 🌐 MongoDB Atlas (Cloud Option)

If you don't want to install MongoDB locally:

1. Go to https://www.mongodb.com/cloud/atlas
2. Create free account
3. Create free cluster (M0)
4. Get connection string
5. Update `.env`:
```env
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/
```

## 📊 View Your Data

**Option 1: MongoDB Compass (GUI)**
- Download: https://www.mongodb.com/products/compass
- Connect to: `mongodb://localhost:27017/`

**Option 2: Command Line**
```bash
mongosh
use skinanalyzer
db.users.find()
db.analyses.find()
```

---

**That's it! Your app now uses MongoDB!** 🎉
