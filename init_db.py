import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('narmer.db')
    cursor = conn.cursor()
    
    # Create customers table
    cursor.execute('''
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
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create landing_pages table
    cursor.execute('''
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
    
    # Insert sample customers
    sample_customers = [
        ('John Doe', 'john@example.com', 'Acme Corp', '+1-555-0123', 'Technology', 'https://acme.com', 'VIP customer'),
        ('Jane Smith', 'jane@example.com', 'TechStart Inc', '+1-555-0124', 'Startup', 'https://techstart.com', 'New customer'),
        ('Bob Johnson', 'bob@example.com', 'Global Industries', '+1-555-0125', 'Manufacturing', 'https://global.com', 'Enterprise customer')
    ]
    
    for customer in sample_customers:
        cursor.execute('''
            INSERT INTO customers (name, email, company, phone, industry, website, notes, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'active', ?)
        ''', (*customer, datetime.now()))
    
    # Get customer IDs for landing pages
    cursor.execute('SELECT id FROM customers')
    customer_ids = [row[0] for row in cursor.fetchall()]
    
    # Insert sample landing pages
    sample_pages = [
        ('Welcome to Acme Corp', customer_ids[0], 'modern', '''
            <h1>Welcome to Acme Corp</h1>
            <p>Your trusted partner in technology solutions.</p>
            <div class="features">
                <h2>Our Features</h2>
                <ul>
                    <li>24/7 Support</li>
                    <li>Enterprise Solutions</li>
                    <li>Cloud Integration</li>
                </ul>
            </div>
        ''', 'active'),
        ('TechStart - Innovation Hub', customer_ids[1], 'classic', '''
            <h1>TechStart Innovation Hub</h1>
            <p>Empowering the future of technology.</p>
            <div class="services">
                <h2>Our Services</h2>
                <ul>
                    <li>Web Development</li>
                    <li>Mobile Apps</li>
                    <li>Cloud Services</li>
                </ul>
            </div>
        ''', 'active'),
        ('Global Industries Solutions', customer_ids[2], 'minimal', '''
            <h1>Global Industries</h1>
            <p>Leading the way in manufacturing excellence.</p>
            <div class="solutions">
                <h2>Our Solutions</h2>
                <ul>
                    <li>Process Automation</li>
                    <li>Quality Control</li>
                    <li>Supply Chain Management</li>
                </ul>
            </div>
        ''', 'active')
    ]
    
    for page in sample_pages:
        cursor.execute('''
            INSERT INTO landing_pages (title, customer_id, template, content, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (*page, datetime.now()))
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized with sample data!") 