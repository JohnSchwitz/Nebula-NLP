from flask import Flask, request, jsonify, send_file
from dotenv import load_dotenv
from flask_cors import CORS
from utils.utils import DatabaseOperations, generate_story_pdf, generate_narrative_pdf, GeminiAPI  # Correct import

app = Flask(__name__)
cors = CORS(app, resources={r"/create_story": {"origins": "http://localhost:5173"}})
load_dotenv()

db = DatabaseOperations()
gemini = GeminiAPI(db)

@app.route('/api/admin/settings', methods=['GET'])
def get_admin_settings():
    try:
        settings = db.get_admin_settings()
        if settings:
            return jsonify(settings), 200
        else:
            default_settings = {
                "apiKey": None,
                "temperature": 0.7,
                "maxTokens": 1000,
                "storyInstructions": None,
                "narrativeInstructions": None,
                "versionNumber": 1,
            }
            return jsonify(default_settings), 200

    except Exception as e:
        print(f"Error getting admin settings: {e}")
        return jsonify({'error': 'Failed to get admin settings'}), 500

@app.route('/api/admin/settings', methods=['POST'])
def save_admin_settings():
    try:
        settings = request.get_json()
        db.save_admin_settings(settings)  # Assumed function
        return jsonify({'message': 'Admin settings saved successfully'}), 200
    except Exception as e:
        print(f"Error saving admin settings: {e}")
        return jsonify({'error': 'Failed to save admin settings'}), 500

@app.route('/create_story', methods=['POST'])
def create_story():
    try:
        data = request.get_json()
        initial_prompt = data.get('initial_prompt')
        current_story = data.get('current_story', '')

        prompt = f"Continue this story: {current_story}\n\nNext part: {initial_prompt}" if current_story else f"Start a story about: {initial_prompt}"

        settings_version = data.get('settings_version', 1)
        story = gemini.generate_content(prompt, version_number=settings_version, max_tokens=500)

        if isinstance(story, tuple):
            return jsonify({'error': story[0]}), story[1]
        else:
            return jsonify({'story': story}), 200

    except Exception as e:
        print(f"Error in /create_story: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/complete_story', methods=['POST'])
def complete_story():
    try:
        data = request.get_json()
        story_content = data.get('story_content')
        prompt = f"Please provide the complete story incorporating all previous elements:\n\n{story_content}"
        completed_story = gemini.generate_content(prompt, max_tokens=6000)
        if isinstance(completed_story, tuple):
            return jsonify({'error': completed_story[0]}), completed_story[1]
        else:
            return jsonify({'story': completed_story}), 200

    except Exception as e:
        print(f"Error in /complete_story: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/generate_narrative', methods=['POST'])
def generate_narrative_route():
    try:
        data = request.get_json()
        selected_stories = data.get('selected_stories')

        # Construct your prompt using selected_stories here

        narrative = gemini.generate_narrative(prompt) # 'prompt' needs to be defined based on selected_stories
        return jsonify(narrative), 200

    except Exception as e:
        print(f"Error generating narrative: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/save_story', methods=['POST'])
def save_story():
    data = request.get_json()
    user_id = data.get('user_id')
    story_name = data.get('story_name')
    story_content = data.get('story_content')

    if not all([user_id, story_name, story_content]):
        return jsonify({'error': 'Missing required fields'}), 400

    story_id = db.save_story(user_id, story_name, story_content)
    return jsonify({'story_id': story_id}), 201  # 201 Created is more appropriate


@app.route('/get_user_stories', methods=['GET'])
def get_user_stories():
    try:
        user_id_str = request.args.get('user_id')
        if user_id_str:
            try:
                user_id = int(user_id_str)
            except ValueError:
                return jsonify({'error': 'Invalid user_id: not an integer'}), 400
        else:
            user_id = 1  # Default

        stories = db.get_user_stories(user_id)
        return jsonify(stories if stories is not None else []), 200

    except Exception as e:
        print(f"Error in get_user_stories: {e}")
        return jsonify({'error': 'Failed to fetch stories'}), 500


@app.route('/update_narrative', methods=['POST'])
def update_narrative():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        narrative_input = data.get('narrative_input')
        current_narrative = data.get('current_narrative')
        selected_stories = data.get('selected_stories')
        settings_version = data.get('settings_version', 1)

        # Construct your prompt here (missing from original code)

        updated_narrative = gemini.generate_content(prompt, version_number=settings_version, max_tokens=500) # 'prompt' needs to be defined

        if isinstance(updated_narrative, tuple):
            return jsonify({'error': updated_narrative[0]}), updated_narrative[1]

        return jsonify({'narrative': updated_narrative}), 200

    except Exception as e:
        print(f"Error in /update_narrative: {e}")
        return jsonify({'error': str(e)}), 500



@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    data = request.get_json()
    story_name = data.get('story_name')
    story_content = data.get('story_content')

    if not story_name or not story_content:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        pdf_content = generate_story_pdf(story_name, story_content)  # Assuming this function exists in utils.pdf_utils or similar
        return pdf_content, 200, {
            'Content-Type': 'application/pdf',
            'Content-Disposition': f'attachment; filename="{story_name}.pdf"'
        }
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)




