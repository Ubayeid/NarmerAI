import sqlite3
from datetime import datetime

def seed_database():
    conn = sqlite3.connect('crm.db')
    c = conn.cursor()
    
    # Sample customers
    customers = [
        {
            'name': 'TechCorp Solutions',
            'email': 'contact@techcorp.com',
            'company': 'TechCorp Solutions Inc.',
            'phone': '+1 (555) 123-4567',
            'industry': 'Technology',
            'website': 'www.techcorp.com',
            'notes': 'Leading technology solutions provider'
        },
        {
            'name': 'Green Earth Foods',
            'email': 'info@greenearth.com',
            'company': 'Green Earth Foods LLC',
            'phone': '+1 (555) 234-5678',
            'industry': 'Food & Beverage',
            'website': 'www.greenearth.com',
            'notes': 'Organic food products manufacturer'
        },
        {
            'name': 'Global Logistics Co',
            'email': 'support@globallogistics.com',
            'company': 'Global Logistics Corporation',
            'phone': '+1 (555) 345-6789',
            'industry': 'Logistics',
            'website': 'www.globallogistics.com',
            'notes': 'International shipping and logistics'
        }
    ]
    
    # Insert customers
    for customer in customers:
        c.execute('''
            INSERT INTO customers (name, email, company, phone, industry, website, notes, status, last_contact)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            customer['name'],
            customer['email'],
            customer['company'],
            customer['phone'],
            customer['industry'],
            customer['website'],
            customer['notes'],
            'active',
            datetime.now()
        ))
    
    # Sample landing pages
    landing_pages = [
        {
            'customer_id': 1,
            'title': 'Welcome to TechCorp Solutions',
            'content': '''
            <div class="hero-section">
                <div class="container">
                    <h1>Welcome to TechCorp Solutions</h1>
                    <p class="lead">Your Partner in Digital Transformation</p>
                    <a href="#contact" class="btn btn-light btn-lg">Get Started</a>
                </div>
            </div>
            
            <div class="content-section">
                <div class="container">
                    <div class="row">
                        <div class="col-md-4">
                            <div class="feature-card p-4 text-center">
                                <i class="fas fa-laptop-code feature-icon"></i>
                                <h3>Custom Software Development</h3>
                                <p>Tailored solutions for your business needs</p>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="feature-card p-4 text-center">
                                <i class="fas fa-cloud feature-icon"></i>
                                <h3>Cloud Solutions</h3>
                                <p>Scalable and secure cloud infrastructure</p>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="feature-card p-4 text-center">
                                <i class="fas fa-shield-alt feature-icon"></i>
                                <h3>Cybersecurity</h3>
                                <p>Protect your digital assets</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            '''
        },
        {
            'customer_id': 2,
            'title': 'Green Earth Foods - Organic Excellence',
            'content': '''
            <div class="hero-section">
                <div class="container">
                    <h1>Green Earth Foods</h1>
                    <p class="lead">Naturally Delicious, Sustainably Sourced</p>
                    <a href="#products" class="btn btn-light btn-lg">Explore Products</a>
                </div>
            </div>
            
            <div class="content-section">
                <div class="container">
                    <div class="row">
                        <div class="col-md-4">
                            <div class="feature-card p-4 text-center">
                                <i class="fas fa-leaf feature-icon"></i>
                                <h3>100% Organic</h3>
                                <p>Certified organic ingredients</p>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="feature-card p-4 text-center">
                                <i class="fas fa-globe feature-icon"></i>
                                <h3>Sustainable Farming</h3>
                                <p>Eco-friendly practices</p>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="feature-card p-4 text-center">
                                <i class="fas fa-heart feature-icon"></i>
                                <h3>Healthy Living</h3>
                                <p>Nutritious and delicious</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            '''
        },
        {
            'customer_id': 3,
            'title': 'Global Logistics - Worldwide Shipping',
            'content': '''
            <div class="hero-section">
                <div class="container">
                    <h1>Global Logistics Co</h1>
                    <p class="lead">Connecting the World Through Efficient Shipping</p>
                    <a href="#services" class="btn btn-light btn-lg">Our Services</a>
                </div>
            </div>
            
            <div class="content-section">
                <div class="container">
                    <div class="row">
                        <div class="col-md-4">
                            <div class="feature-card p-4 text-center">
                                <i class="fas fa-ship feature-icon"></i>
                                <h3>Ocean Freight</h3>
                                <p>Global shipping solutions</p>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="feature-card p-4 text-center">
                                <i class="fas fa-plane feature-icon"></i>
                                <h3>Air Freight</h3>
                                <p>Fast and reliable air shipping</p>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="feature-card p-4 text-center">
                                <i class="fas fa-truck feature-icon"></i>
                                <h3>Ground Transport</h3>
                                <p>Local and regional delivery</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            '''
        }
    ]
    
    # Insert landing pages
    for page in landing_pages:
        c.execute('''
            INSERT INTO landing_pages (customer_id, title, content)
            VALUES (?, ?, ?)
        ''', (
            page['customer_id'],
            page['title'],
            page['content']
        ))
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    seed_database()
    print("Sample data has been added to the database.") 