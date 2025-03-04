import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json
SCOPES = ["https://www.googleapis.com/auth/calendar"]



def get_credentials():
    creds = None

    if os.path.exists("creds/token.json"):
        creds = Credentials.from_authorized_user_file("creds/token.json", SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "creds/credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("creds/token.json", "w") as token:
            token.write(creds.to_json())

    return creds



class GoogleCalendarSearch:
    def __init__(self, **kwargs):
        self.creds = get_credentials()
        self.kwargs = kwargs

    def find_by_date(self, start_date, finish_date):
        events_result = (
            self.service.events()
            .list(
                calendarId="primary",
                timeMin=start_date,
                timeMax=finish_date,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        return events
    
    def take_all_meetings(self):
        pass

    def find_by_attendance(self):
        pass

    def find_one_event(self):
        pass

    def find_many_events(self):
        self.service = build("calendar", "v3", credentials=self.creds)

        if "start_date" in self.kwargs:
            start_date = datetime.datetime.strptime(self.kwargs["start_date"], "%Y-%m-%d")
            finish_date = datetime.datetime.strptime(self.kwargs["finish_date"], "%Y-%m-%d") if "finish_date" in self.kwargs else\
                                                                                                start_date + datetime.timedelta(days=1)
            start_date, finish_date = start_date.isoformat() + "Z", finish_date.isoformat() + "Z"

            events = self.find_by_date(start_date, finish_date)

        return events

        



def take_recent_events(n=10):
    """
        Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = get_credentials()

    try:
        service = build("calendar", "v3", credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
        print("Getting the upcoming 10 events")
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=n,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            print("No upcoming events found.")
            return

        # Prints the start and name of the next 10 events
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            print(start, event["summary"])

    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    take_recent_events()