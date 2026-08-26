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
