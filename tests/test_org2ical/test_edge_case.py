import textwrap

from .utils import compare, iCalEntry

def test_scheduled_space_deadline():
    org_str = textwrap.dedent("""\
    * Entry
    SCHEDULED: <2022-01-01 Sat> DEADLINE: <2022-01-01 Sat>
    <2022-01-01 Sat>
    CLOCK: [2022-01-01 Sat 00:00]--[2022-01-01 Sat 01:11] =>  1:11
    """)
    icals = [
        iCalEntry("2022-01-01", None, "Entry", "<2022-01-01 Sat>", "SCHEDULED"),
        iCalEntry("2022-01-01", None, "Entry", "<2022-01-01 Sat>", "DEADLINE"),
        iCalEntry("2022-01-01", None, "Entry", "<2022-01-01 Sat>", "TIMESTAMP"),
        iCalEntry("2022-01-01 00:00:00+00:00", "2022-01-01 01:11:00+00:00", "Entry", "<2022-01-01 Sat>", "CLOCK"),
    ]
    compare(org_str, icals, include_types={"DEADLINE", "SCHEDULED", "TIMESTAMP", "CLOCK"})

def test_deadline_space_scheduled():
    org_str = textwrap.dedent("""\
    * Entry
    DEADLINE: <2022-01-01 Sat> SCHEDULED: <2022-01-01 Sat>
    <2022-01-01 Sat>
    CLOCK: [2022-01-01 Sat 00:00]--[2022-01-01 Sat 01:11] =>  1:11
    """)
    icals = [
        iCalEntry("2022-01-01", None, "Entry", "<2022-01-01 Sat>", "SCHEDULED"),
        iCalEntry("2022-01-01", None, "Entry", "<2022-01-01 Sat>", "DEADLINE"),
        iCalEntry("2022-01-01", None, "Entry", "<2022-01-01 Sat>", "TIMESTAMP"),
        iCalEntry("2022-01-01 00:00:00+00:00", "2022-01-01 01:11:00+00:00", "Entry", "<2022-01-01 Sat>", "CLOCK"),
    ]
    compare(org_str, icals, include_types={"DEADLINE", "SCHEDULED", "TIMESTAMP", "CLOCK"})

def test_scheduled_newline_deadline():
    org_str = textwrap.dedent("""\
    * Entry
    SCHEDULED: <2022-01-01 Sat>
    DEADLINE: <2022-01-01 Sat>
    <2022-01-01 Sat>
    CLOCK: [2022-01-01 Sat 00:00]--[2022-01-01 Sat 01:11] =>  1:11
    """)
    icals = [
        iCalEntry("2022-01-01", None, "Entry", "DEADLINE: <2022-01-01 Sat>\n<2022-01-01 Sat>", "SCHEDULED"),
        # No deadline
        iCalEntry("2022-01-01", None, "Entry", "DEADLINE: <2022-01-01 Sat>\n<2022-01-01 Sat>", "TIMESTAMP"),
        iCalEntry("2022-01-01", None, "Entry", "DEADLINE: <2022-01-01 Sat>\n<2022-01-01 Sat>", "TIMESTAMP"),
        iCalEntry("2022-01-01 00:00:00+00:00", "2022-01-01 01:11:00+00:00", "Entry", "DEADLINE: <2022-01-01 Sat>\n<2022-01-01 Sat>", "CLOCK"),
    ]
    compare(org_str, icals, include_types={"DEADLINE", "SCHEDULED", "TIMESTAMP", "CLOCK"},
            warnings=["WARNING: DEADLINE keyword found but no timestamp in node: `Entry`."])

def test_deadline_newline_scheduled():
    org_str = textwrap.dedent("""\
    * Entry
    DEADLINE: <2022-01-01 Sat>
    SCHEDULED: <2022-01-01 Sat>
    <2022-01-01 Sat>
    CLOCK: [2022-01-01 Sat 00:00]--[2022-01-01 Sat 01:11] =>  1:11
    """)
    icals = [
        iCalEntry("2022-01-01", None, "Entry", "SCHEDULED: <2022-01-01 Sat>\n<2022-01-01 Sat>", "DEADLINE"),
        # No scheduled
        iCalEntry("2022-01-01", None, "Entry", "SCHEDULED: <2022-01-01 Sat>\n<2022-01-01 Sat>", "TIMESTAMP"),
        iCalEntry("2022-01-01", None, "Entry", "SCHEDULED: <2022-01-01 Sat>\n<2022-01-01 Sat>", "TIMESTAMP"),
        iCalEntry("2022-01-01 00:00:00+00:00", "2022-01-01 01:11:00+00:00", "Entry", "SCHEDULED: <2022-01-01 Sat>\n<2022-01-01 Sat>", "CLOCK"),
    ]
    compare(org_str, icals, include_types={"DEADLINE", "SCHEDULED", "TIMESTAMP", "CLOCK"},
            warnings=["WARNING: SCHEDULED keyword found but no timestamp in node: `Entry`."])

