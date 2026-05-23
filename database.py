from pymongo import MongoClient
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
import config

class Database:
    def __init__(self):
        try:
            self.client = MongoClient(config.Config.MONGODB_URI, serverSelectionTimeoutMS=5000)
            # Test connection
            self.client.server_info()
            self.db = self.client[config.Config.DATABASE_NAME]
            self.users = self.db.users
            self.analyses = self.db.analyses
            
            # Create indexes
            self.users.create_index('username', unique=True)
            self.users.create_index('email', unique=True)
            self.analyses.create_index('user_id')
            self.analyses.create_index('created_at')
            
            print("✅ MongoDB connected successfully!")
        except Exception as e:
            print(f"⚠️  MongoDB not available: {e}")
            print("📝 Using SQLite fallback mode")
            self.client = None
            self._init_sqlite()
    
    # User Operations
    def create_user(self, username, email, password):
        """Create a new user"""
        try:
            user = {
                'username': username,
                'email': email,
                'password': generate_password_hash(password),
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow(),
                'is_active': True,
                'total_analyses': 0
            }
            result = self.users.insert_one(user)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error creating user: {e}")
            return None
    
    def get_user_by_username(self, username):
        """Get user by username"""
        return self.users.find_one({'username': username})
    
    def get_user_by_email(self, email):
        """Get user by email"""
        return self.users.find_one({'email': email})
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        try:
            return self.users.find_one({'_id': ObjectId(user_id)})
        except:
            return None
    
    def verify_password(self, user, password):
        """Verify user password"""
        if user:
            return check_password_hash(user['password'], password)
        return False
    
    def update_user(self, user_id, update_data):
        """Update user information"""
        try:
            update_data['updated_at'] = datetime.utcnow()
            result = self.users.update_one(
                {'_id': ObjectId(user_id)},
                {'$set': update_data}
            )
            return result.modified_count > 0
        except:
            return False
    
    # Analysis Operations
    def save_analysis(self, user_id, predictions, image_data=None):
        """Save analysis results"""
        try:
            analysis = {
                'user_id': ObjectId(user_id),
                'predictions': predictions,
                'image_data': image_data,
                'created_at': datetime.utcnow(),
                'primary_diagnosis': predictions[0]['class'] if predictions else None,
                'confidence': predictions[0]['confidence'] if predictions else None
            }
            result = self.analyses.insert_one(analysis)
            
            # Update user's total analyses count
            self.users.update_one(
                {'_id': ObjectId(user_id)},
                {'$inc': {'total_analyses': 1}}
            )
            
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error saving analysis: {e}")
            return None
    
    def get_user_analyses(self, user_id, limit=10):
        """Get user's analysis history"""
        try:
            analyses = self.analyses.find(
                {'user_id': ObjectId(user_id)}
            ).sort('created_at', -1).limit(limit)
            return list(analyses)
        except:
            return []
    
    def get_analysis_by_id(self, analysis_id):
        """Get specific analysis"""
        try:
            return self.analyses.find_one({'_id': ObjectId(analysis_id)})
        except:
            return None
    
    def get_user_stats(self, user_id):
        """Get user statistics"""
        try:
            user = self.get_user_by_id(user_id)
            if not user:
                return None
            
            total_analyses = user.get('total_analyses', 0)
            
            # Get most common diagnosis
            pipeline = [
                {'$match': {'user_id': ObjectId(user_id)}},
                {'$group': {
                    '_id': '$primary_diagnosis',
                    'count': {'$sum': 1}
                }},
                {'$sort': {'count': -1}},
                {'$limit': 1}
            ]
            
            most_common = list(self.analyses.aggregate(pipeline))
            most_common_diagnosis = most_common[0]['_id'] if most_common else None
            
            # Calculate days active
            if user.get('created_at'):
                days_active = (datetime.utcnow() - user['created_at']).days
            else:
                days_active = 0
            
            return {
                'total_analyses': total_analyses,
                'most_common_diagnosis': most_common_diagnosis,
                'days_active': days_active,
                'member_since': user.get('created_at')
            }
        except Exception as e:
            print(f"Error getting user stats: {e}")
            return None
    
    def delete_user(self, user_id):
        """Delete user and all their analyses"""
        try:
            # Delete user's analyses
            self.analyses.delete_many({'user_id': ObjectId(user_id)})
            # Delete user
            result = self.users.delete_one({'_id': ObjectId(user_id)})
            return result.deleted_count > 0
        except:
            return False
    
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
                      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        conn.commit()
        conn.close()
        self.use_sqlite = True
    
    def close(self):
        """Close database connection"""
        if self.client:
            self.client.close()

# Global database instance
db = Database()
