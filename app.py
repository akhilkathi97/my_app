from flask import Flask, render_template,request

import boto3
import re

import requests
from smart_open import open


app = Flask(__name__)


@app.route('/')

def index():

    return render_template('index.html')


#@app.route('/uploadFile')
def upload_files(req):

    fileLocation ="Users/"+str(req['phonenumber'])+"/"+str(req["year"])+"/"+str(req["month"])

    response = {}

    for _ in req["purchaseInvoices"]:

        response = requests.get(_['inv_location'], stream=True)

        s3url = 's3://invoice-ocr-poc.22/' + fileLocation+"/purchaseInvoices/"+_['inv_name']

        with open(s3url, 'wb') as fout:

            fout.write(response.content)

    for _ in req["saleInvoices"]:

        response = requests.get(_['inv_location'], stream=True)

        s3url = 's3://invoice-ocr-poc.22/' + fileLocation+"/saleInvoices/"+_['inv_name']

        with open(s3url, 'wb') as fout:

            fout.write(response.content)


@app.route('/ocrApi')

def invoices():

    req = request.json

    phoneNumber = req["phonenumber"]

    if(req['uploadToS3']):
        upload_files(req)

    s3 = boto3.resource('s3')

    bucket = s3.Bucket('invoice-ocr-poc.22')

    folderList = ["purchaseInvoices","saleInvoices"]
    file_list = []

    for _ in folderList:

        file_list_ = [obj.key for obj in bucket.objects.filter(Prefix="Users/"+phoneNumber+'/'+req['year'] +'/'+req['month']+'/'+_)]

        file_list.extend(file_list_)

    result = { _.split("/")[-1] :ocr_api(_) for _ in file_list }
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

                amount = val[_]

                digits = re.sub(r"\D",'',amount)

                chars = re.sub(r"\d",'',amount)

                if(chars[-1]=='.'):

                    digits = digits/100

                final_res["invoiceNumber"] = digits

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

