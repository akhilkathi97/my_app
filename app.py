from flask import Flask, render_template
import boto3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ocrApi/<phoneNumber>')
def invoices(phoneNumber):
    req = request.json
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('invoice-ocr-poc.22')
    file_list = [obj.key for obj in bucket.objects.filter(Prefix=phoneNumber+'/'+req['year'] +'/'+req['month'])]
    file_list.pop(0)
    result = { _.split("/")[-1] :ocr_api(_) for _ in file_list }
    for _ in result:
        print(_)
    return result



def ocr_api(doc_name):
    try:
        textract = boto3.client(service_name='textract')
        response = textract.analyze_expense(Document={"S3Object": {"Bucket": "invoice-ocr-poc.22","Name": doc_name}})
        keys= []
        val = []
        for _ in response["ExpenseDocuments"][0]["SummaryFields"]:
            x,y = get_val(_)
            if(x!=None):
                keys.append(x)
                val.append(y)
        final_res = dict()
        invoice_no_added = False
        total_added = False
        for _ in range(len(keys)):
            if("invoice" in keys[_].lower()):
                final_res["invoiceNumber"] = val[_]
                invoice_no_added = True
            if("total" in keys[_].lower()):
                final_res["totalAmount"] = val[_]
                total_added = True
        
        if(not invoice_no_added):
            final_res["invoiceNumber"] = -1
        if(not total_added):
            final_res["totalAmount"] = -1
        return final_res
    except Exception:
        return {"invoiceNumber":"N/A","totalAmount":"N/A"}

def get_val(x):
    try:
        key = x["LabelDetection"]['Text']
        val = x["ValueDetection"]['Text']
        return key,val
    except Exception:
        return None,None


if __name__ == '__main__':
    app.run(port=8000)
