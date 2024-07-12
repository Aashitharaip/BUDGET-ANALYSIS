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
        income = float(request.form.get('income', 0))
        housing = float(request.form.get('housing', 0))
        utilities = float(request.form.get('utilities', 0))
        groceries = float(request.form.get('groceries', 0))
        transportation = float(request.form.get('transportation', 0))
        childcare = float(request.form.get('childcare', 0))
        healthcare = float(request.form.get('healthcare', 0))
        student = float(request.form.get('student', 0))
        debt = float(request.form.get('debt', 0))
        entertainment = float(request.form.get('entertainment', 0))
        dining = float(request.form.get('dining', 0))
        hobbies = float(request.form.get('hobbies', 0))
        splurges = float(request.form.get('splurges', 0))
        emergency_fund = float(request.form.get('Emergency_Fund', 0))
        retirement = float(request.form.get('retirement', 0))
        vacation = float(request.form.get('vacation', 0))

        total_needs = housing + utilities + groceries + transportation + childcare + healthcare + student + debt
        total_wants = entertainment + dining + hobbies + splurges
        total_savings = emergency_fund + retirement + vacation

        return redirect(url_for('piechart', needs=total_needs, wants=total_wants, savings=total_savings))
    return render_template('expenses.html')

@app.route('/piechart', methods=['GET'])
def piechart():
    needs = float(request.args.get('needs', 0))
    wants = float(request.args.get('wants', 0))
    savings = float(request.args.get('savings', 0))

    return render_template('piechart.html', needs=needs, wants=wants, savings=savings)

if __name__ == '__main__':
    app.run(debug=True)
