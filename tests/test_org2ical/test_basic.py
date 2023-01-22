import textwrap

import dateutil.tz

from .utils import compare, iCalEntry


def test_scheduled():
    org_str = textwrap.dedent("""\
    Lorem ipsum
    * Scheduled
    SCHEDULED: <2022-01-01 Sat>
    * TODO Scheduled Todo
    SCHEDULED: <2022-01-01 Sat>
    schedule
    * TODO Scheduled Time Todo
    SCHEDULED: <2022-01-01 Sat 10:00>
    * TODO Repeated Scheduled Todo
    SCHEDULED: <2022-01-01 Sat 10:00 +2w>
    * TODO Repeated Scheduled Todo
    SCHEDULED: <2022-01-01 Sat 10:00 .+2w>
    * TODO Repeated Scheduled Todo
    SCHEDULED: <2022-01-01 Sat 10:00 ++2w>
    * DONE Schedule Done
    CLOSED: [2022-02-01 Tue 00:00] SCHEDULED: <2022-02-01 Tue>
    * CANCELED Schedule Cancelled
    CLOSED: [2022-02-01 Tue 00:00] SCHEDULED: <2022-02-01 Tue>
    * DONE Repeated Scheduled Done
    SCHEDULED: <2022-01-01 Sat 10:00 +2w>
    * TODO Scheduled Todo Archived :ARCHIVE:
    SCHEDULED: <2022-01-01 Sat>
    """)
    icals = [
        iCalEntry("2022-01-01", None, "Scheduled", "", "SCHEDULED"),
        iCalEntry("2022-01-01", None, "Scheduled Todo", "schedule", "SCHEDULED"),
        iCalEntry("2022-01-01 10:00:00+00:00", None, "Scheduled Time Todo", "", "SCHEDULED"),
        iCalEntry("2022-01-01 10:00:00+00:00", None, "Repeated Scheduled Todo", "", "SCHEDULED", "FREQ=WEEKLY;INTERVAL=2"),
        iCalEntry("2022-01-01 10:00:00+00:00", None, "Repeated Scheduled Todo", "", "SCHEDULED", "FREQ=WEEKLY;INTERVAL=2"),
        iCalEntry("2022-01-01 10:00:00+00:00", None, "Repeated Scheduled Todo", "", "SCHEDULED", "FREQ=WEEKLY;INTERVAL=2"),
    ]
    compare(org_str, icals)
    compare(org_str, icals, include_types={"SCHEDULED"})
    compare(org_str, [], ignore_states={"DONE", "CANCELED", None, "TODO"})
    compare(org_str, [], include_types=set())

def test_deadline():
    org_str = textwrap.dedent("""\
    Lorem ipsum
    * Deadline
    DEADLINE: <2022-01-01 Sat>
    * TODO Deadline Todo
    DEADLINE: <2022-01-01 Sat>
    deadline
    * TODO Deadline Time Todo
    DEADLINE: <2022-01-01 Sat 10:00>
    * TODO Repeated Deadline Todo
    DEADLINE: <2022-01-01 Sat 10:00 +2w>
    * TODO Repeated Deadline Todo
    DEADLINE: <2022-01-01 Sat 10:00 .+2w>
    * TODO Repeated Deadline Todo
    DEADLINE: <2022-01-01 Sat 10:00 ++2w>
    * DONE Deadline Done
    CLOSED: [2022-02-01 Tue 00:00] DEADLINE: <2022-02-01 Tue>
    * CANCELED Deadline Cancelled
    CLOSED: [2022-02-01 Tue 00:00] DEADLINE: <2022-02-01 Tue>
    * DONE Repeated Deadline Done
    DEADLINE: <2022-01-01 Sat 10:00 +2w>
    * TODO Deadline Todo Archived :ARCHIVE:
    DEADLINE: <2022-01-01 Sat>
    """)
    icals = [
        iCalEntry("2022-01-01", None, "Deadline", "", "DEADLINE"),
        iCalEntry("2022-01-01", None, "Deadline Todo", "deadline", "DEADLINE"),
        iCalEntry("2022-01-01 10:00:00+00:00", None, "Deadline Time Todo", "", "DEADLINE"),
        iCalEntry("2022-01-01 10:00:00+00:00", None, "Repeated Deadline Todo", "", "DEADLINE", "FREQ=WEEKLY;INTERVAL=2"),
        iCalEntry("2022-01-01 10:00:00+00:00", None, "Repeated Deadline Todo", "", "DEADLINE", "FREQ=WEEKLY;INTERVAL=2"),
        iCalEntry("2022-01-01 10:00:00+00:00", None, "Repeated Deadline Todo", "", "DEADLINE", "FREQ=WEEKLY;INTERVAL=2"),
    ]
    compare(org_str, icals)
    compare(org_str, icals, include_types={"DEADLINE"})
    compare(org_str, [], ignore_states={"DONE", "CANCELED", None, "TODO"})
    compare(org_str, [], include_types=set())

