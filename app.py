from flask import (
    Flask, render_template, jsonify, redirect, url_for, request,
    flash, session, make_response
)
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import datetime
import logging
from functools import wraps
import MySQLdb  # for better exception messages

app = Flask(__name__)

# -------------------------
# Configuration
# -------------------------
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', 'kane@22*')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'parking_system1')
app.config['MYSQL_PORT'] = int(os.getenv('MYSQL_PORT', 3306))
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'static/uploads')
app.config['ALLOWED_EXTENSIONS'] = set(os.getenv('ALLOWED_EXTENSIONS', 'png,jpg,jpeg,gif').split(','))
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5 MB
app.secret_key = os.getenv('SECRET_KEY', 'f894cb67a8c0b040dc8243b0864a320f')

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
mysql = MySQL(app)
logging.basicConfig(level=logging.DEBUG)

# -------------------------
# Decorators
# -------------------------
def admin_required(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if not session.get('is_admin'):
            flash('Unauthorized access! Only admins can access this page.', 'danger')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_func

# -------------------------
# Helper functions
# -------------------------
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def get_cursor():
    try:
        cur = mysql.connection.cursor()
        return cur
    except Exception as e:
        logging.error(f"DB connection error in get_cursor: {e}")
        return None

def test_db_connection():
    cur = get_cursor()
    if not cur:
        return False
    try:
        cur.execute("SELECT 1")
        cur.close()
        return True
    except Exception as e:
        logging.error(f"Database connection failed during test query: {e}")
        return False

if not test_db_connection():
    logging.error("Failed to connect to database. Please check your MySQL configuration.")
    print("❌ Database connection failed!")
    print("Please ensure:\n1. MySQL server is running\n2. Database 'parking_system1' exists\n3. User credentials are correct\n4. Run: mysql -u root -p < database_setup.sql")
else:
    print("✅ Database connection successful!")

# -------------------------
# Routes
# -------------------------
@app.route('/')
def index():
    try:
        cur = get_cursor()
        if not cur:
            raise Exception("Database cursor not available")
        cur.execute("SELECT COUNT(*) FROM users")
        user_count = cur.fetchone()[0] or 0
        cur.execute("SELECT title, message, created_at FROM notifications ORDER BY created_at DESC")
        notifications = cur.fetchall()
        cur.close()
    except Exception as e:
        logging.error(f"Error fetching data for index: {e}")
        user_count = 0
        notifications = []
    return render_template('index.html', user_count=user_count, notifications=notifications)

@app.route('/notification')
def notification():
    try:
        cur = get_cursor()
        if not cur:
            raise Exception("Database cursor not available")
        cur.execute("SELECT title, message, created_at FROM notifications ORDER BY created_at DESC")
        notifications = cur.fetchall()
        cur.close()
    except Exception as e:
        logging.error(f"Error fetching notifications: {e}")
        notifications = []
    return render_template('notifications.html', notifications=notifications)

# ----------------- Admin -----------------
@app.route('/admin_register', methods=['GET', 'POST'])
def admin_register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not username or not email or not password:
            flash('Please fill all required fields.', 'danger')
            return redirect(url_for('admin_register'))
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('admin_register'))

        hashed_password = generate_password_hash(password)
        try:
            cur = get_cursor()
            if not cur:
                raise Exception("Database not available")
            cur.execute(
                'INSERT INTO admins (username, email, password) VALUES (%s, %s, %s)',
                (username, email, hashed_password)
            )
            mysql.connection.commit()
            cur.close()
            flash('Admin registration successful!', 'success')
            return redirect(url_for('admin_login'))
        except MySQLdb.Error as e:
            logging.error(f"MySQL Error during admin_register: {e}")
            flash('An error occurred during registration. Maybe email/username already exists.', 'danger')
        except Exception as e:
            logging.error(f"Error during admin registration: {e}")
            flash('An error occurred during registration. Please try again.', 'danger')
    return render_template('admin_register.html')

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        try:
            cur = get_cursor()
            if not cur:
                raise Exception("Database not available")
            cur.execute("SELECT id, username, email, password FROM admins WHERE email = %s", (email,))
            admin_user = cur.fetchone()
            cur.close()
            if admin_user is None or not check_password_hash(admin_user[3], password):
                flash('Invalid email or password.', 'danger')
                return redirect(url_for('admin_login'))
            session['admin_id'] = admin_user[0]
            session['admin_username'] = admin_user[1]
            session['is_admin'] = True
            flash('Admin login successful!', 'success')
            logging.info(f"Admin {admin_user[1]} logged in successfully.")
            return redirect(url_for('admin_dashboard'))
        except Exception as e:
            logging.error(f"Admin login error: {e}")
            flash('Database error. Please try again later.', 'danger')
            return redirect(url_for('admin_login'))
    return render_template('admin_login.html')

