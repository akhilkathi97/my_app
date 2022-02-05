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
    print(documentName)
    try:
        response = textract.analyze_expense(
           Document={
                "S3Object": {
                    "Bucket": "invoice-ocr-poc.22",
                    "Name": documentName
                }
            })
        return response
        #pretty_printed_string = get_string(textract_json=response, output_type=[Textract_Expense_Pretty_Print.SUMMARY, Textract_Expense_Pretty_Print.LINEITEMGROUPS], table_format=Pretty_Print_Table_Format.fancy_grid)
        #print(pretty_printed_string)
    except Exception as e_raise:
        print(e_raise)
        return e_raise

if __name__ == '__main__':
    app.run(port=8000)

