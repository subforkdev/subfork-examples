# Calendar Merge HTML View

Purpose: extends the merge-calendars graph into an HTML calendar page.

Current behavior: fetches two public ICS feeds, parses, merges, sorts, stringifies the events, and renders them with FullCalendar loaded from jsDelivr.

Architecture note: this is a useful probe for independent graph branches, scheduling fairness, CDN-backed client widgets, and HTML output from row/list pipelines.

Library note: FullCalendar is used here because the standard browser bundle accepts an in-memory events array. Webix Scheduler is still interesting, but its scheduler widget is more backend- and license-oriented, so it is less ideal for a portable seed graph.
