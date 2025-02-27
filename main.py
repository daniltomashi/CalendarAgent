from google_calendar import GoogleCalendarSearch
from agent import answer



if __name__ == "__main__":
    # take_recent_events()

    prompt = ""
    
    # # based on the prompt generate conditions to search events in Google Calendar
    # conditions = answer(prompt)
    # for test we are using predefined conditions
    conditions = {"date": "2025-02-27"}

    # initialize object for Google Calendar class
    google_calendar_search = GoogleCalendarSearch(**conditions)

    # find all events with specific conditions
    events = google_calendar_search.find_many_events()

    for event in events:
        description = event["description"]
        created = event["created"]
        summary = event["summary"]
        attendees = event["attendees"]
        
        print(description)
        print(created)
        print(summary)
        print(attendees)
        
        break