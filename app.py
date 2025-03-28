from flask import Flask, render_template, render_template_string, request, redirect, url_for, flash, jsonify
import sqlite3
from datetime import datetime, timedelta
import os
import traceback
from functools import wraps
import secrets
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['DEBUG'] = True

# Add these constants after the app configuration
API_KEYS = {
    'company_website': secrets.token_urlsafe(32)
}

def get_db():
    conn = sqlite3.connect('narmer.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    try:
        # Delete existing database if it exists
        if os.path.exists('narmer.db'):
            os.remove('narmer.db')
        
        conn = get_db()
        c = conn.cursor()
        
        # Create customers table with all columns
        c.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                company TEXT,
                phone TEXT,
                industry TEXT,
                website TEXT,
                notes TEXT,
                status TEXT DEFAULT 'active',
                last_contact TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create landing_pages table
        c.execute('''
            CREATE TABLE IF NOT EXISTS landing_pages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER,
                title TEXT NOT NULL,
                template TEXT,
                content TEXT NOT NULL,
                status TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers (id)
            )
        ''')
        
        # Insert some sample data
        c.execute('''
            INSERT INTO customers (name, email, company, phone, industry, website, notes, status)
            VALUES 
            ('John Doe', 'john@example.com', 'Tech Corp', '+1234567890', 'Technology', 'https://techcorp.com', 'Sample customer', 'active'),
            ('Jane Smith', 'jane@example.com', 'Health Inc', '+0987654321', 'Healthcare', 'https://healthinc.com', 'Another sample', 'active')
        ''')
        
        conn.commit()
        conn.close()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {str(e)}")
        print(traceback.format_exc())

# Initialize the database
# init_db()  # Commenting out automatic initialization since we've already done it

# Base HTML template with improved styling
BASE_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>CRM System</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f8f9fa;
        }
        .navbar { 
            background-color: #2c3e50; 
            padding: 1rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .navbar-brand { 
            color: white !important; 
            font-weight: bold;
            font-size: 1.5rem;
        }
        .nav-link { 
            color: rgba(255,255,255,0.8) !important;
            margin: 0 0.5rem;
            transition: color 0.3s;
        }
        .nav-link:hover { 
            color: white !important;
        }
        .container { 
            margin-top: 2rem;
            max-width: 1200px;
        }
        .card {
            border: none;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 1.5rem;
            transition: transform 0.3s;
        }
        .card:hover {
            transform: translateY(-5px);
        }
        .card-header {
            background-color: #fff;
            border-bottom: 1px solid #eee;
            padding: 1rem;
        }
        .btn-primary {
            background-color: #3498db;
            border: none;
            padding: 0.5rem 1rem;
        }
        .btn-primary:hover {
            background-color: #2980b9;
        }
        .stats-card {
            background: linear-gradient(45deg, #3498db, #2ecc71);
            color: white;
            padding: 1.5rem;
            border-radius: 10px;
            margin-bottom: 1rem;
        }
        .stats-number {
            font-size: 2rem;
            font-weight: bold;
        }
        .flash-messages {
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
        }
        .search-box {
            margin-bottom: 2rem;
        }
        .alert {
            border: none;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .alert-success {
            background-color: #2ecc71;
            color: white;
        }
        .alert-error {
            background-color: #e74c3c;
            color: white;
        }
        .form-control:focus {
            border-color: #3498db;
            box-shadow: 0 0 0 0.2rem rgba(52, 152, 219, 0.25);
        }
        .table {
            margin-bottom: 0;
        }
        .table th {
            border-top: none;
            background-color: #f8f9fa;
        }
        .badge {
            padding: 0.5em 0.8em;
            font-weight: 500;
        }
        .btn-sm {
            padding: 0.25rem 0.5rem;
            font-size: 0.875rem;
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg">
        <div class="container">
            <a class="navbar-brand" href="/"><i class="fas fa-users-cog"></i> CRM System</a>
            <div class="collapse navbar-collapse">
                <ul class="navbar-nav">
                    <li class="nav-item"><a class="nav-link" href="/"><i class="fas fa-home"></i> Dashboard</a></li>
                    <li class="nav-item"><a class="nav-link" href="/customers"><i class="fas fa-users"></i> Customers</a></li>
                    <li class="nav-item"><a class="nav-link" href="/add_customer"><i class="fas fa-user-plus"></i> Add Customer</a></li>
                    <li class="nav-item"><a class="nav-link" href="/landing_pages"><i class="fas fa-file-alt"></i> Landing Pages</a></li>
                </ul>
            </div>
        </div>
    </nav>
    <div class="container">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                <div class="flash-messages">
                    {% for category, message in messages %}
                        <div class="alert alert-{{ category }} alert-dismissible fade show" role="alert">
                            {{ message }}
                            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                        </div>
                    {% endfor %}
                </div>
            {% endif %}
        {% endwith %}
        {content}
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Auto-dismiss flash messages after 5 seconds
        document.addEventListener('DOMContentLoaded', function() {
            setTimeout(function() {
                var alerts = document.querySelectorAll('.alert');
                alerts.forEach(function(alert) {
                    var bsAlert = new bootstrap.Alert(alert);
                    bsAlert.close();
                });
            }, 5000);
        });
    </script>
</body>
</html>
'''

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key and api_key in API_KEYS.values():
            return f(*args, **kwargs)
        return jsonify({'error': 'Invalid API key'}), 401
    return decorated_function

@app.route('/')
def index():
    conn = get_db()
    cursor = conn.cursor()
    
    # Get total counts
    cursor.execute('SELECT COUNT(*) as count FROM customers')
    total_customers = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM landing_pages')
    total_landing_pages = cursor.fetchone()['count']
    
    # Get recent customers
    cursor.execute('''
        SELECT id, name, company, industry, status, 
               datetime(created_at) as created_at
        FROM customers 
        ORDER BY created_at DESC 
        LIMIT 5
    ''')
    recent_customers = [dict(row) for row in cursor.fetchall()]
    
    # Get recent landing pages
    cursor.execute('''
        SELECT lp.id, lp.title, c.name as customer_name, lp.template, lp.status, 
               datetime(lp.created_at) as created_at
        FROM landing_pages lp 
        JOIN customers c ON lp.customer_id = c.id 
        ORDER BY lp.created_at DESC 
        LIMIT 5
    ''')
    recent_pages = [dict(row) for row in cursor.fetchall()]
    
    # Get recent activity (last 24 hours)
    yesterday = datetime.now() - timedelta(days=1)
    cursor.execute('''
        SELECT COUNT(*) as count 
        FROM (
            SELECT created_at FROM customers WHERE datetime(created_at) > datetime(?)
            UNION ALL
            SELECT created_at FROM landing_pages WHERE datetime(created_at) > datetime(?)
        )
    ''', (yesterday.strftime('%Y-%m-%d %H:%M:%S'), yesterday.strftime('%Y-%m-%d %H:%M:%S')))
    recent_activity = cursor.fetchone()['count']
    
    conn.close()
    
    # Convert string timestamps to datetime objects
    for customer in recent_customers:
        if customer['created_at']:
            customer['created_at'] = datetime.strptime(customer['created_at'], '%Y-%m-%d %H:%M:%S')
    
    for page in recent_pages:
        if page['created_at']:
            page['created_at'] = datetime.strptime(page['created_at'], '%Y-%m-%d %H:%M:%S')
    
    return render_template('index.html',
                         total_customers=total_customers,
                         total_landing_pages=total_landing_pages,
                         recent_customers=recent_customers,
                         recent_pages=recent_pages,
                         recent_activity=recent_activity)

@app.route('/customers')
def customers():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM customers ORDER BY created_at DESC')
    customers = cursor.fetchall()
    conn.close()
    return render_template('customers.html', customers=customers)

@app.route('/customers/add', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        company = request.form['company']
        phone = request.form['phone']
        industry = request.form['industry']
        website = request.form['website']
        notes = request.form['notes']
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO customers (name, email, company, phone, industry, website, notes, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'active', ?)
        ''', (name, email, company, phone, industry, website, notes, datetime.now()))
        conn.commit()
        conn.close()
        
        flash('Customer added successfully!', 'success')
        return redirect(url_for('customers'))
    
    return render_template('add_customer.html')

@app.route('/customers/<int:customer_id>/edit', methods=['GET', 'POST'])
def edit_customer(customer_id):
    conn = get_db()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        company = request.form['company']
        phone = request.form['phone']
        industry = request.form['industry']
        website = request.form['website']
        notes = request.form['notes']
        
        cursor.execute('''
            UPDATE customers 
            SET name = ?, email = ?, company = ?, phone = ?, industry = ?, website = ?, notes = ?
            WHERE id = ?
        ''', (name, email, company, phone, industry, website, notes, customer_id))
        conn.commit()
        
        flash('Customer updated successfully!', 'success')
        return redirect(url_for('customers'))
    
    cursor.execute('SELECT * FROM customers WHERE id = ?', (customer_id,))
    customer = cursor.fetchone()
    conn.close()
    
    if customer is None:
        flash('Customer not found!', 'error')
        return redirect(url_for('customers'))
    
    return render_template('edit_customer.html', customer=customer)

@app.route('/customers/<int:customer_id>/delete', methods=['POST'])
def delete_customer(customer_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM customers WHERE id = ?', (customer_id,))
    conn.commit()
    conn.close()
    
    flash('Customer deleted successfully!', 'success')
    return redirect(url_for('customers'))

@app.route('/landing-pages')
def landing_pages():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT lp.*, c.name as customer_name,
               datetime(lp.created_at) as created_at
        FROM landing_pages lp 
        JOIN customers c ON lp.customer_id = c.id 
        ORDER BY lp.created_at DESC
    ''')
    landing_pages = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    # Convert string timestamps to datetime objects
    for page in landing_pages:
        if page['created_at']:
            page['created_at'] = datetime.strptime(page['created_at'], '%Y-%m-%d %H:%M:%S')
    
    return render_template('landing_pages.html', landing_pages=landing_pages)

@app.route('/landing-pages/add', methods=['GET', 'POST'])
def add_landing_page():
    if request.method == 'POST':
        title = request.form['title']
        customer_id = request.form['customer_id']
        template = request.form['template']
        content = request.form['content']
        status = request.form['status']
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO landing_pages (title, customer_id, template, content, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, customer_id, template, content, status, datetime.now()))
        conn.commit()
        conn.close()
        
        flash('Landing page created successfully!', 'success')
        return redirect(url_for('landing_pages'))
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM customers ORDER BY name')
    customers = cursor.fetchall()
    conn.close()
    
    return render_template('add_landing_page.html', customers=customers)

@app.route('/landing-pages/<int:page_id>/edit', methods=['GET', 'POST'])
def edit_landing_page(page_id):
    conn = get_db()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        title = request.form['title']
        customer_id = request.form['customer_id']
        template = request.form['template']
        content = request.form['content']
        status = request.form['status']
        
        cursor.execute('''
            UPDATE landing_pages 
            SET title = ?, customer_id = ?, template = ?, content = ?, status = ?
            WHERE id = ?
        ''', (title, customer_id, template, content, status, page_id))
        conn.commit()
        
        flash('Landing page updated successfully!', 'success')
        return redirect(url_for('landing_pages'))
    
    cursor.execute('SELECT * FROM landing_pages WHERE id = ?', (page_id,))
    page = cursor.fetchone()
    
    cursor.execute('SELECT * FROM customers ORDER BY name')
    customers = cursor.fetchall()
    conn.close()
    
    if page is None:
        flash('Landing page not found!', 'error')
        return redirect(url_for('landing_pages'))
    
    return render_template('edit_landing_page.html', page=page, customers=customers)

@app.route('/landing-pages/<int:page_id>/delete', methods=['POST'])
def delete_landing_page(page_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM landing_pages WHERE id = ?', (page_id,))
    conn.commit()
    conn.close()
    
    flash('Landing page deleted successfully!', 'success')
    return redirect(url_for('landing_pages'))

@app.route('/landing-pages/<int:page_id>/preview')
def preview_landing_page(page_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT lp.*, c.name as customer_name,
               datetime(lp.created_at) as created_at
        FROM landing_pages lp 
        JOIN customers c ON lp.customer_id = c.id 
        WHERE lp.id = ?
    ''', (page_id,))
    page = cursor.fetchone()
    conn.close()
    
    if page is None:
        flash('Landing page not found!', 'error')
        return redirect(url_for('landing_pages'))
    
    # Convert string timestamp to datetime object
    if page['created_at']:
        page['created_at'] = datetime.strptime(page['created_at'], '%Y-%m-%d %H:%M:%S')
    
    return render_template('preview_landing_page.html', page=page)

@app.route('/api/customers')
def api_customers():
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute('SELECT * FROM customers')
        customers = c.fetchall()
        conn.close()
        return jsonify([dict(customer) for customer in customers])
    except Exception as e:
        print(f"Error in api_customers route: {str(e)}")
        print(traceback.format_exc())
        return str(e), 500

@app.route('/company-website')
def company_website():
    return render_template('demo_company.html', api_key=API_KEYS['company_website'])

@app.route('/api/company-content', methods=['GET'])
@require_api_key
def get_company_content():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT section, content, last_updated
        FROM company_content
        ORDER BY section
    ''')
    content = {row['section']: row['content'] for row in cursor.fetchall()}
    conn.close()
    return jsonify(content)

@app.route('/api/company-content', methods=['POST'])
@require_api_key
def update_company_content():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Create table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS company_content (
                section TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Update or insert content for each section
        for section, content in data.items():
            cursor.execute('''
                INSERT OR REPLACE INTO company_content (section, content, last_updated)
                VALUES (?, ?, ?)
            ''', (section, content, datetime.now()))
        
        conn.commit()
        conn.close()
        return jsonify({'message': 'Content updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/company-content')
def manage_company_content():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT section, content, last_updated
        FROM company_content
        ORDER BY section
    ''')
    content = cursor.fetchall()
    conn.close()
    return render_template('manage_company_content.html', content=content)

@app.route('/company-content/update', methods=['POST'])
def update_content():
    try:
        section = request.form.get('section')
        content = request.form.get('content')
        
        if not section or not content:
            flash('Section and content are required', 'error')
            return redirect(url_for('manage_company_content'))
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO company_content (section, content, last_updated)
            VALUES (?, ?, ?)
        ''', (section, content, datetime.now()))
        conn.commit()
        conn.close()
        
        flash('Content updated successfully', 'success')
        return redirect(url_for('manage_company_content'))
    except Exception as e:
        flash(f'Error updating content: {str(e)}', 'error')
        return redirect(url_for('manage_company_content'))

if __name__ == '__main__':
    print("Starting the application...")
    app.run(debug=True) 