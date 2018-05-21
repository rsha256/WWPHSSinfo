'''  
     author : @krishnan_ram 
     description : makes and shares completed google slide with correct user.
     
'''

#'''#'''#'''#''CODE'#'''#'''#'''#'''#

#imports. reference requirements.txt for full list.
from __future__ import print_function
from apiclient import discovery
from datetime import date
from httplib2 import Http
from oauth2client import file, client, tools
from oauth2client.service_account import ServiceAccountCredentials

import gspread
import json
import datetime

################################

#NOTE: PLEASE HAVE client_secrets.json AND credentials.json IN THE SAME FOLDER AS THIS CODE!
#      IF YOU ARE GOING TO BE USING A JSON OBJECT INSTEAD OF A JSON FILE AS THE DATA TYPE,
#      PLEASE EDIT THE CODE ACCORDINGLY (START AT LINE 168). 

'''
copies template slide, modiifies it according to data, and then shares it to user along with necessary google sheet.

params: 
        d:
            json data.
        email:
            the email the slides and sheet will be shared with,
       
'''
def slides_update_share(d,email):
    #Load data.
    absents = d['absents']
    announcements = d['board']['announcements']
    quote = d['board']['quote'] 
    date1 = d['board']['timestamp'][:10]
    day = d['board']['day']
    date1 = date(day=int(date1[8:10]), month=int(date1[6:7]), year=int(date1[:4])).strftime('%A, %d %B, %Y') 
   
    #initialize APIs
    SCOPES = (
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/presentations',
    )
    store = file.Storage('credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret1.json', SCOPES)
        creds = tools.run_flow(flow, store)
    HTTP = creds.authorize(Http())
    DRIVE  = discovery.build('drive',  'v3', http=HTTP)
    DRIVE1 = discovery.build('drive',  'v2', http=HTTP)
    SLIDES = discovery.build('slides', 'v1', http=HTTP)
    
   
   # Copies template slide into different name
    TMPLFILE = 'HSSinfo3'   # use your own!
    now = datetime.datetime.now()
    NEWFILE = 'HSSInfo_' + now.strftime("%Y-%m-%d")
    rsp = DRIVE.files().list(q="name='%s'" % TMPLFILE).execute().get('files')[0]
    DATA = {'name': NEWFILE}
    print('** Copying template %r as %r' % (rsp['name'], DATA['name']))
    DECK_ID = DRIVE.files().copy(body=DATA, fileId=rsp['id']).execute().get('id')
    print('** Get slide objects, search for image placeholder')
    slide = SLIDES.presentations().get(presentationId=DECK_ID,
            fields='slides').execute().get('slides')[0]

    # Inserts relevant text into newly made slide
    reqs = [
        {'replaceAllText': {
            'containsText': {'text': '{{ ANNOUNCEMENTS }}'},
            'replaceText': announcements
        }},{'replaceAllText': {
            'containsText': {'text': '{{ QUOTE }}'},
            'replaceText': quote
        }},{'replaceAllText': {
            'containsText': {'text': '{{ DAY }}'},
            'replaceText': day
        }},{'replaceAllText': {
            'containsText': {'text': '{{ DATE }}'},
            'replaceText': date1
        }}
    ]
    SLIDES.presentations().batchUpdate(body={'requests': reqs},
            presentationId=DECK_ID).execute()
   
    # ensures no errors
    import time
    time.sleep(1)
    
    #Shares completed slide with user
    file_id = DECK_ID
    def callback(request_id, response, exception):
        if exception:
        # Handle error
            print(exception)
        else:
            pass
    batch = DRIVE.new_batch_http_request(callback=callback)
    user_permission = {
    'type': 'user',
    'role': 'writer',
    'emailAddress': email     
    }
    batch.add(DRIVE.permissions().create(
        fileId=file_id,
        body=user_permission,
        fields='id'
    ))
    batch.execute()
    user_permission = {
    'type': 'user',
    'role': 'reader',
    'emailAddress': email     
    }
    batch.add(DRIVE.permissions().create(
        fileId='1RiH2GfsURjB6Z60DVNnvpqHvQDZLFmi-xYHEbskdl20',      #<-- FileID of HSSINFO sheet.
        body=user_permission,
        fields='id'
    ))
    batch.execute()
    print('DONE')

#################################

'''
edits sheet and then runs the above function to create a slide using the sheet.

params: 
       
       json_path:
            path to json with data.
            
'''

def slide_sheet_creator(json_path,email):    
    print("STARTING DATA PREPROCESSING")
    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sheet = client.open("HSSINFO").sheet1
    sheet.clear()
    sheet.insert_row(['Teachers','Hours',' ', 'Teachers(Cont.)','Hours(Cont.)', ' ', ' ','Period', 'Start', 'End'],index=1,value_input_option='RAW')
    # Extract and print all of the values
    list_of_hashes = sheet.get_all_records()

    #preprocess json data
    absents = []
    teachers = []
    hours = []
    teachers_cont = []
    hours_cont = []
    periods = [] 
    starts = []
    ends = []
    with open(json_path) as json_data:
        ingested_json = json.load(json_data)
        absents = ingested_json['absents']
        for item in ingested_json['schedule']:
            if item['number'] is not None:
                periods.append(item['number'])
                starts.append(item['start'])
                ends.append(item['end'])

    if len(periods) < 9:
        periods = periods + [" "]*(9-len(periods))
        starts = starts + [" "]*(9-len(starts))
        ends = ends + [" "]*(9-len(ends))
    for item in absents:
        teachers.append(item['teacher'])
        hours.append(item['hours'])
    if len(teachers) > 8:
        teachers_cont = teachers[8:]
        hours_cont = hours[8:]
        teachers = teachers[:9]
        hours = hours[:9]
        num_left = 8 - len(teachers_cont)
        if num_left > 0: 
            teachers_cont = teachers_cont + [" "]*num_left
            hours_cont = hours_cont + [" "]*num_left



    print("ADDING ALL DATA") 
    #add all data to sheets in proper format
    if len(teachers_cont) != 0:
        for i in range(0,8):
            sheet.insert_row([teachers[i], hours[i], " ",  teachers_cont[i],  hours_cont[i], " ",    
            " ",periods[i],starts[i],ends[i]],index=(i+2), value_input_option='RAW')
    else:
        for i in range(len(absents)):
            sheet.insert_row([teachers[i],hours[i], " ", " ", " ", " ", " ",periods[i],starts[i],ends[i]],index=i+2,        
            value_input_option='RAW')
    sheet.insert_row([" "," ", " ", " ", " ", " ", " ",periods[8],starts[8],ends[8]], index=10,value_input_option='RAW')

    print("FINISHED DATA RELATED PROCESSES. STARTING 'slides_update_share'")
    #use previously made function to create new slides with all the new stuff
    slides_update_share(ingested_json,email)

    
#runs everything through 'slide_sheet_creator'. comment on and off as needed. editing of params may be necessary.
#slide_sheet_creator('sample.json','20kr0756@wwprsd.org')



'''  
     author : @krishnan_ram 
     description : makes and shares completed google slide with correct user.
     
'''