@app.route('/admin_dashboard')
@admin_required
def admin_dashboard():
    try:
        cur = get_cursor()
        if not cur:
            raise Exception("Database not available")
        cur.execute("SELECT id, username, email, phone, created_at FROM users")
        users = cur.fetchall()
        cur.execute("SELECT id, location, slot_number, status, user_id FROM ParkingSlot")
        slots = cur.fetchall()
        cur.execute("SELECT id, user_id, plot_no, vehicle_no, vehicle_type, hours, amount, payment_type, payment_status, created_at FROM payments")
        payments = cur.fetchall()
        cur.execute("SELECT SUM(amount) FROM payments")
        total_sum = cur.fetchone()[0]
        total_amount = float(total_sum) if total_sum is not None else 0.0
        cur.close()
    except Exception as e:
        logging.error(f"Error fetching admin data: {e}")
        users, slots, payments, total_amount = [], [], [], 0
    return render_template('admin_dashboard.html',
        admin_username=session.get('admin_username'),
        users=users, slots=slots, payments=payments,
        total_amount=total_amount
    )

@app.route('/admin_add_features', methods=['GET', 'POST'])
@admin_required
def admin_add_features():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('content', '').strip()
        icon = request.form.get('icon', '🚗')
        try:
            cur = get_cursor()
            if not cur:
                raise Exception("Database not available")
            cur.execute("INSERT INTO features (title, description, icon) VALUES (%s, %s, %s)",
                        (title, description, icon))
            mysql.connection.commit()
            cur.close()
            flash('Feature content added successfully!', 'success')
        except Exception as e:
            logging.error(f"Error adding feature content: {e}")
            flash('An error occurred while adding feature content. Please try again.', 'danger')
    return render_template('admin_add_features.html')

@app.route('/admin_add_guidelines', methods=['GET', 'POST'])
@admin_required
def admin_add_guidelines():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        category = request.form.get('category', 'general').strip()
        try:
            cur = get_cursor()
            if not cur:
                raise Exception("Database not available")
            cur.execute("INSERT INTO guidelines (title, content, category) VALUES (%s, %s, %s)",
                        (title, content, category))
            mysql.connection.commit()
            cur.close()
            flash('Guideline content added successfully!', 'success')
        except Exception as e:
            logging.error(f"Error adding guideline content: {e}")
            flash('An error occurred while adding guideline content. Please try again.', 'danger')
    return render_template('admin_add_guidelines.html')

# ----------------- User -----------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirmPassword', '')
        phone = request.form.get('phone', '').strip()
        if not username or not email or not password:
            flash('Please fill all required fields.', 'danger')
            return redirect(url_for('register'))
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('register'))
        hashed_password = generate_password_hash(password)
        avatar = None
        if 'avatarUpload' in request.files:
            avatar_file = request.files['avatarUpload']
            if avatar_file and allowed_file(avatar_file.filename):
                filename = secure_filename(avatar_file.filename)
                avatar_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                avatar_file.save(avatar_path)
                avatar = filename
        try:
            cur = get_cursor()
            if not cur:
                raise Exception("Database not available")
            cur.execute(
                'INSERT INTO users (username, email, password, phone, profile_picture) VALUES (%s, %s, %s, %s, %s)',
                (username, email, hashed_password, phone, avatar)
            )
            mysql.connection.commit()
            user_id = cur.lastrowid
            cur.close()
            flash('Registration successful!', 'success')
            session['user_id'] = user_id
            session['username'] = username
            return redirect(url_for('webpage'))
        except MySQLdb.Error as e:
            logging.error(f"MySQL Error during registration: {e}")
            flash('Registration failed: Email or username might already exist.', 'danger')
        except Exception as e:
            logging.error(f"Error during registration: {e}")
            flash('An error occurred during registration. Please try again.', 'danger')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        try:
            cur = get_cursor()
            if not cur:
                raise Exception("Database connection or cursor not available")
            cur.execute("SHOW TABLES LIKE 'users'")
            if not cur.fetchone():
                logging.error("Table 'users' does not exist in database.")
                flash("Database table 'users' is missing.", 'danger')
                return redirect(url_for('login'))
            cur.execute("SELECT id, username, email, password FROM users WHERE email = %s", (email,))
            user = cur.fetchone()
            cur.close()
            if user is None or not check_password_hash(user[3], password):
                flash('Invalid email or password.', 'danger')
                return redirect(url_for('login'))
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['is_admin'] = False
            flash('Login successful!', 'success')
            logging.info(f"User {user[1]} logged in successfully.")
            return redirect(url_for('webpage'))
        except MySQLdb.Error as e:
            logging.error(f"MySQL Error during login: {e}")
            flash(f"MySQL error: {e}", 'danger')
        except Exception as e:
            logging.error(f"Login error: {e}")
            flash(f"Error: {e}", 'danger')
    return render_template('login.html')

