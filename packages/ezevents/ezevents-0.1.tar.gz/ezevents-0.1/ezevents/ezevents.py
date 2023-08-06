from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import argparse

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the upcoming events on the user's calendar.
    """
    # Create the parser
    parser = argparse.ArgumentParser(prog='ezevents',
                                     description="Prints the details of the upcoming events on the user's calendar.")

    # Add the arguments
    parser.add_argument('--number', '-n',
                        action='store',
                        type=int,
                        default=5,
                        help='Number of events to be displayed')
    parser.add_argument('--add',
                        action='store_true',
                        help='Add an event on Calendar')
    parser.add_argument('--name',
                        action='store',
                        type=str,
                        default='An Event',
                        help='Event Name')
    parser.add_argument('--location', '-l',
                        action='store',
                        type=str,
                        help='Event Location')
    parser.add_argument('--description', '-desc',
                        action='store',
                        type=str,
                        help='Event Description')
    parser.add_argument('--date', '-d',
                        action='store',
                        # usage='%(prog)s [YYYY-MM-DD] [YYYY-MM-DD]',
                        default=[datetime.datetime.now().strftime('%Y-%m-%d'), datetime.datetime.now().strftime('%Y-%m-%d')],
                        type=str,
                        nargs=2,
                        help='Event Dates')
    parser.add_argument('--time', '-t',
                        action='store',
                        # usage='%(prog)s [HH-MM] [HH-MM]',
                        default=[datetime.datetime.now().strftime('%H:%M:%S'), datetime.datetime.now().strftime('%H:%M:%S')],
                        type=str,
                        nargs=2,
                        help='Event Timings')
    parser.add_argument('--attendees', '-at',
                        action='store',
                        type=list,
                        default=[],
                        nargs='+',
                        help='Email address of attendees.')

    # Execute the parse_args() method
    args = parser.parse_args()

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    if args.add:
        event = {
            'summary': args.name,
            'location': args.location,
            'description': args.description,
            'start': {
                # 'dateTime': 'YYYY-MM-DDTHH:MM:SS+0530',
                'dateTime': args.date[0] + 'T' + args.time[0] + '+0530',
                'timeZone': 'Asia/Kolkata',

            },
            'end': {
                # 'dateTime': 'YYYY-MM-DDTHH:MM:SS+0530',
                'dateTime': args.date[1] + 'T' + args.time[1] + '+0530',
                'timeZone': 'Asia/Kolkata',

            },
            'attendees': [{'email': mail} for mail in args.attendees],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }
        # print(datetime.datetime.now().strftime('%H:%M:%S'))
        # print(event)
        # event = service.events().insert(calendarId='primary', body=event).execute()
        service.events().insert(calendarId='primary', body=event).execute()
        print("Event Added")

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming {} events'.format(args.number))
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=args.number, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


if __name__ == '__main__':
    main()
