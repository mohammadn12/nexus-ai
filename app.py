import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import database

app = Flask(__name__)
# Flask session secure rakhne ke liye zaroori key
app.secret_key = 'super-secret-key-change-this-later'

# Secret Admin Login Credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "MySecretPassword123"

# Initialize database schema and seed data
with app.app_context():
    database.init_db()

@app.route('/')
def index():
    categories = database.get_all_categories()
    featured_tools = database.get_tools(featured="1", sort_by="popular")
    all_tools = database.get_tools(sort_by="popular")
    stats = database.get_stats()
    return render_template(
        'index.html',
        categories=categories,
        featured_tools=featured_tools,
        tools=all_tools,
        stats=stats
    )

@app.route('/api/tools', methods=['GET'])
def api_get_tools():
    q = request.args.get('q', '').strip()
    category = request.args.get('category', 'all').strip()
    pricing = request.args.get('pricing', 'all').strip()
    featured = request.args.get('featured')
    sort_by = request.args.get('sort', 'popular').strip()

    tools = database.get_tools(
        query=q if q else None,
        category_slug=category if category != 'all' else None,
        pricing=pricing if pricing != 'all' else None,
        featured=featured,
        sort_by=sort_by
    )
    return jsonify({
        'status': 'success',
        'count': len(tools),
        'tools': tools
    })

@app.route('/api/tools/<int:tool_id>', methods=['GET'])
def api_get_tool(tool_id):
    tool = database.get_tool_by_id(tool_id)
    if not tool:
        return jsonify({'status': 'error', 'message': 'Tool not found'}), 404
    return jsonify({
        'status': 'success',
        'tool': tool
    })

@app.route('/api/categories', methods=['GET'])
def api_get_categories():
    categories = database.get_all_categories()
    return jsonify({
        'status': 'success',
        'categories': categories
    })

@app.route('/api/tools/<int:tool_id>/upvote', methods=['POST'])
def api_upvote_tool(tool_id):
    new_count = database.upvote_tool(tool_id)
    if new_count is None:
        return jsonify({'status': 'error', 'message': 'Tool not found'}), 404
    return jsonify({
        'status': 'success',
        'upvotes': new_count
    })

@app.route('/api/tools/submit', methods=['POST'])
def api_submit_tool():
    data = request.get_json()
    if not data:
        return jsonify({'status': 'error', 'message': 'Invalid JSON body'}), 400

    required_fields = ['name', 'tagline', 'website_url', 'category_id']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'status': 'error', 'message': f'Field "{field}" is required'}), 420

    try:
        new_tool = database.submit_tool(data)
        return jsonify({
            'status': 'success',
            'message': 'Tool submitted successfully!',
            'tool': new_tool
        }), 201
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def api_get_stats():
    stats = database.get_stats()
    return jsonify({
        'status': 'success',
        'stats': stats
    })

# --- 🔮 100% CRASH-FREE PREMIUM ADMIN SUITE ---

@app.route('/secret-admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
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
    
    # Form submission handler using native database submit function
    if request.method == 'POST':
        form_data = {
            'name': request.form.get('name'),
            'tagline': request.form.get('tagline'),
            'website_url': request.form.get('website_url'),
            'category_id': int(request.form.get('category_id')),
            'pricing': request.form.get('pricing', 'Free'),
            'featured': request.form.get('featured', '0'),
            'description': request.form.get('description', '')
        }
        try:
            database.submit_tool(form_data)
        except Exception as e:
            return f"Error adding tool: {str(e)}"
        return redirect(url_for('admin_dashboard'))

    # Native connection mapping to avoid lock threads
    tools = database.get_tools()
    categories = database.get_all_categories()
    total_tools = len(tools)
    
    html = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>NexusAI - Premium Control Room</title>
        <style>
            body {{ font-family: 'Segoe UI', sans-serif; background-color: #0d0e12; color: #e4e6eb; margin: 0; padding: 0; }}
            .navbar {{ background-color: #161820; padding: 15px 30px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #242736; }}
            .navbar h2 {{ margin: 0; color: #ff007f; font-size: 22px; }}
            .logout-btn {{ color: #ff4d4d; text-decoration: none; font-weight: bold; padding: 8px 16px; border: 1px solid #ff4d4d; border-radius: 6px; transition: 0.3s; }}
            .logout-btn:hover {{ background: #ff4d4d; color: #fff; }}
            .container {{ max-width: 1100px; margin: 40px auto; padding: 0 20px; display: grid; grid-template-columns: 1fr 2fr; gap: 30px; }}
            .panel-card {{ background-color: #161820; border-radius: 12px; border: 1px solid #242736; padding: 25px; }}
            .panel-card h3 {{ margin-top: 0; color: #fff; border-bottom: 1px solid #242736; padding-bottom: 10px; }}
            .stats-card {{ background: linear-gradient(135deg, #1f1a3a, #161820); padding: 15px; border-radius: 10px; border: 1px solid #32255c; margin-bottom: 20px; text-align: center; }}
            .stats-card p {{ margin: 5px 0 0 0; font-size: 36px; font-weight: bold; color: #00ffff; }}
            .form-group {{ margin-bottom: 15px; }}
            .form-group label {{ display: block; margin-bottom: 5px; font-size: 14px; color: #9aa0a6; }}
            .form-control {{ width: 93%; padding: 10px; background: #0d0e12; border: 1px solid #242736; color: #fff; border-radius: 6px; }}
            .submit-btn {{ width: 100%; padding: 12px; background: #ff007f; color: #fff; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; }}
            table {{ width: 100%; border-collapse: collapse; text-align: left; }}
            th, td {{ padding: 12px 15px; border-bottom: 1px solid #242736; }}
            th {{ background-color: #1f2230; color: #9aa0a6; font-size: 13px; text-transform: uppercase; }}
            tr:hover {{ background-color: #1c1f2e; }}
            .tag {{ background-color: #242736; padding: 4px 10px; border-radius: 20px; font-size: 11px; color: #00ffff; }}
            .delete-btn {{ color: #ff4d4d; text-decoration: none; background: rgba(255, 77, 77, 0.1); padding: 5px 10px; border-radius: 6px; font-size: 13px; transition: 0.2s; }}
            .delete-btn:hover {{ background: #ff4d4d; color: #fff; }}
        </style>
    </head>
    <body>
        <div class="navbar">
            <h2>🔮 NexusAI Premium Admin</h2>
            <div>
                <a href="/" target="_blank" style="color:#00ffff; text-decoration:none; margin-right:20px; font-weight:bold;">View Website 🌐</a>
                <a href="/secret-admin/logout" class="logout-btn">Logout</a>
            </div>
        </div>
        <div class="container">
            <div>
                <div class="stats-card">
                    <span style="color:#9aa0a6; font-size:13px; text-transform:uppercase;">Total Listed Tools</span>
                    <p>{total_tools}</p>
                </div>
                <div class="panel-card">
                    <h3>➕ Add New AI Tool</h3>
                    <form method="POST">
                        <div class="form-group">
                            <label>Tool Name</label>
                            <input type="text" name="name" class="form-control" placeholder="e.g. Midjourney" required>
                        </div>
                        <div class="form-group">
                            <label>Tagline</label>
                            <input type="text" name="tagline" class="form-control" placeholder="Short tagline" required>
                        </div>
                        <div class="form-group">
                            <label>Website URL</label>
