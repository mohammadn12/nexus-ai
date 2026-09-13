
import os
import sys
import sqlite3
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import database

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-prod')

ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'MySecretPassword123')

def seed_ultimate_free_tools():
    try:
        db_path = os.path.join(os.path.dirname(__file__), 'ai_tools.db')
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY, 
                    name TEXT NOT NULL, 
                    slug TEXT NOT NULL UNIQUE
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tools (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    name TEXT NOT NULL, 
                    tagline TEXT NOT NULL, 
                    website_url TEXT NOT NULL, 
                    category_id INTEGER, 
                    pricing TEXT, 
                    featured TEXT, 
                    upvotes INTEGER DEFAULT 0, 
                    FOREIGN KEY (category_id) REFERENCES categories (id)
                )
            ''')

            categories = [
                (1, "Text & Writing", "text-writing"),
                (2, "Image & Art", "image-art"),
                (3, "Coding & Dev", "coding-dev"),
                (4, "Audio & Voice", "audio-voice"),
                (5, "Productivity & Research", "productivity-research"),
                (6, "Video & Motion", "video-motion"),
                (7, "3D & Design", "3d-design")
            ]
            for cat in categories:
                cursor.execute('INSERT OR IGNORE INTO categories (id, name, slug) VALUES (?, ?, ?)', cat)

            tools = [
                ("ChatGPT", "Conversational AI by OpenAI", "https://chatgpt.com", 1, "Freemium", "1", 2100),
                ("Claude AI", "Intelligence by Anthropic", "https://claude.ai", 1, "Freemium", "1", 1850),
                ("DeepSeek R1", "Open-source reasoning model", "https://deepseek.com", 1, "Free", "1", 1950),
                ("Gemini AI", "Multimodal assistant by Google", "https://google.com", 1, "Freemium", "1", 1720),
                ("Midjourney v6", "Industry standard for artistic rendering", "https://midjourney.com", 2, "Paid", "1", 1650),
                ("Cursor", "AI-first code editor for engineers", "https://cursor.com", 3, "Freemium", "1", 1421),
                ("ElevenLabs", "Ultra-realistic text-to-speech engine", "https://elevenlabs.io", 4, "Freemium", "1", 1780),
                ("Perplexity AI", "AI-powered conversational search engine", "https://perplexity.ai", 5, "Freemium", "1", 1920)
            ]

            for t in tools:
                cursor.execute('INSERT OR IGNORE INTO tools (name, tagline, website_url, category_id, pricing, featured, upvotes) VALUES (?, ?, ?, ?, ?, ?, ?)', t)

    except Exception as e:
        print(f"Seeding failed: {e}")

with app.app_context():
    database.init_db()
    seed_ultimate_free_tools()

@app.route('/')
def index():
    categories = database.get_all_categories()
    featured_tools = database.get_tools(featured="1", sort_by="popular")
    all_tools = database.get_tools(sort_by="popular")
    stats = database.get_stats()
    return render_template('index.html', categories=categories, featured_tools=featured_tools, tools=all_tools, stats=stats)

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
    return jsonify({'status': 'success', 'categories': database.get_all_categories()})

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
    
    required_fields = ['name', 'tagline', 'website_url', 'category_id']
    for field in required_fields:
        if not data.get(field): 
            return jsonify({'status': 'error', 'message': f'Field "{field}" is required'}), 400
            
    try:
        new_tool = database.submit_tool(data)
        return jsonify({'status': 'success', 'message': 'Tool submitted successfully!', 'tool': new_tool}), 201
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def api_get_stats():
    return jsonify({'status': 'success', 'stats': database.get_stats()})

@app.route('/secret-admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        return "Invalid Credentials! Please try again.", 401
    return render_template('admin_login.html')  # Or keep your HTML template separate

@app.route('/secret-admin/dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'): 
        return redirect(url_for('admin_login'))
    tools = database.get_tools()
    return render_template('admin_dashboard.html', tools=tools)

@app.route('/secret-admin/delete/<int:id>')
def delete_tool(id):
    if not session.get('admin_logged_in'): 
        return redirect(url_for('admin_login'))
    try:
        db_path = os.path.join(os.path.dirname(__file__), 'ai_tools.db')
        with sqlite3.connect(db_path) as conn:
            conn.execute('DELETE FROM tools WHERE id = ?', (id,))
    except Exception as e: 
        return f"Error deleting tool: {str(e)}", 500
    return redirect(url_for('admin_dashboard'))

@app.route('/secret-admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
