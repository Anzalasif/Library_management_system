from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Hardcoded credentials for demo purposes
users = {
    'admin': {'password': 'admin123', 'role': 'admin'},
    'user': {'password': 'user123', 'role': 'user'}
}

@app.route('/')
def home():
    # Render index.html for the main login page
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username]['password'] == password:
            session['username'] = username
            session['role'] = users[username]['role']
            
            # Redirect based on role
            if users[username]['role'] == 'admin':
                return redirect(url_for('admin_page'))
            else:
                return redirect(url_for('user_page'))
        else:
            flash('Invalid Credentials. Please try again.')
            return redirect(url_for('home'))

    return render_template('index.html')

@app.route('/admin')
def admin_page():
    if session.get('role') == 'admin':
        return render_template('admin.html', username=session['username'])
    else:
        flash('Unauthorized access!')
        return redirect(url_for('home'))

@app.route('/user')
def user_page():
    if session.get('role') == 'user':
        return render_template('user.html', username=session['username'])
    else:
        flash('Unauthorized access!')
        return redirect(url_for('home'))

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/home')
def home_redirect():
    if 'username' in session:
        role = session.get('role')
        if role == 'admin':
            return redirect(url_for('admin_page'))
        elif role == 'user':
            return redirect(url_for('user_page'))
    return redirect(url_for('home'))

@app.route('/admin_book_issue')
def admin_book_issue():
    if session.get('role') == 'admin':
        return render_template('admin_bookIssue.html')
    else:
        flash('Unauthorized access!')
        return redirect(url_for('home'))
#user issue book
@app.route('/user_book_issue')
def user_book_issue():
    if session.get('role') == 'user':
        return render_template('user_bookIssue.html')
    else:
        flash('Unauthorized access!')
        return redirect(url_for('home'))
    
@app.route('/transactions')
def transactions_page():
    if 'role' in session:
        role = session['role']
        print(f"User role: {role}")  # Debugging line to ensure role is set
        if role == 'admin':
            return render_template('admin_transactions.html')
        elif role == 'user':
            return render_template('user_transactions.html')
    flash('Please log in to access transactions.')
    return redirect(url_for('home'))


@app.route('/search_results', methods=['POST', 'GET'])
def search_results():
    return render_template('search_results.html')

#return Book
@app.route('/admin/returnbook', methods=['GET', 'POST'])
def admin_returnbook():
    if request.method == 'POST':
        book_name = request.form.get('bookName')
        return_date = request.form.get('returnDate')
        remarks = request.form.get('remarks')

        # Process the form data as needed

        # Redirect to the admin transactions page or another page
        return redirect(url_for('admin_transactions'))

    return render_template('admin_returnbook.html')

@app.route('/user_return_book', methods=['GET', 'POST'])
def user_return_book():
    if request.method == 'POST':
        # Fetch form data for returning the book
        book_name = request.form.get('returnBookDropdown')
        return_date = request.form.get('returnDate')
        remarks = request.form.get('remarks')

        # Perform return book logic (e.g., check if the book is eligible for return, process return, etc.)

        if not book_name or not return_date:
            flash('Please provide all mandatory fields!', 'error')
            return redirect(url_for('user_return_book'))

        # If successful:
        flash(f'Book "{book_name}" returned successfully!', 'success')
        return redirect(url_for('user_transactions'))
    
    # Render the return book page
    return render_template('user_returnbook.html')
#payfine

@app.route('/admin/payfine', methods=['GET', 'POST'])
def admin_payfine():
    if request.method == 'POST':
        user_id = request.form.get('userId')
        fine_amount = request.form.get('fineAmount')
        remarks = request.form.get('remarks')

        # Process the fine payment as needed

        return redirect(url_for('admin_page'))  # Or another endpoint
    return render_template('admin_payfine.html')

@app.route('/user_payfine', methods=['GET', 'POST'])
def user_payfine():
    if session.get('role') == 'user':
        if request.method == 'POST':
            book_name = request.form.get('bookName')
            author = request.form.get('author')
            serial_no = request.form.get('serialNo')
            issue_date = request.form.get('issueDate')
            return_date = request.form.get('returnDate')
            actual_return_date = request.form.get('actualReturnDate')
            fine_calculated = request.form.get('fineCalculated')
            fine_paid = 'finePaid' in request.form  # Checkbox

            # Add logic to handle fine payment submission
            if not book_name or not serial_no or not fine_calculated:
                flash('Please fill all mandatory fields!', 'error')
                return render_template('user_payfine.html')

            # Process the fine payment
            flash('Fine payment recorded successfully!', 'success')
            return redirect(url_for('user_page'))

        return render_template('user_payfine.html')
    else:
        flash('Unauthorized access!', 'error')
        return redirect(url_for('home'))

