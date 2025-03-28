from flask import Flask, render_template_string

app = Flask(__name__)

# Simple HTML template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Simple CRM</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <h1>Welcome to Simple CRM</h1>
        <p>This is a test page to verify Flask is working correctly.</p>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    print("Starting the simple application...")
    app.run(debug=True) 