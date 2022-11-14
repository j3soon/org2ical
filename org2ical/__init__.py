import hashlib
import textwrap
from datetime import date, datetime, timezone
from typing import Set, Union, Tuple

import orgparse

DEADLINE = 'DEADLINE'
SCHEDULED = 'SCHEDULED'
TIMESTAMP = 'TIMESTAMP'
CLOCK = 'CLOCK'
# Ignore inactive timestamps

def loads(
        org_str: str,
        *,
        prod_id: str = "-//j3soon//org2ical//EN",
        now: datetime = datetime.now(tz=timezone.utc),
        categories: Set[str] = set(),
        ignore_states: Set[str] = {"DONE", "CANCELED"},
        ignore_tags: Set[str] = {"ARCHIVE"},
        include_types: Set[str] = {DEADLINE, SCHEDULED, TIMESTAMP},
    ) -> str:

    def _encode_datetime(datetime: datetime) -> str:
        """Encodes a datetime object into an iCalendar-compatible string."""
        return datetime.replace(tzinfo=timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    def _encode_date(d: Union[date, datetime]) -> str:
        """Encodes a date or datetime object into an iCalendar-compatible string."""
        if isinstance(d, datetime):
            return _encode_datetime(d)
        return d.strftime("%Y%m%d")

    def _encode_rrule(cookie: Tuple[str]) -> str:
        """Encodes a repeater tuple into an iCalendar-compatible string."""
        if cookie is None:
            return ""
        assert len(cookie) == 3
        repeater = cookie[0]
        # This 3 repeaters all mean the same thing during parsing
        assert repeater in ['+', '++', '.+']
        interval = cookie[1]
        freq = {
            'h': 'HOURLY',
            'd': 'DAILY',
            'w': 'WEEKLY',
            'm': 'MONTHLY',
            'y': 'YEARLY'
        }[cookie[2]]
        return f"RRULE:FREQ={freq};INTERVAL={interval}"

    def _node_is_ignored(node: orgparse.OrgNode) -> bool:
        """Determines if a node should be ignored."""
        if ignore_states.intersection([node.todo]):
            return True
        if ignore_tags.intersection(node.tags):
            return True
        # Check manually since orgparse doesn't support custom Todo states
        if node.todo is not None:
            return False
        for s in ignore_states:
            if node.heading.startswith(s):
                if len(node.heading) > len(s) and node.heading[len(s)] == " ":
                    return True
        return False
    
    def _node_full_path(node: orgparse.OrgNode) -> str:
        headings = []
        while node != source:
            headings.append(node.heading)
            node = node.parent
        headings.reverse()
        return " > ".join(headings)
    
    def _construct_warning(node: orgparse.OrgNode, message: str) -> str:
        return textwrap.dedent(f"""WARNING: {message} in node: `{_node_full_path(node)}`.""")

    def _construct_vevent(
            now: str,
            startutc: str,
            endutc: str,
            summary: str,
            description: str,
            categories: Set[str],
            *,
            rrule: str = "",
        ) -> str:
        """Constructs an iCaldendar VEVENT entry string."""
        description = description.replace("\r\n", "\n").replace("\n", "\\n")
        entry_begin = f"""
        BEGIN:VEVENT
        DTSTAMP:{now}
        """.strip()
        entry_mid = f"""
        DTSTART:{startutc}
        DTEND:{endutc}
        SUMMARY:{summary}
        DESCRIPTION:{description}
        CATEGORIES:{",".join(categories)}
        {rrule}
        """.strip()
        entry_end = f"""
        END:VEVENT
        """.strip()
        md5hash = hashlib.md5((entry_begin + entry_mid + entry_end).encode('utf-8')).hexdigest()
        entry = textwrap.dedent(f"""\
        {entry_begin}
        UID:{md5hash}
        {entry_mid}
        {entry_end}
        """)
        return entry
    
    warnings = []
    ical_entries = []
    now_str = _encode_datetime(now)

    source = orgparse.loads(org_str)
    for node in source.root[1:]:  # [1:] for skipping root itself
        if _node_is_ignored(node):
            continue
        summary = node.heading
        if node.priority:  # Restore priority removed by orgparse
            summary = "[{}] ".format(node.priority) + summary
        description = node.body
        if description != "":
            description += "\n\n"
        description += "Org Path: " + _node_full_path(node)
        if SCHEDULED in include_types:
            n_scheduled = node.body.count(SCHEDULED)
            if n_scheduled > 0:
                if node.scheduled:
                    warnings.append(_construct_warning(node, f"Multiple {SCHEDULED} keywords found"))
                else:
                    warnings.append(_construct_warning(node, f"{SCHEDULED} keyword found but no timestamp"))
            if node.scheduled:
                start = end = _encode_date(node.scheduled.start)
                rrule = _encode_rrule(node.scheduled._repeater)
                ical_entries.append(_construct_vevent(now_str, start, end, summary, description, categories.union({SCHEDULED}), rrule=rrule))
        if DEADLINE in include_types:
            n_deadline = node.body.count(DEADLINE)
            if n_deadline > 0:
                if node.deadline:
                    warnings.append(_construct_warning(node, f"Multiple {DEADLINE} keywords found"))
                else:
                    warnings.append(_construct_warning(node, f"{DEADLINE} keyword found but no timestamp"))
            if node.deadline:
                start = end = _encode_date(node.deadline.start)
                rrule = _encode_rrule(node.deadline._repeater)
                ical_entries.append(_construct_vevent(now_str, start, end, summary, description, categories.union({DEADLINE}), rrule=rrule))
        if TIMESTAMP in include_types:
            datelist = node.get_timestamps(active=True, point=True)
            for d in datelist:
                start = end = _encode_date(d.start)
                rrule = _encode_rrule(d._repeater)
                ical_entries.append(_construct_vevent(now_str, start, end, summary, description, categories.union({TIMESTAMP}), rrule=rrule))
            rangelist = node.get_timestamps(active=True, range=True)
            for d in rangelist:
                start = _encode_date(d.start)
                end = _encode_date(d.end)
                rrule = _encode_rrule(d._repeater)
                ical_entries.append(_construct_vevent(now_str, start, end, summary, description, categories.union({"TIMESTAMP"}), rrule=rrule))
        if CLOCK in include_types:
            for d in node.clock:
                start = _encode_date(d.start)
                if d.end is None:
                    continue  # Skip clocks that are still running
                end = _encode_date(d.end)
                ical_entries.append(_construct_vevent(now_str, start, end, summary, description, categories.union({CLOCK})))
                assert d._repeater is None

    ical_entries_str = "".join(ical_entries).strip()
    ical_str = f"""\
BEGIN:VCALENDAR
VERSION:2.0
PRODID:{prod_id}
{ical_entries_str}
END:VCALENDAR
"""
    return ical_str, warnings