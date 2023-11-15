from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import BartForConditionalGeneration, BartTokenizer
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# Load BART model & tokenizer
model_name = 'facebook/bart-large-cnn'
tokenizer = BartTokenizer.from_pretrained(model_name)
model = BartForConditionalGeneration.from_pretrained(model_name)

def extract_text_from_url(url):
    headers = {'User-Agent': 'Mozilla/5.0 ...'}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    main_content = soup.select_one('.main-content-selector')
    if not main_content:
        main_content = soup  # Fallback to the entire soup if specific content is not found

    
    for non_relevant in main_content.select('.non-relevant-section, .footer, .header'):
        non_relevant.decompose()

    
    paragraphs = main_content.find_all('p')
    article_text = ' '.join(p.get_text(strip=True) for p in paragraphs)
    return article_text


    paragraphs = article_body.find_all('p')
    return ' '.join(p.get_text() for p in paragraphs if p.get_text())

@app.route('/summarize', methods=['POST'])
def summarize_text():
    try:
        json_data = request.get_json()
        input_text = json_data.get('text') or extract_text_from_url(json_data.get('url'))

        if not input_text:
            return jsonify({'error': 'No text provided for summarization'}), 400

        inputs = tokenizer([input_text], max_length=1024, return_tensors='pt', truncation=True)
        summary_ids = model.generate(inputs['input_ids'], max_length=150, min_length=150, length_penalty=2.0, num_beams=4, early_stopping=True)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        return jsonify(summary=summary)
    except Exception as e:
        app.logger.error(f'An error occurred: {str(e)}')
        return jsonify({'error': 'An error occurred while summarizing.'}), 500
    
def clean_summary(summary):
    for phrase in ["Log in", "Subscribe now", "Pay for premium", "Donate"]:
        summary = summary.replace(phrase, "")
    return summary


if __name__ == '__main__':
    app.run(debug=True)