@app.route('/maintenance', methods=['GET'])
def maintenance_home():
    return render_template('maintenance_home.html')
@app.route('/add_membership', methods=['GET', 'POST'])
def add_membership():
    if request.method == 'POST':
        membership_type = request.form.get('membershipType')
        if not membership_type:
            error_message = "Please select a membership type."
            return render_template('add_membership.html', error_message=error_message)
        
        # Process the membership addition (e.g., save to database)
        return redirect(url_for('maintenance_home'))  # Redirect to the maintenance home or another relevant page
        
    return render_template('add_membership.html')
@app.route('/update_membership', methods=['GET', 'POST'])
def update_membership():
    if request.method == 'POST':
        # Retrieve form data
        membership_number = request.form.get('membershipNumber')
        start_date = request.form.get('startDate')
        end_date = request.form.get('endDate')
        membership_extension = request.form.get('membershipExtension')

        # Basic validation
        if not membership_number or not start_date or not end_date or not membership_extension:
            flash('Please fill all the fields.', 'error')
            return redirect(url_for('update_membership'))

        # Process the form data (e.g., update the database)
        # Example:
        # update_membership_in_db(membership_number, start_date, end_date, membership_extension)

        flash('Membership updated successfully!', 'success')
        return redirect(url_for('admin_home_page'))

    return render_template('update_membership.html')
@app.route('/add_update_media', methods=['GET', 'POST'])

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        # Retrieve form data
        media_type = request.form.get('mediaType')
        book_movie_name = request.form.get('bookMovieName')
        procurement_date = request.form.get('procurementDate')
        quantity = request.form.get('quantity')

        # Check if all fields are filled and quantity is valid
        if media_type and book_movie_name and procurement_date and int(quantity) > 0:
            # Process the form data (e.g., save to database)
            # For now, let's print it to the console
            print(f"Type: {media_type}, Name: {book_movie_name}, Date: {procurement_date}, Quantity: {quantity}")

            # Redirect to a success page or another route after processing
            return redirect(url_for('User_success_page'))  # Change 'success_page' to your actual success route

        else:
            # If validation fails, reload the form with an error message
            error_message = "Please fill all the fields correctly."
            return render_template('add_book.html', error_message=error_message)
    
    # Render the form for GET requests
    return render_template('add_book.html')

# Route to display success message or handle success logic
@app.route('/success')
def success_page():
    return "Successfull!"
@app.route('/update')
def update_page():
    return "Successfull!"

@app.route('/update_book', methods=['GET', 'POST'])
def update_book():
    if request.method == 'POST':
        # Retrieve form data
        media_type = request.form.get('mediaType')
        book_movie_name = request.form.get('bookMovieName')
        serial_no = request.form.get('serialNo')
        status = request.form.get('status')
        date = request.form.get('date')

        # Check if all fields are filled
        if media_type and book_movie_name and serial_no and status and date:
            # Process the form data (e.g., update in database)
            # For now, let's print it to the console
            print(f"Type: {media_type}, Name: {book_movie_name}, Serial No: {serial_no}, Status: {status}, Date: {date}")

            # Redirect to a success page or another route after processing
            return redirect(url_for('update_page'))  # Change 'success_page' to your actual success route

        else:
            # If validation fails, reload the form with an error message
            error_message = "Please fill all the required fields."
            return render_template('update_book.html', error_message=error_message)
    
    # Render the form for GET requests
    return render_template('update_book.html')
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        # Retrieve form data
        user_type = request.form.get('userType')
        name = request.form.get('name').strip()
        status = 'status' in request.form  # Checkbox status
        is_admin = 'admin' in request.form  # Checkbox status

        # Check if all required fields are filled
        if user_type and name:
            # Process the form data (e.g., add/update user in database)
            # For now, let's print it to the console
            print(f"User Type: {user_type}, Name: {name}, Status: {'Active' if status else 'Inactive'}, Admin: {'Yes' if is_admin else 'No'}")

            # Redirect to a success page or another route after processing
            return redirect(url_for('success_page'))  # Change 'success_page' to your actual success route

        else:
            # If validation fails, reload the form with an error message
            error_message = "Please fill all the required fields."
            return render_template('add_user.html', error_message=error_message)
    
    # Render the form for GET requests
    return render_template('add_user.html')
