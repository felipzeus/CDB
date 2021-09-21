from flask import Flask, request
from webexteamssdk import WebexTeamsAPI, Webhook
from cardcontent import *
import smartsheet

app = Flask (__name__)
api = WebexTeamsAPI(access_token="NGYyNjhkMzUtZjFiOC00YzNiLWFlOWItYWI5ODNkZWZkNWMwMjJkNmE3NWYtMDA3_PF84_41bb3162-5f04-4859-89a6-4a32bdd42e26")

@app.route('/', methods=['POST', 'GET'])
def home ():
        return 'OK', 200

@app.route('/webhookreq', methods=['POST', 'GET'])
def webhookreq():
    if request.method == 'POST':
        req = request.get_json() 

        data_personId = req['data']['personId']
        data_roomId = req['data']['roomId']

        #Loop prevention VERY IMPORTNAT! 
        me = api.people.me() 
        if data_personId == me.id: 
            return 'OK', 200 
        else: 
            if api.messages.create(roomId=data_roomId, text='TOMA PATATA!!!', attachments=[{"contentType": "application/vnd.microsoft.card.adaptive", "content": cardcontent}]):
                return "OK" 

    elif request.method == 'GET':
            return "Si, me pongo a currar."
    return 'OK', 200

@app.route('/cardsubmitted', methods=['POST'])
def cardsubmitted():
    if request.method == 'POST': 
	    req = request.get_json()

	    data_id = req['data']['id']

	    attachment_actions = api.attachment_actions.get(data_id)
	    inputs = attachment_actions.inputs

	    myName = inputs['myName']
	    myEmail = inputs['myEmail']
	    myTel = inputs['myTel']

    print(myName)
    print(myEmail)
    print(myTel)
    
    smart = smartsheet.Smartsheet('5w53mEr52kvBxhnVYxoKXjyuwwo85d5Wdsq6b')
    smart.errors_as_exceptions(True)

    newRow = smartsheet.models.Row()
    newRow.to_top = True

    newRow.cells.append({'column_id': 2269257672222596, 'value':myName})
    newRow.cells.append({'column_id': 1143357765379972, 'value':myEmail,'strict': False})
    newRow.cells.append({'column_id': 3395157579065220, 'value':myTel,'strict': False})
    response = smart.Sheets.add_rows(7177046196545412,newRow)


    return 'OK', 200

if __name__=='__main__':
    app.debug = True
    app.run(host="0.0.0.0")
