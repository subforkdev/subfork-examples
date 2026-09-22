# US Public Holiday Calendar

<a href="../us-public-holiday-calendar.subfork.json" download="us-public-holiday-calendar.subfork.json" aria-label="Download graph" title="Download graph"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12m-5-5 5 5 5-5M5 16v5h14v-5"/></svg></a>

Fetches Nager.Date's 2026 U.S. holiday list, keeps entries marked as national,
normalizes them into calendar rows, and emits a `text/calendar` response. Edit
the year in the fixed provider URL and calendar name when adapting the graph for
a later year.

This graph is keyless and read-only. One country-year naturally bounds the
provider response; the graph additionally keeps at most 25 events and uses a
20-second timeout and 300 KB response cap. Run it again if the provider revises
the year's calendar.

Expected outputs are `holidays`, provider `status`, and an iCalendar `response`.
Bind `holidays` to a Table panel. Events are all-day dates with no timezone or
recurrence expansion. Holiday definitions and observed dates vary by jurisdiction
and employer; verify dates with the relevant authority before operational use.

Source: [Nager.Date Public Holiday API](https://date.nager.at/Api). The 2026 U.S.
endpoint was live-tested on September 21, 2026.
