"""
Hybrid Database - Works with MongoDB or SQLite fallback
"""
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import config

class Database:
    def __init__(self):
        self.use_mongodb = False
        self.client = None
        
        # Try MongoDB first
        try:
            from pymongo import MongoClient
            from bson.objectid import ObjectId
            
            self.client = MongoClient(config.Config.MONGODB_URI, serverSelectionTimeoutMS=10000)
            self.client.server_info()  # Test connection
            
            self.db = self.client[config.Config.DATABASE_NAME]
            self.users = self.db.users
            self.analyses = self.db.analyses
            
            # Create indexes
            self.users.create_index('username', unique=True)
            self.users.create_index('email', unique=True)
            self.analyses.create_index('user_id')
            
            self.use_mongodb = True
            self.ObjectId = ObjectId
            print("✅ MongoDB connected successfully!")
            
        except Exception as e:
            print(f"⚠️  MongoDB not available: {str(e)[:100]}")
            print("📝 Using SQLite fallback mode")
            self._init_sqlite()
    
    def _init_sqlite(self):
        """Initialize SQLite as fallback"""
        import sqlite3
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      username TEXT UNIQUE NOT NULL,
                      email TEXT UNIQUE NOT NULL,
                      password TEXT NOT NULL,
                      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                      total_analyses INTEGER DEFAULT 0)''')
        conn.commit()
        conn.close()
    
    # User Operations
    def create_user(self, username, email, password):
        """Create a new user"""
        if self.use_mongodb:
            try:
                user = {
                    'username': username,
                    'email': email,
                    'password': generate_password_hash(password),
                    'created_at': datetime.utcnow(),
                    'is_active': True,
                    'total_analyses': 0
                }
                result = self.users.insert_one(user)
                return str(result.inserted_id)
            except Exception as e:
                print(f"Error creating user: {e}")
                return None
        else:
            # SQLite fallback
            import sqlite3
            try:
                conn = sqlite3.connect('users.db')
                c = conn.cursor()
                c.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                         (username, email, generate_password_hash(password)))
                conn.commit()
                user_id = c.lastrowid
                conn.close()
                return str(user_id)
            except sqlite3.IntegrityError:
                return None
    
    def get_user_by_username(self, username):
        """Get user by username"""
        if self.use_mongodb:
            return self.users.find_one({'username': username})
        else:
            import sqlite3
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            c.execute('SELECT * FROM users WHERE username = ?', (username,))
            user = c.fetchone()
            conn.close()
            if user:
                return {
                    '_id': user[0],
                    'username': user[1],
                    'email': user[2],
                    'password': user[3],
                    'created_at': user[4],
                    'total_analyses': user[5] if len(user) > 5 else 0
                }
            return None
    
    def get_user_by_email(self, email):
        """Get user by email"""
        if self.use_mongodb:
            return self.users.find_one({'email': email})
        else:
            import sqlite3
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            c.execute('SELECT * FROM users WHERE email = ?', (email,))
            user = c.fetchone()
            conn.close()
            if user:
                return {
                    '_id': user[0],
                    'username': user[1],
                    'email': user[2],
                    'password': user[3],
                    'created_at': user[4]
                }
            return None
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        if self.use_mongodb:
            try:
                return self.users.find_one({'_id': self.ObjectId(user_id)})
            except:
                return None
        else:
            import sqlite3
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            c.execute('SELECT * FROM users WHERE id = ?', (user_id,))
            user = c.fetchone()
            conn.close()
            if user:
                return {
                    '_id': user[0],
                    'username': user[1],
                    'email': user[2],
                    'password': user[3],
                    'created_at': user[4],
                    'total_analyses': user[5] if len(user) > 5 else 0
                }
            return None
    
    def verify_password(self, user, password):
        """Verify user password"""
        if user:
            return check_password_hash(user['password'], password)
        return False
    
    def get_user_stats(self, user_id):
        """Get user statistics"""
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        
        if self.use_mongodb:
            total_analyses = user.get('total_analyses', 0)
            if user.get('created_at'):
                days_active = (datetime.utcnow() - user['created_at']).days
            else:
                days_active = 0
        else:
            total_analyses = user.get('total_analyses', 0)
            days_active = 0
        
        return {
            'total_analyses': total_analyses,
            'most_common_diagnosis': 'N/A',
            'days_active': days_active,
            'member_since': user.get('created_at')
        }
    
    def save_analysis(self, user_id, predictions, image_data=None):
        """Save analysis results"""
        if self.use_mongodb:
            try:
                analysis = {
                    'user_id': self.ObjectId(user_id),
                    'predictions': predictions,
                    'image_data': image_data,
                    'created_at': datetime.utcnow(),
                    'primary_diagnosis': predictions[0]['class'] if predictions else None,
                    'confidence': predictions[0]['confidence'] if predictions else None
                }
                result = self.analyses.insert_one(analysis)
                
                # Update user's total analyses count
                self.users.update_one(
                    {'_id': self.ObjectId(user_id)},
                    {'$inc': {'total_analyses': 1}}
                )
                
                return str(result.inserted_id)
            except Exception as e:
                print(f"Error saving analysis: {e}")
                return None
        else:
            # SQLite - just update count
            import sqlite3
            try:
                conn = sqlite3.connect('users.db')
                c = conn.cursor()
                c.execute('UPDATE users SET total_analyses = total_analyses + 1 WHERE id = ?', (user_id,))
                conn.commit()
                conn.close()
                return "saved"
            except:
                return None
    
    def get_user_analyses(self, user_id, limit=10):
        """Get user's analysis history"""
        if self.use_mongodb:
            try:
                analyses = list(self.analyses.find(
                    {'user_id': self.ObjectId(user_id)}
                ).sort('created_at', -1).limit(limit))
                return analyses
            except Exception as e:
                print(f"Error getting analyses: {e}")
                return []
        else:
            # SQLite doesn't store analyses, return empty
            return []
    
    def close(self):
        """Close database connection"""
        if self.client:
            self.client.close()

# Global database instance
db = Database()
