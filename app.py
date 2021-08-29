import json
import os
from flask import Flask
from flask import request
from flask import make_response
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


cred = credentials.Certificate("iamsaddog-fvit-firebase-adminsdk-j597m-549b61b116.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)
#flask app should be start on global layout

@app.route('/webhook',methods=['POST'])
#@app.route = A decorator that is used to register a view function for a given URL rule. 
#method GET = การรับส่งข้อมูลผ่านทาง URL แบบเห็นข้อมูลที่ส่งไปได้ POST = ไม่เห็นข้อมูลที่ส่ง แต่จะไม่มีปัญหาด้านขนาดข้อมูลที่ส่ง

def webhook():
    req = request.get_json(silent = True,force=True)
    #Parses(แยกวิเคราะห์) the incoming JSON request data and returns it
    res = processRequest(req)
    res = json.dumps(res,indent = 4)
    # Serialize obj to a JSON formatted str.
    #คือการแปลง Python Object (Dict) ไปเป็น JSON 
    r = make_response(res)
    #make_response ทำให้สามารถดู return และ เพิ่ม headers ได้ทั้งสอง ต่างจาก return ที่สามารถดูได้อย่างเดียว
    r.headers['Content-Type'] = 'application/json'
    #เพิ่ม headers
    return r

def processRequest(req):## Parsing(การแยกวิเคราะห์) the POST request body into a dictionary for easy access.
    req_dict =json.loads(request.data)
    print(req_dict)
    ## Accessing the fields on the POST request body of API.ai invocation of the webhook
    intent = req_dict["queryResult"]["intent"]["displayName"]
    if intent == "ถามหนังน่าดู":
        doc_ref = db.collection(u'movies').document(u'IeaibPfdLF1OZT9m9GEn')
        doc = doc_ref.get().to_dict()
        print(doc)

        movie_name = doc['movie_name']
        rel_date = doc['release_date']
        speech = f'ตอนนี้มีเรื่อง {movie_name} เข้าโรงวันที่ {rel_date}'

    else:

        speech = "ผมไม่เข้าใจ คุณต้องการอะไร"

    res = makeWebhookResult(speech)

    return res


def makeWebhookResult(speech):

    return {
  "fulfillmentText": speech
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0', threaded=True)

