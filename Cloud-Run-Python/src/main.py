from flask import Flask, request, jsonify
from flask_cors import CORS
from ai.gemini_direct import GeminiAPI
from utils.db_utils import DatabaseOperations

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

gemini = GeminiAPI()
db = DatabaseOperations()

@app.route('/create_story', methods=['POST'])
def create_story():
    data = request.get_json()
    initial_prompt = data.get('initial_prompt')
    current_story = data.get('current_story', '')
    
    if current_story:
        prompt = f"Continue this story (do not complete it yet): {current_story}\n\nNext part: {initial_prompt}"
    else:
        prompt = f"Start a story about: {initial_prompt}"
    
    story = gemini.generate_content(prompt, max_tokens=500)  # Limit tokens for first iteration
    return jsonify({'story': story})

@app.route('/complete_story', methods=['POST'])
def complete_story():
    data = request.get_json()
    story_content = data.get('story_content')
    complete_prompt = data.get('complete_prompt', 'Please provide the complete story')
    
    prompt = f"{complete_prompt}:\n\n{story_content}"
    completed_story = gemini.generate_content(prompt, max_tokens=2048)
    return jsonify({'story': completed_story})

@app.route('/save_story', methods=['POST'])
def save_story():
    data = request.get_json()
    user_id = data.get('user_id')
    story_name = data.get('story_name')
    story_content = data.get('story_content')
    
    if not all([user_id, story_name, story_content]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    story_id = db.save_story(user_id, story_name, story_content)
    return jsonify({'story_id': story_id})

@app.route('/get_stories', methods=['GET'])
def get_stories():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'Missing user_id'}), 400
    
    stories = db.get_user_stories(int(user_id))
    return jsonify(stories)

@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    data = request.get_json()
    story_name = data.get('story_name')
    story_content = data.get('story_content')
    
    if not story_name or not story_content:
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        from utils.pdf_utils import generate_story_pdf
        pdf_content = generate_story_pdf(story_name, story_content)
        return pdf_content, 200, {
            'Content-Type': 'application/pdf',
            'Content-Disposition': f'attachment; filename="{story_name}.pdf"'
        }
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)