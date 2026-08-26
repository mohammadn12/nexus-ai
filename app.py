import os
import sqlite3
from flask import Flask, render_template, request, jsonify, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'super-secret-key-change-this-later'

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "MySecretPassword123"

def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), 'ai_tools.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    try:
        conn = get_db_connection()
        tools = conn.execute('SELECT * FROM tools').fetchall()
        categories = conn.execute('SELECT * FROM categories').fetchall()
        conn.close()
    except Exception:
        tools, categories = [], []
    return render_template('index.html', tools=tools, categories=categories)

@app.route('/secret-admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if request.form.get('username') == ADMIN_USERNAME and request.form.get('password') == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        return "Galt Password! Dobara koshish karein."
    return '''
        <div style="max-width:300px; margin:100px auto; padding:30px; border:1px solid #242736; background:#161820; text-align:center; font-family:sans-serif; border-radius:12px; color:#fff;">
            <h2 style="color:#ff007f;">Admin Login</h2>
            <form method="POST">
                <input type="text" name="username" placeholder="Username" required style="width:90%; margin-bottom:15px; padding:10px; background:#0d0e12; border:1px solid #242736; color:#fff; border-radius:6px;"><br>
                <input type="password" name="password" placeholder="Password" required style="width:90%; margin-bottom:15px; padding:10px; background:#0d0e12; border:1px solid #242736; color:#fff; border-radius:6px;"><br>
                <button type="submit" style="width:97%; padding:10px; background:#ff007f; color:#fff; border:none; border-radius:6px; font-weight:bold; cursor:pointer;">Sign In</button>
            </form>
        </div>
    '''

@app.route('/secret-admin/dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    conn = get_db_connection()
    
    if request.method == 'POST':
        name = request.form.get('name')
        tagline = request.form.get('tagline')
        url = request.form.get('website_url')
        pricing = request.form.get('pricing', 'Free')
        
        conn.execute('INSERT INTO tools (name, tagline, website_url, pricing) VALUES (?, ?, ?, ?)', 
                     (name, tagline, url, pricing))
        conn.commit()
        return redirect(url_for('admin_dashboard'))

    tools = conn.execute('SELECT * FROM tools').fetchall()
    conn.close()
    
    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>NexusAI Admin</title>
        <style>
            body {{ font-family: sans-serif; background: #0d0e12; color: #fff; padding: 20px; }}
            .container {{ max-width: 800px; margin: 0 auto; }}
            input, select {{ width: 100%; padding: 10px; margin-bottom: 10px; background: #161820; border: 1px solid #242736; color: #fff; border-radius: 6px; }}
            button {{ background: #ff007f; color: #fff; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th, td {{ padding: 12px; border-bottom: 1px solid #242736; text-align: left; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>🔮 NexusAI Premium Admin Panel</h2>
            <form method="POST" style="background: #161820; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
                <h3>➕ Add New Tool</h3>
                <input type="text" name="name" placeholder="Tool Name" required>
                <input type="text" name="tagline" placeholder="Tagline" required>
                <input type="url" name="website_url" placeholder="Website URL" required>
                <select name="pricing">
                    <option value="Free">Free</option>
                    <option value="Freemium">Freemium</option>
                    <option value="Paid">Paid</option>
                </select>
                <button type="submit">Add Tool Live</button>
            </form>
            
            <h3>📋 Live Tools List</h3>
            <table>
                <tr><th>Name</th><th>Pricing</th><th>Action</th></tr>
    '''
    for tool in tools:
        html += f'''
                <tr>
                    <td>{tool['name']}</td>
                    <td>{tool['pricing']}</td>
                    <td><a href="/secret-admin/delete/{tool['id']}" style="color: #ff4d4d; text-decoration: none;">Delete</a></td>
                </tr>
        '''
    html += '</table></div></body></html>'
    return html

@app.route('/secret-admin/delete/<int:id>')
def delete_tool(id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    conn = get_db_connection()
    conn.execute('DELETE FROM tools WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_dashboard'))

@app.route('/secret-admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
