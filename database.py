import sqlite3
import firebase_admin
from firebase_admin import credentials, db

# Firebase initialization
cred = credentials.Certificate('C:/Users/Aashitha/BUDGET-ANALYSIS/serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://budget-analysis-1b3fa-default-rtdb.firebaseio.com/'
})

# Firebase authentication functions:
def get_users():
    try:
        ref = db.reference('users')
        users = ref.get()
        return users.values() if users else []
    except Exception as e:
        print(f"Error getting users: {str(e)}")
        return []

def add_user(name, email, contact, password):
    try:
        ref = db.reference('users')
        new_user_ref = ref.push()
        new_user_ref.set({
            'name': name,
            'email': email,
            'contact': contact,
            'password': password 
        })
        print("User added successfully")
    except Exception as e:
        print(f"Error adding user: {str(e)}")
        raise

def get_user_by_email(email):
    try:
        ref = db.reference('users')
        users = ref.order_by_child('email').equal_to(email).get()
        if users:
            return list(users.values())[0]  
        return None
    except Exception as e:
        print(f"Error getting user by email: {str(e)}")
        return None

# SQLite functions:
def init_db():
    conn = sqlite3.connect('survey.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS survey_responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            spend_on TEXT,
            home_status TEXT,
            sneaky_expenses TEXT,
            debt TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Function to insert a new survey response
def insert_response(name, spend_on, home_status, sneaky_expenses, debt):
    conn = sqlite3.connect('survey.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO survey_responses (name, spend_on, home_status, sneaky_expenses, debt)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, spend_on, home_status, sneaky_expenses, debt))
    conn.commit()
    conn.close()

# Initialize the database
init_db()