@app.route('/update_user', methods=['GET', 'POST'])
def update_user():
    if request.method == 'POST':
        # Retrieve form data
        user_select = request.form.get('userSelect')
        name = request.form.get('name').strip()
        status = 'status' in request.form  # Checkbox status
        is_admin = 'admin' in request.form  # Checkbox status

        # Check if all required fields are filled
        if user_select and name:
            # Process the form data (e.g., update user in database)
            # For now, let's print it to the console
            print(f"Selected User: {user_select}, Updated Name: {name}, Status: {'Active' if status else 'Inactive'}, Admin: {'Yes' if is_admin else 'No'}")

            # Redirect to a success page or another route after processing
            return redirect(url_for('success_page'))  # Change 'success_page' to your actual success route

        else:
            # If validation fails, reload the form with an error message
            error_message = "Please select a user and fill in the required fields."
            return render_template('update_user.html', error_message=error_message)
    
    # Render the form for GET requests
    return render_template('update_user.html')
#search form

books = [
    {"name": "Book A", "author": "Author A", "serial": 12345, "available": "Y"},
    {"name": "Book B", "author": "Author B", "serial": 67890, "available": "Y"},
    {"name": "Book C", "author": "Author C", "serial": 54321, "available": "Y"},
    {"name": "Book D", "author": "Author D", "serial": 98765, "available": "N"}
]

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        # Get the search query from the form (e.g., book name or author)
        search_query = request.form.get('search_query', '').lower()

        # Filter the books based on the search query
        results = [book for book in books if search_query in book['name'].lower() or search_query in book['author'].lower()]

        # Render the template with the search results
        #return render_template('search_results.html', books=results)
    
    # If it's a GET request, just display the search form
    return render_template('search_form.html')

#cancel
@app.route('/cancel')
def cancel_page():
    return render_template('cancel.html')
#reports
@app.route('/reports')
def reports():
    # Ensure session is active and the role is admin
    if 'role' in session and session['role'] == 'admin':
        return render_template('reports.html')
    else:
        flash('Unauthorized access! Please log in as admin.')
        return redirect(url_for('login'))


@app.route('/reports/master_list_books')
def master_list_books():
    # Ensure session is active and the role is admin
    if 'role' in session and session['role'] == 'admin':
        # Render the master list of books report
        return render_template('master_list_books.html')
    else:
        flash('Unauthorized access! Please log in as admin.')
        return redirect(url_for('login'))


@app.route('/reports/master_list_movies')
def master_list_movies():
    # Ensure session is active and the role is admin
    if 'role' in session and session['role'] == 'admin':
        # Render the master list of movies report
        return render_template('master_list_movies.html')
    else:
        flash('Unauthorized access! Please log in as admin.')
        return redirect(url_for('login'))


@app.route('/reports/master_list_memberships')
def master_list_memberships():
    # Ensure session is active and the role is admin
    if 'role' in session and session['role'] == 'admin':
        # Render the master list of memberships report
        return render_template('master_list_memberships.html')
    else:
        flash('Unauthorized access! Please log in as admin.')
        return redirect(url_for('login'))


@app.route('/reports/active_issues')
def active_issues():
    # Ensure session is active and the role is admin
    if 'role' in session and session['role'] == 'admin':
        # Render the active issues report
        return render_template('active_issues.html')
    else:
        flash('Unauthorized access! Please log in as admin.')
        return redirect(url_for('login'))


@app.route('/reports/overdue_returns')
def overdue_returns():
    # Ensure session is active and the role is admin
    if 'role' in session and session['role'] == 'admin':
        # Render the overdue returns report
        return render_template('overdue_returns.html')
    else:
        flash('Unauthorized access! Please log in as admin.')
        return redirect(url_for('login'))


@app.route('/reports/issue_requests')
def issue_requests():
    # Ensure session is active and the role is admin
    if 'role' in session and session['role'] == 'admin':
        # Render the issue requests report
        return render_template('issue_requests.html')
    else:
        flash('Unauthorized access! Please log in as admin.')
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
