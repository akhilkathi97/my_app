from flask import Flask, render_template
import boto3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ocrApi/<doc_name>')
def ocr_api(doc_name):
    try:
        textract = boto3.client(service_name='textract')
        return textract.analyze_expense(Document={"S3Object": {"Bucket": "invoice-ocr-poc.22","Name": doc_name}})
    except Exception as e_raise:
        return jsonify(e_raise)

if __name__ == '__main__':
    app.run(port=8000)

