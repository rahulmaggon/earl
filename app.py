from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
from flask import jsonify
import requests, json

# Create a engine for connecting to SQLite3.
# Assuming salaries.db is in your app root folder


app = Flask(__name__)
api = Api(app)


class Departments_Meta(Resource):
    def get(self):
        # Connect to databse

        return 'abc'


@app.route('/tasks', methods=['POST'])
def add_message():
    d3 = request.get_json()  # 'dumps' gets the dict from 'loads' this time
    print (d3)
    print d3.values()[0]

    intent = d3['result']['metadata']['intentName']
    if intent == 'Bookings':
        print 'Inside Bookings'
        metrics = d3['result']['parameters']['Metrics']
        geo = d3['result']['parameters']['Geography']
        action = d3['result']['parameters']['Action']
        actioncreaatedby = d3['originalRequest']['data']['data']['personEmail']
        headers = {'Authorization': 'Bearer 0/76766095a39c4d5583bc4ff41dd12aa7'}
        payload = {
            'data': {
                'assignee': 503934498601499,
                'workspace': 502764150171378,
                'name': metrics + ' are low for ' + geo + '. Can you please check ?',
                'memberships': [{
                    'project': 502758303624101,
                    'section': 0
                }],
                'followers[0]': 502765457090117
            }
        }

        r = requests.post('https://app.asana.com/api/1.0/tasks', data=json.dumps(payload), headers=headers)
        response1 = (r.json())

        payloadalert = {
            'toPersonEmail': 'rmaggon@cisco.com',
            'text': str(response1['data']['id'])+' '+ metrics + ' are low for ' + geo + '. Can you please check ? - Action Item assigned by ' + actioncreaatedby
        }
        headersalert = {'Content-type': 'application/json; charset=utf-8',
                        'Authorization': 'Bearer ZTMyMjVlZTMtMTUwOS00ZGRmLTg0ZDMtZWQ5NzIxN2RlN2FiZGI0OTkxOGUtNWNk'}
        ralert = requests.post('https://api.ciscospark.com/v1/messages', data=json.dumps(payloadalert),
                               headers=headersalert)
        print ralert
        return jsonify(speech=str(response1['data']['id']) + ' An Action Item has been created an assigned to ' +
                              response1['data']['assignee']['name'],
                       displayText='An Action Item has been created an assigned to ' + response1['data']['assignee'][
                           'name'])
    elif intent == 'CloseTask':
        taskid = d3['result']['parameters']['any']
        print intent
        headerstask = {'Authorization': 'Bearer 0/76766095a39c4d5583bc4ff41dd12aa7'}
        payloadtask = {
            'data': {
                'completed': 'true',
            }
        }
        rtask = requests.put('https://app.asana.com/api/1.0/tasks/' + str(taskid), data=json.dumps(payloadtask),
                              headers=headerstask)
        responsetask = (rtask.json())
        print responsetask
        payloadalert = {
            'toPersonEmail': 'rmaggon@cisco.com',
            'text': str(responsetask['data']['id'])+' '+responsetask['data']['name']+' has been closed.'
        }
        headersalert = {'Content-type': 'application/json; charset=utf-8',
                        'Authorization': 'Bearer ZTMyMjVlZTMtMTUwOS00ZGRmLTg0ZDMtZWQ5NzIxN2RlN2FiZGI0OTkxOGUtNWNk'}
        ralert = requests.post('https://api.ciscospark.com/v1/messages', data=json.dumps(payloadalert),
                               headers=headersalert)
        return jsonify(speech='Task Marked as Completed')