@app.route('/webpage')
def webpage():
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('login'))
    logging.info(f"Rendering webpage for user {session.get('username')}")
    return render_template('webpage.html', username=session.get('username'))

@app.route('/features')
def features():
    try:
        cur = get_cursor()
        if not cur:
            raise Exception("Database not available")
        cur.execute("SELECT title, description, icon FROM features WHERE is_active = TRUE")
        features_content = cur.fetchall()
        cur.close()
    except Exception as e:
        logging.error(f"Error fetching features content: {e}")
        features_content = []
    return render_template('features.html', features_content=features_content)

@app.route('/guidelines')
def guidelines():
    try:
        cur = get_cursor()
        if not cur:
            raise Exception("Database not available")
        cur.execute("SELECT title, content, category FROM guidelines WHERE is_active = TRUE")
        guidelines_content = cur.fetchall()
        cur.close()
    except Exception as e:
        logging.error(f"Error fetching guidelines content: {e}")
        guidelines_content = []
    return render_template('guidelines.html', guidelines_content=guidelines_content)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

@app.route('/pricing1')
def pricing1():
    return render_template('pricing1.html')

@app.route('/pricing2')
def pricing2():
    return render_template('pricing2.html')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/slots/<location>')
def slots(location):
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('login'))
    try:
        cur = get_cursor()
        if not cur:
            raise Exception("Database not available")
        cur.execute("SELECT id, location, slot_number, status FROM ParkingSlot WHERE location = %s", (location,))
        slots = cur.fetchall()
        cur.close()
        slots = list(slots)
        if len(slots) < 20:
            for i in range(len(slots), 20):
                slots.append((None, location, i + 1, 'available'))
        return render_template('slots.html', location=location, slots=slots)
    except Exception as e:
        logging.error(f"Error fetching slots for location '{location}': {e}")
        flash('An error occurred while fetching slots. Please try again.', 'danger')
        return redirect(url_for('index'))

@app.route('/book_slot', methods=['POST'])
def book_slot():
    if 'user_id' not in session:
        flash('Please log in to book a slot.', 'danger')
        return redirect(url_for('login'))
    slot_id = request.form.get('slot_id')
    slot_number = request.form.get('slot_number')
    location = request.form.get('location')
    user_id = session.get('user_id')
    if not slot_number or not location:
        flash('Missing slot information.', 'danger')
        return redirect(url_for('index'))
    try:
        cur = get_cursor()
        if not cur:
            raise Exception("Database not available")
        cur.execute("""
            UPDATE ParkingSlot
            SET status = 'booked', user_id = %s, slot_number = %s
            WHERE id = %s AND location = %s AND status = 'available'
        """, (user_id, slot_number, slot_id, location))
        mysql.connection.commit()
        if cur.rowcount == 0:
            flash('Slot is already booked or unavailable.', 'danger')
            cur.close()
            return redirect(url_for('slots', location=location))
        else:
            flash('Slot booked successfully!', 'success')
            cur.close()
            return redirect(url_for('payment', slotNumber=slot_number))
    except Exception as e:
        logging.error(f"Error booking slot: {e}")
        flash('An error occurred while booking the slot. Please try again.', 'danger')
        return redirect(url_for('slots', location=location))

@app.route('/payment')
def payment():
    slotNumber = request.args.get('slotNumber')
    return render_template('payment.html', slotNumber=slotNumber)