def test_timestamp():
    org_str = textwrap.dedent("""\
    Lorem ipsum
    * Timestamp
    <2022-01-01 Sat>
    * TODO Timestamp Todo
    <2022-01-01 Sat>
    timestamp
    * TODO Timestamp Time Todo
    <2022-01-01 Sat 10:00>
    * TODO Timestamp Date Range Todo
    <2022-01-01 Sat>--<2022-01-08 Sat>
    * TODO Timestamp Time Range Todo
    <2022-01-01 Sat 10:00>--<2022-01-08 Sat 11:00>
    * TODO Timestamp Time Range in Day Todo
    <2022-01-01 Sat 10:00-11:00>
    * TODO Repeated Timestamp Todo
    <2022-01-01 Sat 20:00-22:00 +1w>
    * TODO Repeated Timestamp Todo Done Once
    :PROPERTIES:
    :LAST_REPEAT: [2022-01-26 Wed 22:00]
    :END:
    - State "DONE"       from "TODO"       [2022-01-26 Wed 22:00]
    <2022-02-02 Wed 20:00-22:00 +1w>
    * TODO Repeated Timestamp Todo Cancelled Once
    :PROPERTIES:
    :LAST_REPEAT: [2022-01-26 Wed 22:00]
    :END:
    - State "CANCELED"   from "TODO"       [2022-01-26 Wed 22:00]
    <2022-02-02 Wed 20:00-22:00 +1w>
    * DONE Timestamp Done
    CLOSED: [2022-02-01 Tue 00:00]
    <2022-01-01 Sat>
    * CANCELED Timestamp Cancelled
    CLOSED: [2022-02-01 Tue 00:00]
    <2022-01-01 Sat>
    * DONE Repeated Timestamp Done
    :PROPERTIES:
    :LAST_REPEAT: [2022-01-26 Wed 22:00]
    :END:
    - State "DONE"       from "TODO"       [2022-01-26 Wed 22:00]
    <2022-02-02 Wed 20:00-22:00 +1w>
    * CANCELED Repeated Timestamp Cancelled
    :PROPERTIES:
    :LAST_REPEAT: [2022-01-26 Wed 22:00]
    :END:
    - State "CANCELED"   from "TODO"       [2022-01-26 Wed 22:00]
    <2022-02-02 Wed 20:00-22:00 +1w>
    * TODO Timestamp Todo Archived :ARCHIVE:
    <2022-01-01 Sat>
    * TODO Timestamp Todo Inactive
    [2022-01-01 Sat]
    """)
    icals = [
        iCalEntry("2022-01-01", None, "Timestamp", "<2022-01-01 Sat>", "TIMESTAMP"),
        iCalEntry("2022-01-01", None, "Timestamp Todo", "<2022-01-01 Sat>\ntimestamp", "TIMESTAMP"),
        iCalEntry("2022-01-01 10:00:00+00:00", None, "Timestamp Time Todo", "<2022-01-01 Sat 10:00>", "TIMESTAMP"),
        iCalEntry("2022-01-01", "2022-01-08 23:59:59+00:00", "Timestamp Date Range Todo", "<2022-01-01 Sat>--<2022-01-08 Sat>", "TIMESTAMP"),
        iCalEntry("2022-01-01 10:00:00+00:00", "2022-01-08 11:00:00+00:00", "Timestamp Time Range Todo", "<2022-01-01 Sat 10:00>--<2022-01-08 Sat 11:00>", "TIMESTAMP"),
        iCalEntry("2022-01-01 10:00:00+00:00", "2022-01-01 11:00:00+00:00", "Timestamp Time Range in Day Todo", "<2022-01-01 Sat 10:00-11:00>", "TIMESTAMP"),
        iCalEntry("2022-01-01 20:00:00+00:00", "2022-01-01 22:00:00+00:00", "Repeated Timestamp Todo", "<2022-01-01 Sat 20:00-22:00 +1w>", "TIMESTAMP", "FREQ=WEEKLY;INTERVAL=1"),
        iCalEntry("2022-02-02 20:00:00+00:00", "2022-02-02 22:00:00+00:00", "Repeated Timestamp Todo Done Once", "<2022-02-02 Wed 20:00-22:00 +1w>", "TIMESTAMP", "FREQ=WEEKLY;INTERVAL=1"),
        iCalEntry("2022-02-02 20:00:00+00:00", "2022-02-02 22:00:00+00:00", "Repeated Timestamp Todo Cancelled Once", "<2022-02-02 Wed 20:00-22:00 +1w>", "TIMESTAMP", "FREQ=WEEKLY;INTERVAL=1"),
    ]
    compare(org_str, icals)
    compare(org_str, icals, include_types={"TIMESTAMP"})
    compare(org_str, [], ignore_states={"DONE", "CANCELED", None, "TODO"})
    compare(org_str, [], include_types=set())

