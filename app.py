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
                    name TEXT NOT NULL UNIQUE, 
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
                # 1. Text & Writing (12 Tools)
                ("ChatGPT", "Conversational AI by OpenAI", "https://chatgpt.com", 1, "Freemium", "1", 2100),
                ("Claude AI", "Advanced AI Assistant by Anthropic", "https://claude.ai", 1, "Freemium", "1", 1850),
                ("DeepSeek R1", "Open-source reasoning AI model", "https://deepseek.com", 1, "Free", "1", 1950),
                ("Gemini AI", "Multimodal assistant by Google", "https://gemini.google.com", 1, "Freemium", "1", 1720),
                ("Jasper AI", "AI copywriting assistant for teams", "https://jasper.ai", 1, "Paid", "0", 850),
                ("Copy.ai", "AI content generator for marketing", "https://copy.ai", 1, "Freemium", "0", 920),
                ("Writesonic", "AI writer for SEO blogs and ads", "https://writesonic.com", 1, "Freemium", "0", 780),
                ("QuillBot", "AI paraphrasing and grammar tool", "https://quillbot.com", 1, "Freemium", "0", 1450),
                ("Grammarly", "AI writing assistant and proofreader", "https://grammarly.com", 1, "Freemium", "0", 1600),
                ("Rytr", "Best AI writer & email generator", "https://rytr.me", 1, "Freemium", "0", 640),
                ("Sudowrite", "AI partner for fiction & story writers", "https://sudowrite.com", 1, "Paid", "0", 520),
                ("Notion AI", "Connected workspace AI assistant", "https://notion.so", 1, "Paid", "0", 1100),

                # 2. Image & Art (12 Tools)
                ("Midjourney v6", "Industry standard for photorealistic art", "https://midjourney.com", 2, "Paid", "1", 1650),
                ("DALL-E 3", "Image generator powered by OpenAI", "https://openai.com/dall-e-3", 2, "Paid", "1", 1500),
                ("Leonardo.ai", "Generative AI for creative art and game assets", "https://leonardo.ai", 2, "Freemium", "1", 1400),
                ("Stable Diffusion", "Open-source text-to-image AI", "https://stability.ai", 2, "Free", "0", 1320),
                ("Adobe Firefly", "Creative generative AI for designers", "https://firefly.adobe.com", 2, "Freemium", "0", 1250),
                ("Canva Magic Studio", "AI suite for quick graphic design", "https://canva.com", 2, "Freemium", "0", 1800),
                ("Freepik Pikaso", "Real-time AI sketch to image generator", "https://freepik.com/pikaso", 2, "Freemium", "0", 720),
                ("Lexica Art", "Search engine & prompt generator for art", "https://lexica.art", 2, "Freemium", "0", 890),
                ("Ideogram", "AI image generator with perfect text typography", "https://ideogram.ai", 2, "Freemium", "1", 1150),
                ("Clipdrop", "AI powered ecosystem for image editing", "https://clipdrop.co", 2, "Freemium", "0", 610),
                ("Magnific AI", "AI upscaler & image enhancer", "https://magnific.ai", 2, "Paid", "0", 940),
                ("Remove.bg", "Automated background remover for photos", "https://remove.bg", 2, "Freemium", "0", 1550),

                # 3. Coding & Dev (11 Tools)
                ("Cursor", "AI-first code editor for developers", "https://cursor.com", 3, "Freemium", "1", 1421),
                ("GitHub Copilot", "Your AI pair programmer", "https://github.com/features/copilot", 3, "Paid", "1", 1890),
                ("Replit Ghostwriter", "In-browser AI coding assistant", "https://replit.com", 3, "Freemium", "0", 980),
                ("Tabnine", "AI code completion for development teams", "https://tabnine.com", 3, "Freemium", "0", 820),
                ("v0 by Vercel", "Generative UI system powered by AI", "https://v0.dev", 3, "Freemium", "1", 1350),
                ("Codeium", "Free AI code autocomplete and chat", "https://codeium.com", 3, "Free", "0", 1100),
                ("Sourcegraph Cody", "AI assistant for reading & writing codebase", "https://sourcegraph.com/cody", 3, "Freemium", "0", 670),
                ("Phind", "AI search engine for software engineers", "https://phind.com", 3, "Free", "0", 910),
                ("Supermaven", "Ultra-fast AI code editor plugin", "https://supermaven.com", 3, "Freemium", "0", 540),
                ("Blackbox AI", "AI powered code search and autocomplete", "https://blackbox.ai", 3, "Freemium", "0", 760),
                ("Warp Terminal", "AI terminal built for modern teams", "https://warp.dev", 3, "Freemium", "0", 830),

                # 4. Audio & Voice (10 Tools)
                ("ElevenLabs", "Ultra-realistic text-to-speech engine", "https://elevenlabs.io", 4, "Freemium", "1", 1780),
                ("Suno AI", "Generate full song audio with lyrics & music", "https://suno.com", 4, "Freemium", "1", 1620),
                ("Udio", "High quality AI music creation studio", "https://udio.com", 4, "Freemium", "1", 1490),
                ("Adobe Podcast", "AI voice enhancement & noise remover", "https://podcast.adobe.com", 4, "Free", "0", 1310),
                ("Murf.ai", "Versatile AI voice generator for videos", "https://murf.ai", 4, "Freemium", "0", 720),
                ("Lovo.ai", "AI voiceover generator for video creation", "https://lovo.ai", 4, "Freemium", "0", 590),
                ("Descript", "Audio & video editing like a text document", "https://descript.com", 4, "Freemium", "0", 1120),
                ("Voice AI", "Real-time AI voice changer", "https://voice.ai", 4, "Free", "0", 870),
                ("Play.ht", "Realistic AI voice clones & generator", "https://play.ht", 4, "Freemium", "0", 650),
                ("Speranker", "AI audio cleaner and mastering", "https://audo.ai", 4, "Freemium", "0", 410),

                # 5. Productivity & Research (11 Tools)
                ("Perplexity AI", "Conversational AI search engine", "https://perplexity.ai", 5, "Freemium", "1", 1920),
                ("Glean", "Enterprise search and intelligence AI", "https://glean.com", 5, "Paid", "0", 430),
                ("Otter.ai", "AI meeting notes & transcription assistant", "https://otter.ai", 5, "Freemium", "0", 1250),
                ("Consensus", "AI research search engine for scientific papers", "https://consensus.app", 5, "Freemium", "0", 870),
                ("Elicit", "AI research assistant for paper analysis", "https://elicit.com", 5, "Freemium", "0", 790),
                ("Gamma App", "Generate presentations and docs with AI", "https://gamma.app", 5, "Freemium", "1", 1680),
                ("Tome", "AI storytelling and deck builder", "https://tome.app", 5, "Freemium", "0", 950),
                ("Miro AI", "Mindmapping and visual brainstorming with AI", "https://miro.com", 5, "Freemium", "0", 810),
                ("Humata AI", "Chat with any PDF research document", "https://humata.ai", 5, "Freemium", "0", 740),
                ("ChatPDF", "Analyze and summarize PDF files easily", "https://chatpdf.com", 5, "Freemium", "0", 1150),
                ("Fireflies.ai", "Automated meeting assistant and note taker", "https://fireflies.ai", 5, "Freemium", "0", 910),

                # 6. Video & Motion (10 Tools)
                ("Runway Gen-2", "Text-to-video & image-to-video generation", "https://runwayml.com", 6, "Freemium", "1", 1540),
                ("Pika Labs", "Idea-to-video creative AI platform", "https://pika.art", 6, "Freemium", "1", 1380),
                ("Sora", "OpenAI text-to-video model", "https://openai.com/sora", 6, "Paid", "1", 1980),
                ("Luma Dream Machine", "High quality cinematic video generator", "https://lumalabs.ai/dream-machine", 6, "Freemium", "1", 1290),
                ("HeyGen", "Create realistic AI avatar videos", "https://heygen.com", 6, "Freemium", "1", 1410),
                ("Synthesia", "AI video generator from plain text", "https://synthesia.io", 6, "Paid", "0", 980),
                ("Opus Clip", "Turn long videos into viral shorts using AI", "https://opus.pro", 6, "Freemium", "0", 1120),
                ("CapCut AI", "Smart video editor with automated captions", "https://capcut.com", 6, "Freemium", "0", 1750),
                ("Kling AI", "High resolution video creation model", "https://klingai.com", 6, "Freemium", "0", 860),
                ("Veed.io", "Online video editor with text-to-speech & captions", "https://veed.io", 6, "Freemium", "0", 890),

                # 7. 3D & Design (9 Tools)
                ("Spline AI", "3D design and scene generator with AI prompts", "https://spline.design", 7, "Freemium", "1", 1120),
                ("Meshy", "Text and image to 3D model generator", "https://meshy.ai", 7, "Freemium", "0", 780),
                ("Luma AI Interactive NeRF", "3D capture and NeRF creation tool", "https://lumalabs.ai", 7, "Free", "0", 890),
                ("Tripo3D", "Generate 3D assets in seconds using AI", "https://tripo3d.ai", 7, "Freemium", "0", 640),
                ("Relume", "AI website sitemap & wireframe builder", "https://relume.io", 7, "Freemium", "0", 1020),
                ("Figma AI", "Design assistant directly in Figma", "https://figma.com", 7, "Freemium", "1", 1590),
                ("Uizard", "Design UI wireframes from text prompts", "https://uizard.io", 7, "Freemium", "0", 830),
                ("Kaedim", "Transform 2D images into 3D models", "https://kaedim3d.com", 7, "Paid", "0", 520),
                ("CSM (Common Sense Machines)", "Create 3D digital twins with AI", "https://csm.ai", 7, "Freemium", "0", 470)
            ]

            for t in tools:
                cursor.execute('''
                    INSERT OR REPLACE INTO tools (name, tagline, website_url, category_id, pricing, featured, upvotes)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', t)

            conn.commit()
            print("75 AI Tools successfully seeded!")

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
    return render_template('admin_login.html')

@app.route('/secret-admin/dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'): 
        return redirect(url_for('admin_login'))
    tools = database.get_tools()
    return render_template('admin_dashboard.html', tools=tools)

@app.route('/secret-admin/delete/<int:id>', methods=['POST'])
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
