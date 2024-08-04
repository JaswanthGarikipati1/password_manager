from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, make_response
from .models import db, User, PasswordEntry
from .utils import create_cipher_suite, encrypt_text, decrypt_text
from werkzeug.security import check_password_hash

bp = Blueprint('password_manager', __name__)

from flask import session

#main page of the project
@bp.route('/')
def index():
    user_id = 1  # Replace with the actual user ID
    entries = PasswordEntry.query.filter_by(user_id=user_id).all()
    return render_template('index.html', entries=entries)

#used to add the user entries from the form
@bp.route('/add_entry', methods=['POST'])
def add_entry():
    user_id = 1 
    website = request.form['website']
    username = request.form['username']
    password = request.form['password']

    # Create the cipher_suite within the application context
    cipher_suite = create_cipher_suite(current_app.config['SECRET_KEY'])
    
    encrypted_password = encrypt_text(cipher_suite, password)

    new_entry = PasswordEntry(user_id=user_id, website=website, username=username, encrypted_password=encrypted_password)
    db.session.add(new_entry)
    db.session.commit()

    flash('Password entry added successfully!', 'success')
    return redirect(url_for('password_manager.index'))

#function for admin login page
@bp.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        #admin_user = User.query.filter_by(username=username).first() --- I forgot my password :(
        admin_user = 'adminuser'
        #if admin_user and check_password_hash(admin_user.hashed_password, password): --- uncomment this line if you remember your password :)
        if admin_user and password=='Jaswanth@12':
            session['admin_authenticated'] = True
            flash('Login successful!', 'success')
            return redirect(url_for('password_manager.admin_dashboard'))

        flash('Invalid username or password', 'danger')

    return render_template('admin_login.html')

#admin logout function
@bp.route('/admin_logout')
def admin_logout():
    session.pop('admin_authenticated', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('password_manager.admin_login'))

#this is the dashboard for admin
@bp.route('/admin_dashboard')
def admin_dashboard():
    if 'admin_authenticated' not in session:
        flash('You need to log in as an admin', 'danger')
        return redirect(url_for('password_manager.admin_login'))

    # Query the database for password entries
    entries = PasswordEntry.query.all()

    # Decrypt passwords for display
    cipher_suite = create_cipher_suite(current_app.config['SECRET_KEY'])
    for entry in entries:
        entry.decrypted_password = decrypt_text(cipher_suite, entry.encrypted_password)

    return render_template('admin_dashboard.html', entries=entries)

#delete the given entry
@bp.route('/delete_entry/<int:entry_id>', methods=['GET', 'POST'])
def delete_entry(entry_id):
    entry = PasswordEntry.query.get_or_404(entry_id)
    
    if request.method == 'POST':
        db.session.delete(entry)
        db.session.commit()
        flash('Password deleted successfully', 'success')
        return redirect(url_for('password_manager.admin_dashboard'))

    return render_template('delete_entry.html', entry=entry)



def is_authenticated_admin():
    # Check if the user is authenticated as an admin
    return True




