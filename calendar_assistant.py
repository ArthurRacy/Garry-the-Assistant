import os.path
import pickle
import openai
import datetime
import pytz
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from chatgpt_function import generate_chatgpt_response
SCOPES = ['https://www.googleapis.com/auth/calendar']



def create_event(service, event_details):
    event = {
        'summary': event_details['summary'],
        'start': {
            'dateTime': event_details['start_time'],
            'timeZone': event_details['timezone'],
        },
        'end': {
            'dateTime': event_details['end_time'],
            'timeZone': event_details['timezone'],
        },
        'attendees': event_details['attendees'],
        'reminders': {
            'useDefault': True
        },
    }
    calendar_id = 'primary'
    event = service.events().insert(calendarId=calendar_id, body=event).execute()
    print(f'Event created: {event.get("htmlLink")}')


def get_calendar_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:  
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('calendar', 'v3', credentials=creds)


def parse_meeting_details(meeting_text):
    prompt = f"Extrair detalhes da reunião do seguinte texto: \"{meeting_text}\""
    chatgpt_response = generate_chatgpt_response(prompt)


    return chatgpt_response


def main():
    print("Bem-vindo ao Assistente de Reuniões do Google Calendar!")

    service = get_calendar_service()

    while True:
        print("\nDigite o texto com os detalhes da reunião ou digite 'sair' para encerrar:")
        meeting_text = input()

        if meeting_text.lower() == "sair":
            break

        meeting_details = parse_meeting_details(meeting_text)
 
        # A função parse_meeting_details deve ser aprimorada para extrair informações
        # relevantes da resposta do ChatGPT. Por enquanto, vamos supor que a resposta
        # contém informações suficientes para criar o evento no Google Calendar.

        event_details = {
            'summary': meeting_details,
            'start_time': datetime.datetime.utcnow().isoformat() + 'Z', # Exemplo: data e hora de início em UTC
            'end_time': (datetime.datetime.utcnow() + datetime.timedelta(hours=1)).isoformat() + 'Z', # Exemplo: data e hora de término em UTC
            'timezone': 'UTC',
            'attendees': [],
        }

        create_event(service, event_details)

if __name__ == "__main__":
    main()