@app.route('/process_payment', methods=['POST'])
def process_payment():
    try:
        plot_no = request.form.get('plotNo')
        vehicle_no = request.form.get('vehicleNo')
        vehicle_type = request.form.get('vehicleType')
        hours = int(request.form.get('hours', 0))
        amount = float(request.form.get('amount', 0))
        payment_type = request.form.get('paymentType')
        user_id = session.get('user_id')
        if not all([plot_no, vehicle_no, vehicle_type, hours, amount, payment_type]):
            return jsonify({'error': 'All fields are required!'}), 400
        cur = get_cursor()
        if not cur:
            raise Exception("Database not available")
        cur.execute("""
            INSERT INTO payments (user_id, plot_no, vehicle_no, vehicle_type, hours, amount, payment_type, payment_status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (user_id, plot_no, vehicle_no, vehicle_type, hours, amount, payment_type, 'completed'))
        mysql.connection.commit()
        payment_id = cur.lastrowid
        cur.close()
        return jsonify({
            'message': 'Payment processed successfully!',
            'payment_id': payment_id, 'plot_no': plot_no,
            'amount': amount, 'date': str(datetime.date.today())
        }), 200
    except Exception as e:
        logging.error(f"Error processing payment: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/calculate_amount', methods=['POST'])
def calculate_amount():
    try:
        data = request.get_json() or {}
        vehicle_type = data.get('vehicleType')
        hours = int(data.get('hours', 0))
        if vehicle_type not in ['2wheeler', '4wheeler']:
            return jsonify({'error': 'Invalid vehicle type!'}), 400
        if hours <= 0:
            return jsonify({'error': 'Invalid hours!'}), 400
        if vehicle_type == '2wheeler':
            amount = 20 if hours <= 2 else 20 + (hours - 2) * 10
        else:
            amount = 40 if hours <= 2 else 40 + (hours - 2) * 20
        return jsonify({'amount': amount}), 200
    except Exception as e:
        logging.error(f"Error calculating amount: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/generate_bill', methods=['GET', 'POST'])
def generate_bill():
    try:
        payment_id = request.args.get('paymentId') if request.method == 'GET' else request.form.get('paymentId')
        if not payment_id:
            return jsonify({'error': 'Payment ID is required'}), 400
        cur = get_cursor()
        if not cur:
            raise Exception("Database not available")
        cur.execute("""
            SELECT p.id, p.plot_no, p.vehicle_no, p.vehicle_type, p.hours, p.amount, p.payment_type, p.created_at, u.username
            FROM payments p
            JOIN users u ON p.user_id = u.id
            WHERE p.id = %s
        """, (payment_id,))
        payment_data = cur.fetchone()
        cur.close()
        if not payment_data:
            return jsonify({'error': 'Payment not found'}), 404
        (p_id, plot_no, vehicle_no, vehicle_type, hours, amount, payment_type, created_at, username) = payment_data
        bill_id = f"BILL-{int(p_id):06d}"
        payment_date = created_at.strftime("%Y-%m-%d") if created_at else datetime.date.today().strftime("%Y-%m-%d")
        payment_time = created_at.strftime("%H:%M:%S") if created_at else datetime.datetime.now().strftime("%H:%M:%S")
        rendered = render_template('bill.html',
            bill_id=bill_id, payment_id=p_id, slot_id=plot_no, amount=amount,
            date=payment_date, time=payment_time, username=username,
            vehicle_no=vehicle_no, vehicle_type=vehicle_type, hours=hours, payment_type=payment_type
        )
        try:
            import pdfkit
            wk_paths = [
                '/usr/local/bin/wkhtmltopdf',
                '/usr/bin/wkhtmltopdf',
                'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe',
                os.getenv('WKHTMLTOPDF_PATH', '')
            ]
            config = None
            for path in wk_paths:
                if path and os.path.isfile(path):
                    config = pdfkit.configuration(wkhtmltopdf=path)
                    break
            options = {'page-size': 'A4', 'encoding': 'UTF-8'}
            if config:
                pdf_content = pdfkit.from_string(rendered, False, configuration=config, options=options)
                response = make_response(pdf_content)
                response.headers['Content-Type'] = 'application/pdf'
                response.headers['Content-Disposition'] = f'attachment; filename=bill_{p_id}.pdf'
                return response
            else:
                logging.warning("wkhtmltopdf not found; returning HTML bill")
                return rendered
        except ImportError:
            logging.warning("pdfkit not installed; returning HTML bill")
            return rendered
        except Exception as pdf_err:
            logging.error(f"PDF generation error: {pdf_err}")
            return rendered
    except Exception as e:
        logging.error(f"Error generating bill: {e}")
        return jsonify({'error': str(e)}), 500

# -------------------------
# Run
# -------------------------
if __name__ == '__main__':
    app.run(debug=True)