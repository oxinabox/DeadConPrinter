def get_slots(start,end, slot_length_minutes=30, exclusive_end=True):
    from dateutil import rrule
    from datetime import timedelta
    until = end-timedelta(0,0,1) if exclusive_end else end
    slots = rrule.rrule(rrule.MINUTELY, 
                          interval = slot_length_minutes,
                          dtstart = start,
                          until = until,
                          )
    return list(slots)

def get_sesson_slots(session, slot_length_minutes):
    return get_slots(session.start, session.end, slot_length_minutes)

    
class SessionOutOfSlotAlignmentError(Exception):
    def __init__(self, slot, day):
        self.slot=slot
        self.day=day
        

def get_day_venue_timeslots(sessions, slot_length_minutes=30):
    from collections import defaultdict
    from defaultordereddict import DefaultOrderedDict
    dtv_bookings = DefaultOrderedDict(lambda : defaultdict(lambda : defaultdict(str)))

    import random

    for session in sessions:
        for venue in session.venues:
            session_timeslots = get_sesson_slots(session, slot_length_minutes)
            colorstring = "\cellcolor[gray]{%f} " % (0.5+0.5*random.random()) #HACK
            dtv_bookings[session.day][session_timeslots[0]][venue] = colorstring + session.title
            for slot in session_timeslots[1:]:
                dtv_bookings[session.day][slot][venue] =colorstring + "...cont..."
    return dtv_bookings

def write_timetable(sessions, doc, slot_length_minutes):
    from pylatex import Section, Subsection, Table, Package
    from pylatex.command import Command
    from pagelayout import Landscape
    from venueordering import get_order_from_sessions

    doc.packages.append(Package('xcolor', options=['table']))
    venue_columns = get_order_from_sessions(sessions)
    
    dtv_bookings = get_day_venue_timeslots(sessions, slot_length_minutes)
    
    with doc.create(Landscape()):
        with doc.create(Section('Timetable',numbering=False)):
            for day in dtv_bookings.keys():
                if len(dtv_bookings[day])>0:
                    with doc.create(Subsection(day, numbering=False)):
                        table_spec = "c||"+"p{25mm}|"*len(venue_columns)
                        doc.append(Command('tiny'))
                        with doc.create(Table(table_spec)) as timetable:
                            timetable.add_row(["Time"]+venue_columns)
                            timetable.add_hline()
                            timetable.add_hline()

                            used_slots = set(dict.keys(dtv_bookings[day]))
                            slots = get_slots(min(used_slots),max(used_slots), slot_length_minutes, False)

                            for used_slot in used_slots:
                                if not used_slot in slots:
                                    raise SessionOutOfSlotAlignmentError(used_slot,day)

                            for slot in slots:
                                venue_bookings = dtv_bookings[day][slot]
                                venue_slots = [venue_bookings[vv] for vv in venue_columns]

                                slot_time_str = slot.strftime("%H:%M")
                                timetable.add_row([slot_time_str] + venue_slots)
    
