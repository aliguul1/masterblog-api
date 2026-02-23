from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Hardcoded data structure
POSTS = [
    {"id": 1, "title": "Apple post", "content": "Zebra content."},
    {"id": 2, "title": "Zebra post", "content": "Apple content."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """
    Step 6: Enhanced list endpoint with optional sorting.
    Supports sort (title, content) and direction (asc, desc).
    """
    sort_field = request.args.get('sort')
    direction = request.args.get('direction', 'asc').lower()

    # Validation requirements
    valid_sort_fields = ['title', 'content']
    valid_directions = ['asc', 'desc']

    # Error Handling: Validate sort field if provided
    if sort_field and sort_field not in valid_sort_fields:
        return jsonify({"error": f"Invalid sort field: {sort_field}"}), 400

    # Error Handling: Validate direction
    if direction not in valid_directions:
        return jsonify({"error": f"Invalid direction: {direction}"}), 400

    # Create a copy to avoid mutating global data
    result_posts = list(POSTS)

    # Apply sorting logic only if sort_field is present
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
    """Step 5: Search posts by title and/or content."""
    title_query = request.args.get('title', '').lower()
    content_query = request.args.get('content', '').lower()

    filtered_posts = []

    for post in POSTS:
        title_match = (title_query in post['title'].lower()
                       if title_query else True)
        content_match = (content_query in post['content'].lower()
                         if content_query else True)

        if title_match and content_match:
            filtered_posts.append(post)

    return jsonify(filtered_posts), 200


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


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """Step 4: Update an existing post."""
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
    """Deletes a post by its unique ID."""
    global POSTS

    post = next((p for p in POSTS if p['id'] == post_id), None)

    if post is None:
        return jsonify({"error": f"Post with id {post_id} was not found."}), 404

    POSTS = [p for p in POSTS if p['id'] != post_id]

    return jsonify({
        "message": f"Post with id {post_id} has been deleted successfully."
    }), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)