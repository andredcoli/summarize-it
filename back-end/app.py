from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import BartForConditionalGeneration, BartTokenizer
import requests  
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

#BART MODEL & TOKENIZER
model_name = 'facebook/bart-large-cnn'
tokenizer = BartTokenizer.from_pretrained(model_name)
model = BartForConditionalGeneration.from_pretrained(model_name)

@app.route('/summarize', methods=['POST'])


@app.route('/summarize', methods=['POST'])
def summarize_text():
    try:
        json_data = request.get_json()
        input_text = json_data.get('text')

        if not input_text:
            return jsonify({'error': 'No text provided for summarization'}), 400

        inputs = tokenizer([input_text], max_length=1024, return_tensors='pt', truncation=True)
        summary_ids = model.generate(inputs['input_ids'], max_length=150, min_length=150, length_penalty=2.0, num_beams=4, early_stopping=True)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        return jsonify(summary=summary)
    except Exception as e:
        app.logger.error(f'An error occurred: {str(e)}')
        return jsonify({'error': 'An error occurred while summarizing.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
