# IoT Example Instructions

- Prefer read-only public telemetry feeds. Never include device credentials,
  private broker addresses, home-network URLs, or precise personal locations.
- Bound remote reads by result count, timeout, and response size, then apply a
  local row limit before exposing table output.
- Preserve observation timestamps and units. Label values as raw when the source
  does not publish a trustworthy unit.
- Document expected reporting cadence, stale-data behavior, caching, and whether
  a feed is suitable for operational or safety-critical decisions.
- Treat HTTP examples as snapshots. MQTT subscriptions, device commands, and
  scheduled ingestion require separate runtime capabilities.
