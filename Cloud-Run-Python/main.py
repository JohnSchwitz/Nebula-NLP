# main.py
import os
import uuid
import logging
from flask import Flask, request, jsonify
import psycopg2
from google.api_core import client_options
from google.cloud import discoveryengine_v1beta

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get environment variables (replace with your actual variable names)
PROJECT_ID = os.environ.get("PROJECT_ID")
# DATASTORE_ID = os.environ.get("DATASTORE_ID")  # Or DATA_STORE_ID as per Gemini docs
# CONVERSATION_ID = os.environ.get("CONVERSATION_ID")  # Manage conversations appropriately.
DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")


# Initialize Gemini client
gemini_client = discoveryengine_v1beta.ConversationalSearchServiceClient(
    client_options=client_options.ClientOptions(
        api_endpoint="us-central1-discoveryengine.googleapis.com"  # Update if necessary
    )
)




def get_db_connection():
    try:
        return psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    except psycopg2.Error as e:
        logger.error(f"Database connection error: {e}")
        return None


def get_stories():
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM stories") #Change this query as per your table schema
            stories = cur.fetchall()
            cur.close()
            return stories
        except psycopg2.Error as e:
            logger.error(f"Error retrieving stories: {e}")
        finally:
            conn.close()
    return None  # Or [] if you prefer an empty list on error


def create_story(story_title, story_content, user_id):  # Add other fields as needed
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO stories (story_title, story_content, user_id) VALUES (%s, %s, %s) RETURNING story_id",
                (story_title, story_content, user_id)
            )
            conn.commit()
            new_story_id = cur.fetchone()[0]
            cur.close()
            return new_story_id
        except psycopg2.Error as e:
            logger.error(f"Error creating story: {e}")
            conn.rollback()  # Rollback on error
        finally:
            conn.close()
    return None


@app.route('/api/getStories', methods=['GET'])
def api_get_stories():
    stories = get_stories()
    if stories:
        # ... format data as needed for JSON response
        return jsonify(stories), 200
    else:
        return jsonify({"error": "Failed to retrieve stories"}), 500

@app.route('/api/startStoryCreation', methods=['POST'])  # New endpoint to initiate story creation
def api_start_story_creation():
    new_conversation_id = str(uuid.uuid4())
    return jsonify({"conversationId": new_conversation_id}), 201  # Return the new ID


@app.route('/api/generateNarrative', methods=['POST'])
def api_generate_narrative():
    data = request.get_json()
    prompt = data.get('prompt')
    conversation_id = data.get('conversationId') 

    try:
        conversation_name = (
            f"projects/{PROJECT_ID}/locations/us-central1/dataStores/"
            f"{DATASTORE_ID}/conversations/{conversation_id}"  # Use the received conversation_id
        )

@app.route('/api/createStory', methods=['POST'])
def api_create_story():
    data = request.get_json()
    story_title = data.get('storyTitle')
    story_content = data.get('storyContent')
    user_id = data.get('userId')  # Make sure userId is being sent from the frontend


    new_story_id = create_story(story_title, story_content, user_id)
    if new_story_id:
        return jsonify({"message": "Story created successfully", "storyId": new_story_id}), 201
    else:
        return jsonify({"error": "Failed to create story"}), 500



@app.route('/api/generateNarrative', methods=['POST'])
def api_generate_narrative():
    data = request.get_json()
    prompt = data.get('prompt')

    try:
        conversation_name = (
            f"projects/{PROJECT_ID}/locations/us-central1/dataStores/"
            f"{DATASTORE_ID}/conversations/{CONVERSATION_ID}"
        )
        request = discoveryengine_v1beta.ConverseConversationRequest(
            name=conversation_name,
            query=discoveryengine_v1beta.TextInput(text=prompt),
        )

        response = gemini_client.converse_conversation(request=request)
        narrative = response.reply.text
        return jsonify({"narrative": narrative}), 200

    except Exception as e:
        logger.error(f"Error generating narrative: {e}")
        return jsonify({"error": "Failed to generate narrative"}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))