import venueordering


def get_tag_colors_auto(sessions):
        from collections import defaultdict
        tag_occurances = defaultdict(lambda: 0)
        for session in sessions:
            for tag in session.tags:
                tag_occurances[tag]+=1

        tags = list(tag_occurances)
        tags.sort(key=lambda tt: -tag_occurances[tt])

        colors=["blue","brown","cyan","green","lime","magenta","olive","orange","pink","purple","red","teal","violet", "yellow"]
        color_map = {tag:color for tag,color in zip(tags,colors)}
        return color_map



def get_tag_colors_people(sessions):
    return {' Needs Moderator': 'green',
    ' Needs Panelists': 'red'}




def get_tag_colors_mono(sessions):
    return {}


def get_tag_colors_manual(sessions):
    return {
        "Anime" : "Maroon",
        "Art" : "Lime",
        "Comics" : "Pink",
        "Core" : "SlateGray",
        "Creative Works" : "PaleGreen",
        "discussion" : "SlateBlue",
        "Fandom/Conrunning" : "Teal",
        "Fantasy" : "Wheat",
        "Gaming" : "Green",
        "Horror" : "DarkGreen",
        "Science and Tech" : "Chocolate",
        "Scifi" : "Salmon",
        "TV/Movies" : "LightBlue",
        "Written Fiction" : "Coral",
        "a launch in five parts" : "DarkViolet",
        "Academic" : "Gold",
        "AdultsOnly" : "HotPink",
        "Family" : "Cornsilk",
        "Lightning (series of 3 minute)" : "Yellow",
        "Loud" : "SaddleBrown",
        "Music" : "Violet",
        "Video Games" : "SeaGreen",
        "Video Games (outside the gamesroom)" : "CadetBlue",
        "workshop " : "RoyalBlue"
    }


def with_units(func):
    def wrapper(*args, **kwargs):
        units = args[0].units #Assumes that this is decorating a method on a class with a units field
        result = func(*args, **kwargs)
        return str(round(result,3))+units
    return wrapper
    
class timetable_metric_solver(object):
   
    def __init__(self,sessions, hour_len, venue_width, units, 
                 overlap=0, #Set this to the line thickness to allow overlap. It is excluded from position calculations
                 voffset=0,             
                 venue_orderer = venueordering.get_order_from_sessions,
                 get_tag_colors = get_tag_colors_auto):
        
        
        self.voffset = voffset
        self.overlap=overlap
        self.hour_len = hour_len
        self.venue_width = venue_width
        self.units = units
        
        self.venues_to_x = { name:ii*venue_width
                                for ii, name in enumerate(venue_orderer(sessions))}
        
        from itertools import groupby
        self.day_starts = {date:min(map(lambda ss: ss.start, sessions))
                                for date, sessions in groupby(sessions, lambda ss: ss.start.date())}
        self.tag_colors = get_tag_colors(sessions)
    
    def get_color(self,session):
        if session.tags:
            colored_tags = set.intersection( set(session.tags), set(self.tag_colors.keys()) )
            if len(colored_tags)>0:
                mix = round(70/len(colored_tags)) #paleness
                colors = [self.tag_colors[tag]+ "!%s!" % mix 
                              for tag in colored_tags]
                return ''.join(colors)+"white"
            else:
                return ""
        else:
            return ""
        
    
    @with_units
    def get_width(self,session):
        if session.venues:
            nVenues = len(session.venues)
        else:
            nVenues = len(self.venues_to_x.keys())
            
        return nVenues*self.venue_width + self.overlap   
    
    @with_units
    def get_venue_x(self,venue):
        return self.venues_to_x[venue]
    
    @with_units
    def get_x(self, session):
        #Get the left most venue position
        if session.venues:
            return min(map(lambda vv: self.venues_to_x[vv],session.venues))
        else:
            return 0 # fills all Venues, starting from left
            
    
    def duration_to_height(self,duration):
        return duration.seconds/(60*60)*self.hour_len
    
    @with_units
    def get_y(self, session):
        day_start = self.day_starts[session.start.date()]
        time_til_start = session.start - day_start
        return self.voffset + self.duration_to_height(time_til_start)
    
    @with_units
    def get_height(self,session):
        return self.duration_to_height(session.duration) + self.overlap
    
    @with_units
    def get_venue_width(self):
        return self.venue_width + self.overlap
    
    @property
    def venues(self):
        return list(self.venues_to_x.keys())
    
    