# src/main.py
from flask import Flask, request, jsonify
from ai.gemini_direct import GeminiAPI
from utils.db_utils import DatabaseOperations

app = Flask(__name__)
gemini = GeminiAPI()
db = DatabaseOperations()

@app.route('/create_story', methods=['POST'])
def create_story():
    data = request.get_json()
    user_id = data.get('user_id')
    initial_prompt = data.get('initial_prompt')
    
    if not user_id or not initial_prompt:
        return jsonify({'error': 'Missing required fields'}), 400
    
    story = gemini.generate_content(initial_prompt)
    return jsonify({'story': story})

@app.route('/complete_story', methods=['POST'])
def complete_story():
    data = request.get_json()
    user_id = data.get('user_id')
    story_content = data.get('story_content')
    
    if not user_id or not story_content:
        return jsonify({'error': 'Missing required fields'}), 400
    
    completed_story = gemini.generate_content(f"Complete this story: {story_content}")
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

if __name__ == '__main__':
    app.run(debug=True)