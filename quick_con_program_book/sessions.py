#CONFIG
import re
import pytz
from datetime import *
LOCAL_TIMEZONE = pytz.timezone("Australia/Perth")
SLOT_LENGTH_MINUTES = 30

DAYS = [  'Monday', 
          'Tuesday', 
          'Wednesday', 
          'Thursday',  
          'Friday', 
          'Saturday',
          'Sunday']

from html.parser import HTMLParser

class HtmlResolver(HTMLParser):
    def __init__(self):
        super().__init__()
        self.result=""
        
    def handle_starttag(self, tag, attrs):
        pass
    
    def handle_endtag(self, tag):
        pass
    
    def handle_data(self, data):
        self.result+=data


def resolve_html(html_frag):
    oldtext = ""
    text = html_frag
    while text!=oldtext: #keep resolving HTML til no change
        oldtext = text
        res = HtmlResolver()
        res.feed(text)
        text = res.result
    return text




def normalise(string): 
    string = resolve_html(string)
    string = resolve_html(string)
    string = string.replace("\r",'')
    string = string.replace("\xa0", " ")
    
    string = re.sub(r"\n\s*\n", "\n", string)
        
    return string.strip()
    
def strip_titles(string):
    return re.sub(r"\b(mr|mrs|dr|ms|mx)\b\s*","",string, flags=re.I)

def load_list(csl):
    ldlst=[]
    if type(csl) is list:
        ldlst=csl
    else:
        ldlst = str.split(csl, ',')
    
    ldlst=[normalise(ll).strip().replace("\n", " ") for ll in ldlst]
    return [ll for ll in ldlst if len(ll)>0]
    
    
def parse_datetime(datetime_str):
    if type(datetime_str) is datetime:
        return datetime_str
    
    import dateutil.parser
    
    raw = dateutil.parser.parse(datetime_str)
    return raw.astimezone(LOCAL_TIMEZONE)


class session(object):
    def __init__(self, id,
                 start_time_str,end_time_str,
                 title,tags_str,people_str,
                 venues_str,description):
        self.id = int(id)
        self.start = parse_datetime(start_time_str)
        self.end = parse_datetime(end_time_str)
        self.title = normalise(title)
        self.tags = set(load_list(tags_str))
        self.people = list(map(strip_titles, load_list(people_str)))
        self.venues = set(load_list(venues_str))
        self.description = normalise(description)
    
    @property
    def day(self):
        week_days   = DAYS
        daynum = self.start.weekday()
        return week_days[daynum]
    
    
    @property
    def start_time(self):
        return self.start.strftime("%H:%M")
    
    @property
    def end_time(self):
        return self.end.strftime("%H:%M")
    
    @property
    def duration(self):
        return self.end - self.start
    
    def __str__(self):
        str(self.__dict__)
        
def load_sessions_csv(csvpath):
    import csv
    sessions = []
    with open(csvpath, 'r') as csvfile:
        con_csv = csv.reader(csvfile)
        next(con_csv) #Skip heading
        sessions = [session(*row) for row in con_csv]
    return sessions