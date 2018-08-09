import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

SCOPES = 'https://www.googleapis.com/auth/calendar'

def get_service():
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    return build('calendar', 'v3', http=creds.authorize(Http()))

def create_calendar(club_name):
    calendar = {
        'summary': club_name,
        'timeZone': 'America/New_York'
    }
    created_calendar = get_service().calendars().insert(body=calendar).execute()
    return created_calendar['id']

def create_event(cal_id, summary, location, description, start_time, end_time):
    event = {
        'summary': summary,
        'location': location,
        'description': description,  
        'start': {
            'dateTime': start_time,
            'timeZone': 'America/New_York',
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'America/New_York',
         },
    }
    event=get_service().events().insert(calendarId=cal_id, body=event).execute()
    return event.get('htmlLink')

def get_events(cal_id):
    all_events= []
    page_token = None
    while True:
        events = get_service().events().list(calendarId='primary', pageToken=page_token).execute()
        for event in events['items']:
            all_events.append(event)
        page_token = events.get('nextPageToken')
        if not page_token:
            break
    return all_events

