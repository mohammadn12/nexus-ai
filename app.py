import os
import sqlite3
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import database

app = Flask(__name__)
# Flask session secure rakhne ke liye zaroori key
app.secret_key = 'super-secret-key-change-this-later'

# Global Admin Settings
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "MySecretPassword123"
SITE_NOTIFICATION = "Welcome to NexusAI! Submit your tool today to reach thousands of users."

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
        stats=stats,
        announcement=SITE_NOTIFICATION
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
    return jsonify({'status': 'success', 'count': len(tools), 'tools': tools})

@app.route('/api/tools/<int:tool_id>', methods=['GET'])
def api_get_tool(tool_id):
    tool = database.get_tool_by_id(tool_id)
    if not tool:
        return jsonify({'status': 'error', 'message': 'Tool not found'}), 404
    return jsonify({'status': 'success', 'tool': tool})

@app.route('/api/categories', methods=['GET'])
def api_get_categories():
    categories = database.get_all_categories()
    return jsonify({'status': 'success', 'categories': categories})

@app.route('/api/tools/<int:tool_id>/upvote', methods=['POST'])
def api_upvote_tool(tool_id):
    new_count = database.upvote_tool(tool_id)
    if new_count is None:
        return jsonify({'status': 'error', 'message': 'Tool not found'}), 404
    return jsonify({'status': 'success', 'upvotes': new_count})

@app.route('/api/tools/submit', methods=['POST'])
def api_submit_tool():
    data = request.get_json()
    if not data:
        return jsonify({'status': 'error', 'message': 'Invalid JSON body'}), 400
    try:
        new_tool = database.submit_tool(data)
        return jsonify({'status': 'success', 'message': 'Tool submitted successfully!', 'tool': new_tool}), 201
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def api_get_stats():
    stats = database.get_stats()
    return jsonify({'status': 'success', 'stats': stats})


# --- 🔮 MASTER CONTROL ROOM ROUTES ---

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
    
    global SITE_NOTIFICATION
    
    if request.method == 'POST':
        if 'update_announcement' in request.form:
            SITE_NOTIFICATION = request.form.get('announcement_text', '')
            return redirect(url_for('admin_dashboard'))
            
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

    tools = database.get_tools()
    categories = database.get_all_categories()
    
    total_tools = len(tools)
    featured_count = sum(1 for t in tools if str(t.get('featured')) == '1')
    total_upvotes = sum(int(t.get('upvotes', 0)) for t in tools)
    
    html = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>NexusAI - Super Admin Portal</title>
        <style>
            body {{ font-family: 'Segoe UI', sans-serif; background-color: #0d0e12; color: #e4e6eb; margin: 0; padding: 0; }}
            .navbar {{ background-color: #161820; padding: 15px 30px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #242736; }}
            .navbar h2 {{ margin: 0; color: #ff007f; font-size: 22px; }}
            .logout-btn {{ color: #ff4d4d; text-decoration: none; font-weight: bold; padding: 8px 16px; border: 1px solid #ff4d4d; border-radius: 6px; transition: 0.3s; }}
            .logout-btn:hover {{ background: #ff4d4d; color: #fff; }}
            .analytics-grid {{ max-width: 1200px; margin: 30px auto 0 auto; padding: 0 20px; display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }}
            .stats-card {{ background: linear-gradient(135deg, #1f1a3a, #161820); padding: 20px; border-radius: 12px; border: 1px solid #32255c; text-align: center; }}
            .stats-card p {{ margin: 8px 0 0 0; font-size: 32px; font-weight: bold; color: #fff; }}
            .container {{ max-width: 1200px; margin: 30px auto; padding: 0 20px; display: grid; grid-template-columns: 1fr 2fr; gap: 30px; }}
            .panel-card {{ background-color: #161820; border-radius: 12px; border: 1px solid #242736; padding: 25px; margin-bottom: 20px; }}
            .panel-card h3 {{ margin-top: 0; color: #fff; border-bottom: 1px solid #242736; padding-bottom: 10px; }}
            .search-box {{ width: 95%; padding: 12px; margin-bottom: 20px; background: #0d0e12; border: 1px solid #242736; color: #fff; border-radius: 8px; }}
            .form-group {{ margin-bottom: 15px; }}
            .form-group label {{ display: block; margin-bottom: 5px; font-size: 14px; color: #9aa0a6; }}
            .form-control {{ width: 93%; padding: 10px; background: #0d0e12; border: 1px solid #242736; color: #fff; border-radius: 6px; }}
            .submit-btn {{ width: 100%; padding: 12px; background: #ff007f; color: #fff; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; }}
            table {{ width: 100%; border-collapse: collapse; text-align: left; }}
            th, td {{ padding: 12px 15px; border-bottom: 1px solid #242736; }}
            th {{ background-color: #1f2230; color: #9aa0a6; font-size: 13px; text-transform: uppercase; }}
            tr:hover {{ background-color: #1c1f2e; }}
            .tag {{ background-color: #242736; padding: 4px 10px; border-radius: 20px; font-size: 11px; color: #00ffff; }}
            .action-btn {{ text-decoration: none; padding: 4px 8px; border-radius: 6px; font-size: 12px; transition: 0.2s; margin-left: 2px; display: inline-block; font-weight: bold; }}
            .delete-btn {{ color: #ff4d4d; background: rgba(255, 77, 77, 0.1); }}
            .delete-btn:hover {{ background: #ff4d4d; color: #fff; }}
            .feature-btn {{ color: #ffaa00; background: rgba(255, 170, 0, 0.1); }}
            .feature-btn:hover {{ background: #ffaa00; color: #fff; }}
            .normal-btn {{ color: #00ffaa; background: rgba(0, 255, 170, 0.1); }}
            .normal-btn:hover {{ background: #00ffaa; color: #000; }}
            .boost-btn {{ color: #a066ff; background: rgba(160, 102, 255, 0.1); border: 1px solid #a066ff; }}
            .boost-btn:hover {{ background: #a066ff; color: #fff; }}
            .danger-zone {{ border: 1px dashed #ff4d4d; padding: 15px; border-radius: 8px; background: rgba(255, 77, 77, 0.05); margin-top: 20px; }}
        </style>
        <script>
            function filterTools() {{
                let input = document.getElementById('adminSearch').value.toLowerCase();
                let rows = document.querySelectorAll('.tool-row');
                rows.forEach(row => {{
                    let name = row.getAttribute('data-name').toLowerCase();
                    if(name.includes(input)) {{ row.style.display = ""; }}
                    else {{ row.style.display = "none"; }}
                }});
            }}
