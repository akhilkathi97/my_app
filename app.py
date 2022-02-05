from flask import Flask, render_template,json,jsonify
import gunicorn
import boto3
import os
from textractprettyprinter.t_pretty_print_expense import get_string, Textract_Expense_Pretty_Print, Pretty_Print_Table_Format
from flask import Flask, jsonify, request,send_file

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ocrApi/<documentName>')
def ocr_api(documentName):
    textract = boto3.client(service_name='textract')
    return "Hello World 2.0"
    """{
       "Document": { 
          "Bytes": blob,
          "S3Object": { 
             "Bucket": "string",
             "Name": "string",
             "Version": "string"
          }
       }
    }"""
    try:
        response = textract.analyze_expense(
           Document={
                "S3Object": {
                    "Bucket": "invoice-ocr-poc.22",
                    "Name": documentName
                }
            })
        return jsonify(response)
        
    except Exception as e_raise:
        print(e_raise)
        return jsonify(e_raise)

if __name__ == '__main__':
    app.run(port=8000)

