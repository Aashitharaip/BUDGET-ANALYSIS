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
        
        if not email or not password:
            flash('Please enter both email and password.', 'danger')
            return redirect(url_for('signin'))
        
        user = database.get_user_by_email(email)
        
        if user:
            if user['password'] == password:
                session['user'] = {'email': user['email']}
                flash('Logged in successfully!', 'success')
                return redirect(url_for('info'))
            else:
                flash('Invalid email or password', 'danger')
                return redirect(url_for('signin'))
        else:
            flash('User does not exist.', 'danger')
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
    
@app.route('/expenses', methods=['GET', 'POST'])
def expenses():
    if request.method == 'POST':
        # Retrieve income and expense data from the form, default to 0 if empty
        income = float(request.form['income'])
        needs = sum(float(request.form.get(key, 0) or 0) for key in [
            'housing', 'utilities', 'groceries', 'transportation', 'childcare', 'healthcare', 'student', 'debt'
        ])
        wants = sum(float(request.form.get(key, 0) or 0) for key in [
            'entertainment', 'dining', 'hobbies', 'splurges'
        ])
        savings = sum(float(request.form.get(key, 0) or 0) for key in [
            'emergency_fund', 'retirement', 'vacation'
        ])
        
        total_expenses = needs + wants + savings

        # Debugging: Print out the calculated values
        print(f"Income: {income}, Needs: {needs}, Wants: {wants}, Savings: {savings}, Total: {total_expenses}")
        
        if total_expenses > income:
            flash('Your total expenses exceed your income!', 'error')
            return redirect(url_for('expenses'))  # Redirect back to expenses page

        # Redirect to piechart with URL parameters
        return redirect(url_for('piechart', needs=needs, wants=wants, savings=savings))
        
    else:
        # Handle the initial GET request
        return render_template('expenses.html')


@app.route('/piechart', methods=['GET'])
def piechart():
    needs = float(request.args.get('needs', 0))
    wants = float(request.args.get('wants', 0))
    savings = float(request.args.get('savings', 0))

    return render_template('piechart.html', needs=needs, wants=wants, savings=savings)

@app.route('/report', methods=['GET'])
def report():
    # Retrieve budget details from session or database
    budget = session.get('budget', None)
    if budget:
        needs = budget['needs']
        wants = budget['wants']
        savings = budget['savings']
        # Render the report template with budget details
        return render_template('report.html', needs=needs, wants=wants, savings=savings)
    else:
        flash('Budget details not found.', 'danger')
        return redirect(url_for('expenses'))

    
if __name__ == '__main__':
    app.run(debug=True)
