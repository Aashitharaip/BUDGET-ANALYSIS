from flask import Flask, session, redirect, url_for, flash, render_template, request, jsonify
import database  

app = Flask(__name__)
app.secret_key = 'ltkrj6iekrlkwhjrnfjsbdhnknfksmtij'  

@app.route('/')
def index():
    users = database.get_users()
    return render_template('index.html', users=users)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = database.get_user_by_email(email)
        if user and user['password'] == password:
            session['user'] = {'email': user['email']}  
            flash('Logged in successfully!', 'success')
            return redirect(url_for('info'))
        else:
            flash('Invalid email or password', 'danger')
            return redirect(url_for('signin'))
    return render_template('signin.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == ('POST'):
        name = request.form['name']
        email = request.form['email']
        contact = request.form['contact']
        password = request.form['password']
        if not name or not email or not contact or not password:
            flash('All fields are required!', 'danger')
            return redirect(url_for('signup'))
        try:
            user = database.get_user_by_email(email)
            if user:
                flash("User already exists", 'danger')
            else:
                database.add_user(name, email, contact, password)
                flash('User registered successfully!', 'success')
            return redirect(url_for('signin'))
        except Exception as e:
            flash(f'Error adding user: {str(e)}', 'danger')
            return redirect(url_for('signup'))
    return render_template('signup.html')

@app.route('/info')
def info():
    if 'user' in session:
        users = database.get_users()
        return render_template('info.html', users=users)
    else:
        flash('Please sign in to view this page.', 'danger')
        return redirect(url_for('signin'))
    
@app.route('/expenses')
def expenses():
    users = database.get_users()
    return render_template('expenses.html', users=users)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    name = data.get('name')
    spend_on = data.get('spendOn')
    home_status = data.get('homeStatus')
    sneaky_expenses = data.get('sneakyExpenses')
    debt = data.get('debt')

    try:
        database.insert_response(name, spend_on, home_status, sneaky_expenses, debt)
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
