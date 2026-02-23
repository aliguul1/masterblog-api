from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Hardcoded data structure
POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """Returns the current list of blog posts."""
    return jsonify(POSTS)


@app.route('/api/posts', methods=['POST'])
def add_post():
    """Validates and adds a new blog post."""
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid JSON or empty body"}), 400

    missing_fields = []
    if 'title' not in data or not str(data.get('title')).strip():
        missing_fields.append('title')
    if 'content' not in data or not str(data.get('content')).strip():
        missing_fields.append('content')

    if missing_fields:
        return jsonify({
            "error": f"Missing or empty fields: {', '.join(missing_fields)}"
        }), 400

    new_id = max(post['id'] for post in POSTS) + 1 if POSTS else 1
    new_post = {
        "id": new_id,
        "title": data['title'],
        "content": data['content']
    }
    POSTS.append(new_post)
    return jsonify(new_post), 201


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """
    Deletes a post by its unique ID.
    Returns 404 if the ID does not exist.
    """
    global POSTS

    # Locate the post to confirm existence
    post = next((p for p in POSTS if p['id'] == post_id), None)

    if post is None:
        # Fulfills Step 3: Error Handling requirement
        return jsonify({"error": f"Post with id {post_id} was not found."}), 404

    # Generic file/list handling: filter out the post with the matching ID
    POSTS = [p for p in POSTS if p['id'] != post_id]

    return jsonify({
        "message": f"Post with id {post_id} has been deleted successfully."
    }), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)