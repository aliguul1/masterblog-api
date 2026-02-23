import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

# --- FIX: Define absolute path for the static folder ---
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, static_folder=os.path.join(BASE_DIR, 'static'))
CORS(app)

# --- Step Two: Configure Swagger ---
SWAGGER_URL = "/api/docs"
API_URL = "/static/masterblog.json"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': 'Masterblog API'}
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

# Hardcoded data structure
POSTS = [
    {"id": 1, "title": "Apple post", "content": "Zebra content."},
    {"id": 2, "title": "Zebra post", "content": "Apple content."},
]

@app.route('/api/posts', methods=['GET'])
def get_posts():
    sort_field = request.args.get('sort')
    direction = request.args.get('direction', 'asc').lower()
    valid_sort_fields = ['title', 'content']
    valid_directions = ['asc', 'desc']

    if sort_field and sort_field not in valid_sort_fields:
        return jsonify({"error": f"Invalid sort field: {sort_field}"}), 400
    if direction not in valid_directions:
        return jsonify({"error": f"Invalid direction: {direction}"}), 400

    result_posts = list(POSTS)
    if sort_field:
        reverse_order = (direction == 'desc')
        result_posts = sorted(
            result_posts,
            key=lambda x: x[sort_field].lower(),
            reverse=reverse_order
        )
    return jsonify(result_posts), 200

@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    title_query = request.args.get('title', '').lower()
    content_query = request.args.get('content', '').lower()
    filtered_posts = []
    for post in POSTS:
        title_match = (title_query in post['title'].lower() if title_query else True)
        content_match = (content_query in post['content'].lower() if content_query else True)
        if title_match and content_match:
            filtered_posts.append(post)
    return jsonify(filtered_posts), 200

@app.route('/api/posts', methods=['POST'])
def add_post():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON or empty body"}), 400
    missing_fields = []
    if 'title' not in data or not str(data.get('title')).strip():
        missing_fields.append('title')
    if 'content' not in data or not str(data.get('content')).strip():
        missing_fields.append('content')
    if missing_fields:
        return jsonify({"error": f"Missing or empty fields: {', '.join(missing_fields)}"}), 400

    new_id = max(post['id'] for post in POSTS) + 1 if POSTS else 1
    new_post = {"id": new_id, "title": data['title'], "content": data['content']}
    POSTS.append(new_post)
    return jsonify(new_post), 201

@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    post = next((p for p in POSTS if p['id'] == post_id), None)
    if post is None:
        return jsonify({"message": f"Post with id {post_id} was not found."}), 404
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    post['title'] = data.get('title', post['title'])
    post['content'] = data.get('content', post['content'])
    return jsonify(post), 200

@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    global POSTS
    post = next((p for p in POSTS if p['id'] == post_id), None)
    if post is None:
        return jsonify({"error": f"Post with id {post_id} was not found."}), 404
    POSTS = [p for p in POSTS if p['id'] != post_id]
    return jsonify({"message": f"Post with id {post_id} has been deleted successfully."}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)