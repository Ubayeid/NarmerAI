# Narmer - Landing Page Manager

Narmer is a modern web application for managing customers and their landing pages. It provides a user-friendly interface for creating, editing, and managing landing pages for different customers.

## Features

- Customer Management
  - Add, edit, and delete customers
  - Track customer details including company, industry, and contact information
  - View customer history and activity

- Landing Page Management
  - Create custom landing pages for each customer
  - Multiple template options (Modern, Classic, Minimal)
  - Preview functionality
  - Status tracking (Draft, Active, Inactive)

- Dashboard
  - Overview of total customers and landing pages
  - Recent activity tracking
  - Quick access to important features

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/narmer.git
cd narmer
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
python init_db.py
```

5. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Project Structure

```
narmer/
├── app.py              # Main application file
├── init_db.py          # Database initialization script
├── requirements.txt    # Project dependencies
├── narmer.db          # SQLite database file
└── templates/         # HTML templates
    ├── base.html      # Base template
    ├── index.html     # Dashboard
    ├── customers.html # Customer list
    ├── add_customer.html
    ├── edit_customer.html
    ├── landing_pages.html
    ├── add_landing_page.html
    ├── edit_landing_page.html
    └── preview_landing_page.html
```

## Usage

1. **Dashboard**
   - View overall statistics
   - Access recent customers and landing pages
   - Quick actions for common tasks

2. **Customers**
   - View all customers
   - Add new customers
   - Edit customer details
   - Delete customers

3. **Landing Pages**
   - View all landing pages
   - Create new landing pages
   - Edit existing pages
   - Preview pages
   - Delete pages

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 