def test_deadline_newline_scheduled():
    org_str = textwrap.dedent("""\
    * Entry
    Lorem ipsum
    SCHEDULED: <2022-01-01 Sat>
    DEADLINE: <2022-01-01 Sat>
    <2022-01-01 Sat>
    CLOCK: [2022-01-01 Sat 00:00]--[2022-01-01 Sat 01:11] =>  1:11
    """)
    icals = [
        # No scheduled
        # No deadline
        iCalEntry("2022-01-01", None, "Entry", "Lorem ipsum\nSCHEDULED: <2022-01-01 Sat>\nDEADLINE: <2022-01-01 Sat>\n<2022-01-01 Sat>", "TIMESTAMP"),
        iCalEntry("2022-01-01", None, "Entry", "Lorem ipsum\nSCHEDULED: <2022-01-01 Sat>\nDEADLINE: <2022-01-01 Sat>\n<2022-01-01 Sat>", "TIMESTAMP"),
        iCalEntry("2022-01-01", None, "Entry", "Lorem ipsum\nSCHEDULED: <2022-01-01 Sat>\nDEADLINE: <2022-01-01 Sat>\n<2022-01-01 Sat>", "TIMESTAMP"),
        iCalEntry("2022-01-01 00:00:00+00:00", "2022-01-01 01:11:00+00:00", "Entry", "Lorem ipsum\nSCHEDULED: <2022-01-01 Sat>\nDEADLINE: <2022-01-01 Sat>\n<2022-01-01 Sat>", "CLOCK"),
    ]
    compare(org_str, icals, include_types={"DEADLINE", "SCHEDULED", "TIMESTAMP", "CLOCK"},
            warnings=["WARNING: SCHEDULED keyword found but no timestamp in node: `Entry`.",
                      "WARNING: DEADLINE keyword found but no timestamp in node: `Entry`."])

def test_scheduled2():
    org_str = textwrap.dedent("""\
    * Entry
    SCHEDULED: <2022-01-01 Sat>
    SCHEDULED: <2022-01-02 Sun>
    """)
    icals = [
        iCalEntry("2022-01-01", None, "Entry", "SCHEDULED: <2022-01-02 Sun>", "SCHEDULED"),
        iCalEntry("2022-01-02", None, "Entry", "SCHEDULED: <2022-01-02 Sun>", "TIMESTAMP"),
    ]
    compare(org_str, icals, include_types={"DEADLINE", "SCHEDULED", "TIMESTAMP", "CLOCK"},
            warnings=["WARNING: Multiple SCHEDULED keywords found in node: `Entry`."])

def test_deadline2():
    org_str = textwrap.dedent("""\
    * Entry
    DEADLINE: <2022-01-01 Sat>
    DEADLINE: <2022-01-02 Sun>
    """)
    icals = [
        iCalEntry("2022-01-01", None, "Entry", "DEADLINE: <2022-01-02 Sun>", "DEADLINE"),
        iCalEntry("2022-01-02", None, "Entry", "DEADLINE: <2022-01-02 Sun>", "TIMESTAMP"),
    ]
    compare(org_str, icals, include_types={"DEADLINE", "DEADLINE", "TIMESTAMP", "CLOCK"},
            warnings=["WARNING: Multiple DEADLINE keywords found in node: `Entry`."])

def test_multiple_repeater():
    org_str = textwrap.dedent("""\
    * Entry
    DEADLINE: <2022-01-01 Sat 10:00 +2w> SCHEDULED: <2022-01-01 Sat 10:00 +2w>
    <2022-01-01 Sat 10:00 +2w>
    """)
    icals = [
        iCalEntry("2022-01-01 10:00:00+00:00", None, "Entry", "<2022-01-01 Sat 10:00 +2w>", "SCHEDULED", "FREQ=WEEKLY;INTERVAL=2"),
        iCalEntry("2022-01-01 10:00:00+00:00", None, "Entry", "<2022-01-01 Sat 10:00 +2w>", "DEADLINE", "FREQ=WEEKLY;INTERVAL=2"),
        iCalEntry("2022-01-01 10:00:00+00:00", None, "Entry", "<2022-01-01 Sat 10:00 +2w>", "TIMESTAMP", "FREQ=WEEKLY;INTERVAL=2"),
    ]
    compare(org_str, icals, include_types={"DEADLINE", "SCHEDULED", "TIMESTAMP", "CLOCK"})
