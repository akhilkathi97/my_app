from flask import Flask, render_template,json
import gunicorn

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ocrApi/<documentName>')
def ocr_api(documentName):
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
        res = textract.analyze_expense(
           Document={
                "S3Object": {
                    "Bucket": "invoice-ocr-poc.22",
                    "Name": documentName
                }
            })
        response = app.response_class(response=json.dumps(res),status=200,mimetype='application/json')
        return response
        #pretty_printed_string = get_string(textract_json=response, output_type=[Textract_Expense_Pretty_Print.SUMMARY, Textract_Expense_Pretty_Print.LINEITEMGROUPS], table_format=Pretty_Print_Table_Format.fancy_grid)
        #print(pretty_printed_string)
    except Exception as e_raise:
        print(e_raise)
        return app.response_class(response=e_raise,status=400)

