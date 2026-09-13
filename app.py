import os
import sys
import sqlite3
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import database

app = Flask(__name__)
app.secret_key = 'super-secret-key-change-this-later'

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "MySecretPassword123"

def seed_ultimate_free_tools():
    try:
        db_path = os.path.join(os.path.dirname(__file__), 'ai_tools.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

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
            ("ChatGPT", "The world's most popular conversational AI by OpenAI", "https://chatgpt.com", 1, "Freemium", "1", 2100),
            ("Claude AI", "State-of-the-art intelligence for analysis and writing by Anthropic", "https://claude.ai", 1, "Freemium", "1", 1850),
            ("DeepSeek R1", "Open-source reasoning model rivaling top proprietary chat layers", "https://deepseek.com", 1, "Free", "1", 1950),
            ("DuckDuckGo AI Chat", "100% Anonymous and secure open-source model chat", "https://duckduckgo.com", 1, "Free", "0", 350),
            ("Gemini AI", "Google's powerful multimodal assistant with massive context limits", "https://google.com", 1, "Freemium", "1", 1720),
            ("Bing Image Creator", "Generate hyper-realistic 3D scenes via DALL-E", "https://bing.com", 2, "Free", "1", 190),
            ("Flux.1", "Next-gen premier open-weights photorealistic image model", "https://github.com", 2, "Free", "1", 1340),
            ("Fooocus", "Local workspace offering Midjourney quality without limits", "https://github.com", 2, "Free", "1", 510),
            ("Midjourney v6", "Industry standard for artistic rendering and conceptual visual style", "https://midjourney.com", 2, "Paid", "1", 1650),
            ("Cursor", "An AI-first code editor tailored for hyper-productive builders", "https://cursor.com", 3, "Freemium", "1", 1421),
            ("Devin AI", "The premier autonomous system capable of complete engineering tasks", "https://cognition.ai", 3, "Paid", "0", 1),
            ("GitHub Copilot", "Autocompletion pair-programmer baked right into common editors", "https://github.com", 3, "Paid", "1", 1280),
            ("v0 by Vercel", "Generative design interface outputting raw React and Tailwind components", "https://v0.dev", 3, "Freemium", "1", 1150),
            ("ElevenLabs", "Ultra-realistic text-to-speech engine and authentic voice replication", "https://elevenlabs.io", 4, "Freemium", "1", 1780),
            ("Suno v3.5", "Synthesize full musical compositions with rich instrumental and vocal tracks", "https://suno.com", 4, "Freemium", "1", 1410),
            ("Perplexity AI", "Real-time query engine providing annotated contextual search webs", "https://perplexity.ai", 5, "Freemium", "1", 1920),
            ("HeyGen", "Production studio generating human-realistic avatar spokespersons", "https://heygen.com", 6, "Freemium", "1", 950),
            ("Runway Gen-3", "Next-gen generation tool offering dynamic panning and simulations", "https://runwayml.com", 6, "Freemium", "1", 1290),
            ("Sora by OpenAI", "Unbelievable text-to-video foundation layer tracking intricate details", "https://openai.com", 6, "Paid", "1", 1510),
            ("Spline AI", "An interactive engine generating functional browser assets via inputs", "https://spline.design", 7, "Freemium", "1", 1260)
        ]

        for t in tools:
            cursor.execute('INSERT OR IGNORE INTO tools (name, tagline, website_url, category_id, pricing, featured, upvotes) VALUES (?, ?, ?, ?, ?, ?, ?)', t)

        conn.commit()
        conn.close()
        print("Global AI Directory seeded successfully! 🎉")
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
    
    tools = database.get_tools()
    html = '''
    <div style="padding:20px; font-family:sans-serif; max-width:800px; margin:0 auto;">
        <h2>NexusAI Admin Dashboard</h2>
        <p><a href="/secret-admin/logout" style="color:red;">Logout</a></p>
        <table border="1" cellpadding="10" style="width:100%; border-collapse:collapse;">
            <tr><th>Tool Name</th><th>Category</th><th>Action</th></tr>
    '''
    for tool in tools:
        html += f"<tr><td>{tool['name']}</td><td>{tool['category_name']}</td><td><a href='/secret-admin/delete/{tool['id']}' style='color:red;'>Delete</a></td></tr>"
    html += '</table></div>'
    return html

@app.route('/secret-admin/delete/<int:id>')
def delete_tool(id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    try:
        db_path = os.path.join(os.path.dirname(__file__), 'ai_tools.db')
        conn = sqlite3.connect(db_path)
        conn.execute('DELETE FROM tools WHERE id = ?', (id,))
        conn.commit()
        conn.close()
    except Exception as e:
        return f"Error deleting tool: {str(e)}"
    return redirect(url_for('admin_dashboard'))

@app.route('/secret-admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
