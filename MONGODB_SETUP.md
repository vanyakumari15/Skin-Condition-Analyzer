# MongoDB Integration Setup Guide

## 📦 What Was Added

### New Files:
1. **database.py** - MongoDB database operations
2. **config.py** - Configuration management
3. **.env** - Environment variables (MongoDB URI, secrets)
4. **MONGODB_SETUP.md** - This file

### Updated Files:
1. **app.py** - Replaced SQLite with MongoDB
2. **requirements.txt** - Added pymongo and python-dotenv
3. **templates/profile.html** - Shows real statistics from MongoDB

## 🚀 Installation Steps

### Step 1: Install MongoDB

**Option A: MongoDB Community Server (Recommended)**
1. Download from: https://www.mongodb.com/try/download/community
2. Install MongoDB Community Server
3. MongoDB will run on `mongodb://localhost:27017/` by default

**Option B: MongoDB Atlas (Cloud)**
1. Create free account at: https://www.mongodb.com/cloud/atlas
2. Create a free cluster
3. Get connection string
4. Update `.env` file with your connection string

### Step 2: Install Python Dependencies

```bash
pip install pymongo python-dotenv
```

Or install all requirements:
```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables

Edit the `.env` file:

```env
# For Local MongoDB
MONGODB_URI=mongodb://localhost:27017/
DATABASE_NAME=skinanalyzer

# For MongoDB Atlas (Cloud)
# MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/
# DATABASE_NAME=skinanalyzer

SECRET_KEY=your-secret-key-change-this-in-production
FLASK_ENV=development
```

### Step 4: Start MongoDB Service

**Windows:**
```cmd
net start MongoDB
```

**Mac/Linux:**
```bash
sudo systemctl start mongod
```

**Or use MongoDB Compass** (GUI tool) to manage your database

### Step 5: Run the Application

```bash
python app.py
```

## 📊 Database Structure

### Collections:

#### 1. **users** Collection
```javascript
{
  _id: ObjectId,
  username: String (unique),
  email: String (unique),
  password: String (hashed),
  created_at: DateTime,
  updated_at: DateTime,
  is_active: Boolean,
  total_analyses: Number
}
```

#### 2. **analyses** Collection
```javascript
{
  _id: ObjectId,
  user_id: ObjectId (reference to users),
  predictions: Array,
  image_data: String (base64),
  created_at: DateTime,
  primary_diagnosis: String,
  confidence: Number
}
```

## 🔧 Database Operations

### Available Functions in `database.py`:

**User Operations:**
- `create_user(username, email, password)` - Create new user
- `get_user_by_username(username)` - Find user by username
- `get_user_by_email(email)` - Find user by email
- `get_user_by_id(user_id)` - Find user by ID
- `verify_password(user, password)` - Verify password
- `update_user(user_id, update_data)` - Update user info
- `delete_user(user_id)` - Delete user and their data

**Analysis Operations:**
- `save_analysis(user_id, predictions, image_data)` - Save analysis
- `get_user_analyses(user_id, limit)` - Get user's history
- `get_analysis_by_id(analysis_id)` - Get specific analysis
- `get_user_stats(user_id)` - Get user statistics

## 📈 New Features with MongoDB

### 1. **Analysis History**
- All analyses are now saved to database
- Users can view their past analyses
- Track analysis trends over time

### 2. **User Statistics**
- Total analyses count
- Most common diagnosis
- Days active
- Member since date

### 3. **Better Performance**
- Indexed queries for fast lookups
- Scalable for millions of users
- No file locking issues

### 4. **Data Relationships**
- User → Analyses (one-to-many)
- Easy to query related data
- Efficient aggregations

## 🔍 Verify MongoDB Connection

### Using Python:
```python
from database import db

# Test connection
user = db.create_user("testuser", "test@example.com", "password123")
print(f"User created with ID: {user}")

# Get user
user = db.get_user_by_username("testuser")
print(f"User found: {user['username']}")
```

### Using MongoDB Compass:
1. Open MongoDB Compass
2. Connect to `mongodb://localhost:27017/`
3. You should see `skinanalyzer` database
4. Collections: `users` and `analyses`

## 🔄 Migration from SQLite

If you have existing SQLite data, you can migrate it:

```python
import sqlite3
from database import db

# Connect to old SQLite database
conn = sqlite3.connect('users.db')
c = conn.cursor()
c.execute('SELECT username, email, password, created_at FROM users')
users = c.fetchall()

# Migrate to MongoDB
for user in users:
    db.users.insert_one({
        'username': user[0],
        'email': user[1],
        'password': user[2],  # Already hashed
        'created_at': user[3],
        'is_active': True,
        'total_analyses': 0
    })

conn.close()
print(f"Migrated {len(users)} users to MongoDB")
```

## 🛠️ Troubleshooting

### MongoDB Not Starting?
```bash
# Check if MongoDB is running
mongosh

# If not, start the service
# Windows:
net start MongoDB

# Mac/Linux:
sudo systemctl start mongod
```

### Connection Error?
- Check if MongoDB is running
- Verify MONGODB_URI in `.env`
- Check firewall settings
- For Atlas: Check IP whitelist

### Import Error?
```bash
pip install pymongo python-dotenv
```

## 📝 Environment Variables

Create `.env` file in project root:

```env
# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017/
DATABASE_NAME=skinanalyzer

# Flask Configuration
SECRET_KEY=your-secret-key-change-this-in-production
FLASK_ENV=development
```

## 🎯 Benefits of MongoDB

✅ **Scalability** - Handle millions of users
✅ **Flexibility** - Easy to add new fields
✅ **Performance** - Fast queries with indexes
✅ **Relationships** - Link users to analyses
✅ **Analytics** - Powerful aggregation pipeline
✅ **Cloud Ready** - Easy to deploy to MongoDB Atlas
✅ **No Migrations** - Schema-less design

## 🔐 Security Best Practices

1. **Change SECRET_KEY** in `.env`
2. **Use strong passwords** for MongoDB
3. **Enable authentication** in production
4. **Use MongoDB Atlas** for cloud deployment
5. **Backup regularly** using mongodump
6. **Use environment variables** for sensitive data

## 📚 Additional Resources

- MongoDB Documentation: https://docs.mongodb.com/
- PyMongo Documentation: https://pymongo.readthedocs.io/
- MongoDB Atlas: https://www.mongodb.com/cloud/atlas
- MongoDB Compass: https://www.mongodb.com/products/compass

---

**Your application now uses MongoDB for better scalability and features!** 🎉