@app.route('/tasks2', methods=['POST'])
def add_task():
    d3 = request.get_json()  # 'dumps' gets the dict from 'loads' this time
    print d3
    print d3.values()[0]
    intent = d3['result']['metadata']['intentName']

    if intent == 'EventTrigger':
        metrics = d3['result']['parameters']['Metrics']
        geo = d3['result']['parameters']['Geography']
        user = d3['originalRequest']['data']['data']['personEmail']
        sparkWelcomeMsg = {
            'toPersonEmail': user,
            'text': 'Hello '+user+', What is your concern with '+metrics+' metrics'+' for '+geo + ' ?'
        }
        headersalert = {'Content-type': 'application/json; charset=utf-8',
                        'Authorization': 'Bearer ZTMyMjVlZTMtMTUwOS00ZGRmLTg0ZDMtZWQ5NzIxN2RlN2FiZGI0OTkxOGUtNWNk'}
        ralert = requests.post('https://api.ciscospark.com/v1/messages', data=json.dumps(sparkWelcomeMsg),
                               headers=headersalert)
        print ralert
        return jsonify('"followupEvent": { "name": "EventTrigger-followup", "data": { "metrics": "bookings" } }')
    elif intent == 'EventTrigger - custom - yes':
        metrics = d3['result']['contexts'][0]['parameters']['Metrics']
        geo = d3['result']['contexts'][0]['parameters']['Geography']
        issue = d3['result']['contexts'][0]['parameters']['issue']
        headers = {'Authorization': 'Bearer 0/76766095a39c4d5583bc4ff41dd12aa7'}
        payload = {
            'data': {
                'assignee': 503934498601499,
                'workspace': 502764150171378,
                'name': metrics + ' are '+issue+' for ' + geo + '. Can you please check ?',
                'memberships': [{
                    'project': 502758303624101,
                    'section': 0
                }],
                'followers[0]': 502765457090117
            }
        }
        r = requests.post('https://app.asana.com/api/1.0/tasks', data=json.dumps(payload), headers=headers)
        response1 = (r.json())
        user = d3['originalRequest']['data']['data']['personEmail']
        payloadalert = {
            'toPersonEmail': 'rmaggon@cisco.com',
            'text': str(response1['data'][
                            'id']) + ' ' + metrics + ' are '+issue+' for ' + geo + '. Can you please check ? - Action Item assigned by ' + user
        }
        headersalert = {'Content-type': 'application/json; charset=utf-8',
                        'Authorization': 'Bearer ZTMyMjVlZTMtMTUwOS00ZGRmLTg0ZDMtZWQ5NzIxN2RlN2FiZGI0OTkxOGUtNWNk'}
        ralert = requests.post('https://api.ciscospark.com/v1/messages', data=json.dumps(payloadalert),
                               headers=headersalert)
        return jsonify(speech=str(response1['data']['id']) + ' An Action Item has been created and assigned to ' +
                              response1['data']['assignee']['name'],
                       displayText='An Action Item has been created an assigned to ' + response1['data']['assignee'][
                           'name'])
    elif intent == 'TaskComments - custom':
        taskID = d3['result']['contexts'][0]['parameters']['id.original']
        comments = d3['result']['contexts'][0]['parameters']['Comments.original']
        headers = {'Authorization': 'Bearer 0/76766095a39c4d5583bc4ff41dd12aa7'}
        payload = {
            'data': {
                'text': comments
            }
        }
        r = requests.post('https://app.asana.com/api/1.0/tasks/'+taskID+'/stories', data=json.dumps(payload), headers=headers)
        response1 = (r.json())
        print response1
        payloadComments = {
            'toPersonEmail': 'rmaggon@cisco.com',
            'text': 'Following Comments has been added to Task ID *'+taskID+'* : \n'+comments+' by '+'**Rahul Maggon**'
        }
        headersalertComments = {'Content-type': 'application/json; charset=utf-8',
                        'Authorization': 'Bearer ZTMyMjVlZTMtMTUwOS00ZGRmLTg0ZDMtZWQ5NzIxN2RlN2FiZGI0OTkxOGUtNWNk'}
        ralert = requests.post('https://api.ciscospark.com/v1/messages', data=json.dumps(payloadComments),
                               headers=headersalertComments)
        return jsonify(speech='Comment has been added to task '+taskID+' successfully!!!')
    elif intent == 'CloseTask':
        print intent
        taskid = d3['result']['parameters']['any']
        closureComments = d3['result']['parameters']['comments']
        print intent
        headerstask = {'Authorization': 'Bearer 0/894af380f603cfa9e94ded1119b00065'}
        payloadtask = {
            'data': {
                'completed': 'true',
            }
        }
        rtask = requests.put('https://app.asana.com/api/1.0/tasks/' + str(taskid), data=json.dumps(payloadtask),
                             headers=headerstask)
        responsetask = (rtask.json())
        print responsetask
        payloadalert = {
            'toPersonEmail': 'saddala@cisco.com',
            'text': str(responsetask['data']['id']) + ' ' + responsetask['data']['name'] + ' has been closed with following comments:\n'+closureComments
        }
        headersalert = {'Content-type': 'application/json; charset=utf-8',
                        'Authorization': 'Bearer ZTMyMjVlZTMtMTUwOS00ZGRmLTg0ZDMtZWQ5NzIxN2RlN2FiZGI0OTkxOGUtNWNk'}
        ralert = requests.post('https://api.ciscospark.com/v1/messages', data=json.dumps(payloadalert),
                               headers=headersalert)
        CTaskheaders = {'Authorization': 'Bearer 0/894af380f603cfa9e94ded1119b00065'}
        CTaskpayload = {
            'data': {
                'text': closureComments
            }
        }
        cTaskr = requests.post('https://app.asana.com/api/1.0/tasks/' + taskid + '/stories', data=json.dumps(CTaskpayload),
                          headers=CTaskheaders)
        cTaskresponse1 = (cTaskr.json())
        print cTaskresponse1
        return jsonify(speech='Task has been marked as Completed')
    elif intent == 'TaskCreator':
        print intent
        headersTaskCreator = {'Authorization': 'Bearer 0/76766095a39c4d5583bc4ff41dd12aa7'}
        r = requests.get('https://app.asana.com/api/1.0/tasks?assignee=503934498601499&&workspace=502764150171378', headers=headersTaskCreator)
        taskList = (r.json())
        print taskList
        taskid1= taskList['data'][0]['id']
        taskName1 =  taskList['data'][0]['name']
        taskid2= taskList['data'][1]['id']
        taskName2 = taskList['data'][1]['name']
        return jsonify(speech='Here is the list of Tasks Created by you:\n'+str(taskid1)+' : '+taskName1+'\n'+str(taskid2)+' : '+taskName2+'\n')
    elif intent == 'TaskAssigned':
        print intent
        headersTaskCreator = {'Authorization': 'Bearer 0/76766095a39c4d5583bc4ff41dd12aa7'}
        r = requests.get('https://app.asana.com/api/1.0/tasks?assignee=503934498601499&&workspace=502764150171378', headers=headersTaskCreator)
        taskList = (r.json())
        print taskList
        taskid1= taskList['data'][0]['id']
        taskName1 =  taskList['data'][0]['name']
        taskid2= taskList['data'][1]['id']
        taskName2 = taskList['data'][1]['name']
        return jsonify(speech='Here is the list of Tasks Assigned to you:\n'+str(taskid1)+' : '+taskName1+'\n'+str(taskid2)+' : '+taskName2+'\n')

@app.route('/query', methods=['POST'])
def add_query():
    d3 = request.get_json()  # 'dumps' gets the dict from 'loads' this time
    print d3
    print d3.values()[0]
    metrics = d3['result']['parameters']['Metrics']
    geo = d3['result']['parameters']['Geo']
    period = d3['result']['parameters']['Period']
    payloadQuery = {
    'hierarchyName':geo,
    'timePeriod':'20174',
    'cecId':'souagraw'
    }

    headersalert = {'Content-type': 'application/json; charset=utf-8',
                    'Authorization': 'Basic c2l2YW1hcmk6V2h5NFNvbHIk'}
    ralert = requests.post('https://mbr-dev.cloudapps.cisco.com/mbrng/services/orderLifecycleBookings/weekly/getBookings', data=json.dumps(payloadQuery),
                           headers=headersalert)
    print ralert.json()
    return jsonify(speech=round(ralert.json()['sumOfActualAmount'], 2))


api.add_resource(Departments_Meta, '/departments')

if __name__ == '__main__':
    app.run()
