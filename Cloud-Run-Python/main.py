# main.py
import os
from dotenv import load_dotenv  # Import load_dotenv
load_dotenv()  # Load environment variables from .env file
from flask import Flask, request, jsonify
from db_utils import create_connection_pool, get_all_stories, save_story, delete_story, close_connection_pool
from gemini_api import create_gemini_client, call_gemini
from pdf_utils import generate_pdf
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# mainfrom flask_cors import COR
# ... (rest of the main.py code - database setup, routes, etc.)
# Make sure to use the pool object correctly in your database functions:
# get_all_stories(pool, user_id), delete_story(pool, story_id), etc.
# Also, implement your save_story logic in db_utils.py
# In your app initialization:
pool = create_connection_pool()
if not pool:
    exit(1)
g.pool = pool  # Store the pool in the g object

# Example placeholder implementation for save_story in main.py (you should move this to db_utils.py and implement the actual database logic)
def save_story(user_id, story_name, story_content):
    # TODO: Implement database saving logic here.  This is just a placeholder!
    print(f"Saving story for user {user_id}: {story_name} - Content: {story_content}")
    return True

# ... (rest of main.py code - routes, etc.)

# Routes (APIs)
@app.route('/get_stories', methods=['GET'])
def get_stories():
    user_id = request.args.get('user_id')  # Get user ID from query parameters
    stories = get_all_stories(pool, user_id) # Pass pool to get_all_stories
    if stories is not None:
        return jsonify(stories)
    else:
        return jsonify({"error": "Failed to fetch stories"}), 500 # Return 500 for server error


@app.route('/delete_story', methods=['POST'])
def delete_story_api():
    story_id = request.json.get('story_id')
    success = delete_story(pool, story_id)  # Pass the pool
    return jsonify({"success": success})

@app.route('/create_narrative', methods=['POST'])
def create_narrative_api():
    user_id = request.json.get('user_id')
    story_ids = request.json.get('story_ids')
    # ... (Get stories from DB using story_ids, pass to Gemini, save result to DB) ...
    return jsonify({"status": "success"})  # or error



@app.route('/create_story', methods=['POST'])
def create_story_route():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        initial_prompt = data.get('initial_prompt')

        # Call Gemini API
        story_content = call_gemini(gemini_client, initial_prompt)

        if story_content:
             # Save the story (replace with your actual save logic)
            save_story(user_id, "Story Title", story_content)  # Placeholder - replace with your logic
            return jsonify({"story": story_content}), 200
        else:
            return jsonify({"error": "Failed to generate story."}), 500

    except Exception as e:
        print(f"Error generating story: {e}")
        return jsonify({"error": "An error occurred."}), 500


# ... (other API endpoints)

@app.teardown_appcontext
def shutdown_session(exception=None):
    if 'pool' in g:  # Check if pool exists in g (in case of errors during app startup)
        g.pool.closeall()


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))  # for cloud run