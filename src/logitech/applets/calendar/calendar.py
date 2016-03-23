from logitech.g19 import *
from logitech.g19_keys import Key
from logitech.g19_receivers import *

import multiprocessing
import os
import tempfile
import threading
import time


import httplib2
from apiclient import discovery
from apiclient.errors import HttpError
import oauth2client
from oauth2client import client
from oauth2client import tools
import datetime
from pyrfc3339 import parse # pip install pyRFC3339
import pytz  # 3rd party: $ pip install pytz
from tzlocal import get_localzone # $ pip install tzlocal



try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = '~/.lg19/client_secret.json'
APPLICATION_NAME = 'G19'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-g19.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


class CalendarProcessor(InputProcessor):

    def __init__(self, run):
        self.__run = run

    def process_input(self, evt):
        processed = False
        
        if Key.OK in evt.keysDown:
            self.__run.selectCalendar()
            processed = True
            
        if self.__run.getMode() == 'eventview':
            if Key.SETTINGS in evt.keysDown:
                self.__run.setMode('calselect')
                processed = True
            
        if self.__run.getMode() == 'calselect':
            if Key.UP in evt.keysDown:
                self.__run.changeSelected(-1)
                processed = True
            
            if Key.DOWN in evt.keysDown:
                self.__run.changeSelected(1)
                processed = True
            
            if Key.LEFT in evt.keysDown:
                self.__run.nextSelectedPage()
                processed = True
            
            if Key.RIGHT in evt.keysDown:
                self.__run.nextSelectedPage()
                processed = True
            
        return processed

class CalendarRun(Runnable):
    '''Lists Files in the given Directory and shows them on the screen'''
    def __init__(self, lg19):
        self.__lg19 = lg19
        
        self.__lg19.load_text("Calendar", 1,True, center=True, color="yellow")
        self.__lg19.load_text("You need to open a url.", 3, center=True)
        self.__lg19.load_text("Browser will open url.", 4, center=True)
        self.__lg19.load_text("or run this in terminal", 5, center=True)
        self.__lg19.load_text("to see the url.", 6, center=True)
        self.__lg19.set_text()
        
        self.__conf = G19Config("calendar")
        try:
          self.__credentials = get_credentials()
          self.__http = self.__credentials.authorize(httplib2.Http())
          self.__service = discovery.build('calendar', 'v3', http=self.__http)
        except:
          pass
        self.__calSelectCursorPos = 0
        self.__calSelectPage = None
        self.__nextPageToken = None
        self.__calendarID = self.__conf.read("calendarID", "primary", "string")
        self.__mode = 'eventview';
        self.__updateSec = 70;
        
        Runnable.__init__(self)

    def execute(self):

        if self.__mode == 'eventview':
            if self.__updateSec > 60:
              now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
              try:
                eventsResult = self.__service.events().list(
                calendarId=self.__calendarID, timeMin=now, maxResults=5, singleEvents=True,
                orderBy='startTime').execute()
              except HttpError, err:
                if err.resp.status in [403, 500, 503]:
                  time.sleep(5)
                else: 
                  if err.resp.get('content-type', '').startswith('application/json'):
                    reason = json.loads(err.content).reason
                    print reason
                  raise
              
              events = eventsResult.get('items', [])
              self.__lg19.load_text("Calendar", 1,True, center=True, color="yellow")
              
              i = 3;
              if not events:
                  self.__lg19.load_text("No upcoming events found.", 2)
              for event in events:
                  if event['start'].get('dateTime') == None:
                      start = datetime.datetime.strptime(event['start'].get('date'),"%Y-%m-%d")
                      end = datetime.datetime.strptime(event['start'].get('date'),"%Y-%m-%d")
                      now = datetime.datetime.today()
                      prefix = " "
                      if start <= now <= end:
                          prefix = "-"
                      self.__lg19.load_text(prefix + start.strftime("%d/%m") + " " +event['summary'], i)
                  else:
                      start = parse(event['start'].get('dateTime'), utc=True)
                      end = parse(event['end'].get('dateTime'), utc=True)
                      now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
                      inhour = now + datetime.timedelta(hours=1)
                      late = now + datetime.timedelta(hours=6)
                      color = "white"
                      if start >= late:
                          color = "DarkGray"
                      if start <= inhour <= end:
                          color = "gold"
                      if start <= now <= end:
                          color = "red"
                      start = start.astimezone(get_localzone())
                      self.__lg19.load_text(start.strftime("%d/%m %H:%M") + " " +event['summary'], i, color=color)
                  i += 1
              
              self.__lg19.set_text()
              self.__updateSec = 0
            self.__updateSec += 1
            time.sleep(1)
        elif self.__mode == 'calselect':
            try:
                calendar_list = self.__service.calendarList().list(maxResults=5, pageToken=self.__calSelectPage).execute()
            except HttpError, err:
              if err.resp.status in [403, 500, 503]:
                time.sleep(5)
              else: 
                if err.resp.get('content-type', '').startswith('application/json'):
                  reason = json.loads(err.content).reason
                  print reason
                raise
            i = 3;
            self.__lg19.load_text("Select Calendar", 1,True, center=True)
            for calendar_list_entry in calendar_list['items']:
                if i-3 == self.__calSelectCursorPos:
                  self.__lg19.load_text("-> "+ calendar_list_entry['summary'], i)
                  self.__calendarID = calendar_list_entry['id'];
                else:
                  self.__lg19.load_text("   "+ calendar_list_entry['summary'], i)
                i += 1
            self.__lg19.set_text()
            self.__nextPageToken = calendar_list.get('nextPageToken');
            time.sleep(0.5)
            
    def changeSelected(self, direction):
        self.__calSelectCursorPos = (self.__calSelectCursorPos + direction)%5;
        
    def nextSelectedPage(self):
        pagetoken = self.__nextPageToken;
        if not pagetoken:
            pagetoken = None
        self.__calSelectPage = pagetoken;
        
    def selectCalendar(self):
        self.__conf.write("calendarID", self.__calendarID)
        self.__updateSec = 70;
        self.setMode('eventview');
        
    def setMode(self, mode):
        self.__mode = mode
    
    def getMode(self):
        return self.__mode;

class calendar(object):

    def __init__(self, lg19):
        self.__lg19 = lg19
        self.__calendarrun = CalendarRun(self.__lg19)
        self.__inputProcessor = CalendarProcessor(self.__calendarrun)
        self.start()
    
    def get_input_processor(self):
        return self.__inputProcessor
    
    def start(self):
        t = threading.Thread(target=self.__calendarrun.run)
        t.start()
        pass
    
    def stop(self):
        self.__calendarrun.stop()
        pass;