def test_clock():
    org_str = textwrap.dedent("""\
    Lorem ipsum
    * Clock
    :LOGBOOK:
    CLOCK: [2022-01-01 Sat 00:00]--[2022-01-01 Sat 01:11] =>  1:11
    :END:
    * TODO Clock Todo
    :LOGBOOK:
    CLOCK: [2022-01-01 Sat 00:00]--[2022-01-01 Sat 01:11] =>  1:11
    :END:
    * DONE Clock Done
    CLOSED: [2022-02-02 Wed 02:00]
    :PROPERTIES:
    :Effort:   2h
    :END:
    :LOGBOOK:
    CLOCK: [2022-02-02 Wed 00:00]--[2022-02-02 Wed 02:22] =>  2:22
    :END:
    * CANCELED Clock Cancelled
    CLOSED: [2022-02-02 Wed 02:00]
    :PROPERTIES:
    :Effort:   2h
    :END:
    :LOGBOOK:
    CLOCK: [2022-02-02 Wed 00:00]--[2022-02-02 Wed 02:22] =>  2:22
    :END:
    * TODO Clock Todo Archived :ARCHIVE:
    :LOGBOOK:
    CLOCK: [2022-01-01 Sat 00:00]--[2022-01-01 Sat 01:11] =>  1:11
    :END:
    """)
    icals = [
        # The LOGBOOK drawer can be removed after the issue in orgparse is resolved:
        # Link: https://github.com/karlicoss/orgparse/issues/59
        iCalEntry("2022-01-01 00:00:00+00:00", "2022-01-01 01:11:00+00:00", "Clock", ":LOGBOOK:\n:END:", "CLOCK"),
        iCalEntry("2022-01-01 00:00:00+00:00", "2022-01-01 01:11:00+00:00", "Clock Todo", ":LOGBOOK:\n:END:", "CLOCK"),
    ]
    compare(org_str, [])
    compare(org_str, icals, include_types={"CLOCK"})
    compare(org_str, [], ignore_states={"DONE", "CANCELED", None, "TODO"}, include_types={"CLOCK"})

