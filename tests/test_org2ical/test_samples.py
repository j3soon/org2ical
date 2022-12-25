"""
Test samples found online
"""

import textwrap

from .utils import iCalEntry, compare


# Ref: https://orgmode.org/manual/Deadlines-and-Scheduling.html
def test_Deadlines_and_Scheduling():
    org_str = textwrap.dedent("""\
    *** TODO write article about the Earth for the Guide
        DEADLINE: <2004-02-29 Sun>
        The editor in charge is [[bbdb:Ford Prefect]]
    *** TODO Call Trillian for a date on New Years Eve.
        SCHEDULED: <2004-12-25 Sat>
    """)
    icals = [
        iCalEntry("2004-02-29", None, "write article about the Earth for the Guide", "    The editor in charge is bbdb:Ford Prefect", "DEADLINE"),
        iCalEntry("2004-12-25", None, "Call Trillian for a date on New Years Eve.", "", "SCHEDULED"),
    ]
    compare(org_str, icals)

# Ref: https://orgmode.org/manual/Clocking-Work-Time.html
def test_Clocking_Work_Time():
    pass

# Ref: https://orgmode.org/manual/Timestamps.html
def test_Timestamps():
    org_str = textwrap.dedent("""\
    * Meet Peter at the movies
      <2006-11-01 Wed 19:15>
    * Discussion on climate change
      <2006-11-02 Thu 20:00-22:00>
    * Pick up Sam at school
      <2007-05-16 Wed 12:30 +1w>
    * Meetings
    ** Meeting in Amsterdam
       <2004-08-23 Mon>--<2004-08-26 Thu>
    * Gillian comes late for the fifth time
      [2006-11-01 Wed]
    """)
    icals = [
        iCalEntry("2006-11-01 19:15:00+00:00", None, "Meet Peter at the movies", "  <2006-11-01 Wed 19:15>", "TIMESTAMP"),
        iCalEntry("2006-11-02 20:00:00+00:00", "2006-11-02 22:00:00+00:00", "Discussion on climate change", "  <2006-11-02 Thu 20:00-22:00>", "TIMESTAMP"),
        iCalEntry("2007-05-16 12:30:00+00:00", None, "Pick up Sam at school", "  <2007-05-16 Wed 12:30 +1w>", "TIMESTAMP", "FREQ=WEEKLY;INTERVAL=1"),
        iCalEntry("2004-08-23", "2004-08-26 23:59:59+00:00", "Meeting in Amsterdam", "   <2004-08-23 Mon>--<2004-08-26 Thu>", "TIMESTAMP", parents=["Meetings"]),
    ]
    compare(org_str, icals)

# Ref: https://orgmode.org/manual/Repeated-tasks.html
def test_Repeated_tasks():
    org_str = textwrap.dedent("""\
    * My Todos
    ** TODO Pay the rent
       DEADLINE: <2005-10-01 Sat +1m>
    ** TODO Pay the rent (with warning)
       DEADLINE: <2005-10-01 Sat +1m -3d>
    ** TODO Pay the rent
       DEADLINE: <2005-11-01 Tue +1m>
    ** TODO Call Father
       DEADLINE: <2008-02-10 Sun ++1w>
       Marking this DONE shifts the date by at least one week, but also
       by as many weeks as it takes to get this date into the future.
       However, it stays on a Sunday, even if you called and marked it
       done on Saturday.
    ** TODO Empty kitchen trash
       DEADLINE: <2008-02-08 Fri 20:00 ++1d>
       Marking this DONE shifts the date by at least one day, and also
       by as many days as it takes to get the timestamp into the future.
       Since there is a time in the timestamp, the next deadline in the
       future will be on today's date if you complete the task before
       20:00.
    ** TODO Check the batteries in the smoke detectors
       DEADLINE: <2005-11-01 Tue .+1m>
       Marking this DONE shifts the date to one month after today.
    ** TODO Wash my hands
       DEADLINE: <2019-04-05 08:00 Fri .+1h>
       Marking this DONE shifts the date to exactly one hour from now
    """)
    icals = [
        iCalEntry("2005-10-01", None, "Pay the rent", "", "DEADLINE", "FREQ=MONTHLY;INTERVAL=1", parents=["My Todos"]),
        iCalEntry("2005-10-01", None, "Pay the rent (with warning)", "", "DEADLINE", "FREQ=MONTHLY;INTERVAL=1", parents=["My Todos"]),
        iCalEntry("2005-11-01", None, "Pay the rent", "", "DEADLINE", "FREQ=MONTHLY;INTERVAL=1", parents=["My Todos"]),
        iCalEntry("2008-02-10", None, "Call Father", """\
   Marking this DONE shifts the date by at least one week, but also
   by as many weeks as it takes to get this date into the future.
   However, it stays on a Sunday, even if you called and marked it
   done on Saturday.""", "DEADLINE", "FREQ=WEEKLY;INTERVAL=1", parents=["My Todos"]),
        iCalEntry("2008-02-08 20:00:00+00:00", None, "Empty kitchen trash", """\
   Marking this DONE shifts the date by at least one day, and also
   by as many days as it takes to get the timestamp into the future.
   Since there is a time in the timestamp, the next deadline in the
   future will be on today's date if you complete the task before
   20:00.""", "DEADLINE", "FREQ=DAILY;INTERVAL=1", parents=["My Todos"]),
        iCalEntry("2005-11-01", None, "Check the batteries in the smoke detectors", "   Marking this DONE shifts the date to one month after today.", "DEADLINE", "FREQ=MONTHLY;INTERVAL=1", parents=["My Todos"]),
        iCalEntry("2019-04-05 08:00:00+00:00", None, "Wash my hands", "   Marking this DONE shifts the date to exactly one hour from now", "DEADLINE", "FREQ=HOURLY;INTERVAL=1", parents=["My Todos"]),
    ]
    compare(org_str, icals)
