from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


@app.route('/api/posts', methods=['POST'])
def add_post():
    data = request.get_json()

    # 1. Check if data exists at all
    if not data:
        return jsonify({"error": "Invalid JSON or empty body"}), 400

    # 2. Check for missing keys AND empty content
    missing_fields = []

    # Check Title
    if 'title' not in data or not str(data.get('title')).strip():
        missing_fields.append('title')

    # Check Content
    if 'content' not in data or not str(data.get('content')).strip():
        missing_fields.append('content')

    if missing_fields:
        return jsonify({"error": f"Missing or empty fields: {', '.join(missing_fields)}"}), 400

    # 3. ID Generation
    new_id = max(post['id'] for post in POSTS) + 1 if POSTS else 1

    # 4. Create and Append
    new_post = {
        "id": new_id,
        "title": data['title'],
        "content": data['content']
    }

    POSTS.append(new_post)
    return jsonify(new_post), 201


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)