import os
from flask import Flask, render_template, request, jsonify
import database

app = Flask(__name__)

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

if __name__ == '__main__':
    # Run development server
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
# Secret Admin Login Credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "MySecretPassword123" # <--- Ise aap badal sakte hain

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
        <div style="max-width:300px; margin:100px auto; padding:20px; border:1px solid #ccc; text-align:center; font-family:sans-serif;">
            <h2>Admin Login</h2>
            <form method="POST">
                <input type="text" name="username" placeholder="Username" required style="width:100%; margin-bottom:10px; padding:8px;"><br>
                <input type="password" name="password" placeholder="Password" required style="width:100%; margin-bottom:10px; padding:8px;"><br>
                <button type="submit" style="width:100%; padding:10px; background:#ff007f; color:#fff; border:none; cursor:pointer;">Login</button>
            </form>
        </div>
    '''

@app.route('/secret-admin/dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    conn = get_db_connection()
    tools = conn.execute('SELECT * FROM tools').fetchall()
    conn.close()
    
    # Simple Dashboard to see and delete tools
    html = '''
    <div style="padding:20px; font-family:sans-serif; max-width:800px; margin:0 auto;">
        <h2>NexusAI Admin Dashboard</h2>
        <p><a href="/secret-admin/logout" style="color:red;">Logout</a></p>
        <table border="1" cellpadding="10" style="width:100%; border-collapse:collapse;">
            <tr><th>Tool Name</th><th>Category</th><th>Action</th></tr>
    '''
    for tool in tools:
        html += f"<tr><td>{tool['name']}</td><td>{tool['category']}</td><td><a href='/secret-admin/delete/{tool['id']}' style='color:red;'>Delete</a></td></tr>"
    html += '</table></div>'
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
