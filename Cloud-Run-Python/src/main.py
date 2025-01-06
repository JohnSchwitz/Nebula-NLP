# src/main.py
from flask import Flask, request, jsonify, send_file
from utils.db_utils import DatabaseOperations
from utils.pdf_utils import generate_story_pdf, generate_narrative_pdf
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

db = DatabaseOperations()

@app.route('/create_story', methods=['POST'])
def create_story():
    try:
        data = request.json
        user_id = data.get('user_id')
        initial_prompt = data.get('initial_prompt')
        
        if not all([user_id, initial_prompt]):
            return jsonify({'error': 'Missing required fields'}), 400
            
        # Your story creation logic here
        return jsonify({'story': 'Generated story content'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    try:
        data = request.json
        doc_type = data.get('type', 'story')
        
        if doc_type == 'story':
            pdf_content = generate_story_pdf(
                data.get('story_name', 'Untitled'),
                data.get('story_content', '')
            )
        else:
            pdf_content = generate_narrative_pdf(
                data.get('narrative_name', 'Untitled'),
                data.get('narrative_content', ''),
                data.get('source_stories', [])
            )
            
        return send_file(
            pdf_content,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f"{data.get('story_name', 'story')}.pdf"
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)