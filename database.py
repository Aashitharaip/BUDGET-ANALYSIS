import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate('C:/Users/Aashitha/BUDGET-ANALYSIS/serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://budget-analysis-1b3fa-default-rtdb.firebaseio.com/'
})

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
