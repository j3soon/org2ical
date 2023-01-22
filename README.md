# org2ical

[![pypi](https://img.shields.io/pypi/v/org2ical)](https://pypi.org/project/org2ical/)
[![python](https://img.shields.io/pypi/pyversions/org2ical)](https://pypi.org/project/org2ical/)
[![Downloads](https://pepy.tech/badge/org2ical)](https://pepy.tech/project/org2ical)
[![license](https://img.shields.io/pypi/l/org2ical)](https://github.com/j3soon/org2ical/blob/master/LICENSE)

[![tests](https://img.shields.io/github/actions/workflow/status/j3soon/org2ical/test-with-tox.yaml?label=tests)](https://github.com/j3soon/org2ical/actions/workflows/test-with-tox.yaml)
[![build](https://img.shields.io/github/actions/workflow/status/j3soon/org2ical/publish-to-pypi.yaml)](https://github.com/j3soon/org2ical/actions/workflows/publish-to-pypi.yaml)
[![codecov](https://codecov.io/gh/j3soon/org2ical/branch/master/graph/badge.svg?token=xNbUgClfdP)](https://codecov.io/gh/j3soon/org2ical)

Generate an [iCalendar](https://icalendar.org/) (.ics) file based on a [OrgMode](https://orgmode.org/) (.org) file.

This package is especially useful if your OrgMode file is too large to be exported with [OrgMode iCalendar Export](https://orgmode.org/manual/iCalendar-Export.html).

Installation:

```sh
pip install -U org2ical
```

Usage:

```py
import org2ical
# Ref: https://orgmode.org/manual/Timestamps.html
org_str = """
* Meet Peter at the movies
  <2006-11-01 Wed 19:15>
* Discussion on climate change
  <2006-11-02 Thu 20:00-22:00>
"""
ical_str, warnings = org2ical.loads(org_str)
assert warnings == []
print(ical_str)
```

Results:

```
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//j3soon//org2ical//EN
BEGIN:VEVENT
DTSTAMP:20221114T153849Z
UID:2f8059beaf05751acc703c2a12eee7e8
DTSTART:20061101T191500Z
DTEND:20061101T191500Z
SUMMARY:Meet Peter at the movies
DESCRIPTION:  <2006-11-01 Wed 19:15>\n\nOrg Path: Meet Peter at the movies
CATEGORIES:TIMESTAMP
END:VEVENT
BEGIN:VEVENT
DTSTAMP:20221114T153849Z
UID:72b76db7dacae0489b50bb9c9b3b3c34
DTSTART:20061102T200000Z
DTEND:20061102T220000Z
SUMMARY:Discussion on climate change
DESCRIPTION:  <2006-11-02 Thu 20:00-22:00>\n\nOrg Path: Discussion on climate change
CATEGORIES:TIMESTAMP
END:VEVENT
END:VCALENDAR

```

Please note that the `DTSTAMP` here depends on your current time.

## Import to Thunderbird's Lightning Calendar

![](docs/images/preview-thunderbird.png)

1. Export a Org (.org) file to an iCal (.ics) file using org2ical.
2. In Thunderbird, select `Events and Tasks > Import...` and follow the steps to import the iCal file.
3. (Optional) Set category colors:
   ```
   DEADLINE : rgb(255, 128, 128)
   SCHEDULED: rgb(128, 192, 128)
   TIMESTAMP: rgb(128, 128, 255)
   CLOCK    : rgb(255, 192, 128)
   ```
4. (Optional) Fill events with category color by following [this Stack Overflow answer](https://stackoverflow.com/a/74842106).