def test_mixed():
    org_str = textwrap.dedent("""\
    Lorem ipsum
    * Parent
    ** Child
    SCHEDULED: <2022-01-01 Sat> DEADLINE: <2022-01-01 Sat>
    <2022-01-01 Sat>
    CLOCK: [2022-01-01 Sat 00:00]--[2022-01-01 Sat 01:11] =>  1:11
    <2022-01-02 Sun>
    CLOCK: [2022-01-02 Sun 00:00]--[2022-01-02 Sun 01:11] =>  1:11
    """)
    icals = [
        iCalEntry("2022-01-01", None, "Child", "<2022-01-01 Sat>\n<2022-01-02 Sun>", "SCHEDULED", parents=["Parent"]),
        iCalEntry("2022-01-01", None, "Child", "<2022-01-01 Sat>\n<2022-01-02 Sun>", "DEADLINE", parents=["Parent"]),
        iCalEntry("2022-01-01", None, "Child", "<2022-01-01 Sat>\n<2022-01-02 Sun>", "TIMESTAMP", parents=["Parent"]),
        iCalEntry("2022-01-02", None, "Child", "<2022-01-01 Sat>\n<2022-01-02 Sun>", "TIMESTAMP", parents=["Parent"]),
        iCalEntry("2022-01-01 00:00:00+00:00", "2022-01-01 01:11:00+00:00", "Child", "<2022-01-01 Sat>\n<2022-01-02 Sun>", "CLOCK", parents=["Parent"]),
        iCalEntry("2022-01-02 00:00:00+00:00", "2022-01-02 01:11:00+00:00", "Child", "<2022-01-01 Sat>\n<2022-01-02 Sun>", "CLOCK", parents=["Parent"]),
    ]
    compare(org_str, icals, include_types={"DEADLINE", "SCHEDULED", "TIMESTAMP", "CLOCK"})

def test_next():
    org_str = textwrap.dedent("""\
    * NEXT Entry
    SCHEDULED: <2022-01-01 Sat> DEADLINE: <2022-01-01 Sat>
    """)
    icals = [
        iCalEntry("2022-01-01", None, "NEXT Entry", "", "SCHEDULED"),
        iCalEntry("2022-01-01", None, "NEXT Entry", "", "DEADLINE"),
    ]
    compare(org_str, icals)
    compare(org_str, [], ignore_states={None})
    compare(org_str, [], ignore_states={"NEXT"})

def test_timezone():
    org_str = textwrap.dedent("""\
    * Entry
    SCHEDULED: <2022-01-01 Sat 10:00>
    """)
    # UTC -> UTC
    icals = [
        iCalEntry("2022-01-01 10:00:00+00:00", None, "Entry", "", "SCHEDULED"),
    ]
    compare(org_str, icals)
    # UTC -> UTC+8
    icals = [
        iCalEntry("2022-01-01 02:00:00+00:00", None, "Entry", "", "SCHEDULED"),
    ]
    compare(org_str, icals, to_tz=dateutil.tz.gettz('Asia/Taipei'))
    # UTC+8 -> UTC
    icals = [
        iCalEntry("2022-01-01 18:00:00+00:00", None, "Entry", "", "SCHEDULED"),
    ]
    compare(org_str, icals, from_tz=dateutil.tz.gettz("Asia/Taipei"))
    # UTC+8 -> UTC+9
    icals = [
        iCalEntry("2022-01-01 09:00:00+00:00", None, "Entry", "", "SCHEDULED"),
    ]
    compare(org_str, icals,
            from_tz=dateutil.tz.gettz("Asia/Taipei"),
            to_tz=dateutil.tz.gettz('Asia/Tokyo'))
    # Don't use pytz for tests, see:
    # - https://stackoverflow.com/a/48566388
    # - https://stackoverflow.com/q/11473721
