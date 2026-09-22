# Public GitHub Releases

<a href="../public-releases.subfork.json" download="public-releases.subfork.json" aria-label="Download graph" title="Download graph"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12m-5-5 5 5 5-5M5 16v5h14v-5"/></svg></a>

Fetches the first ten published releases from a public GitHub repository. Change
the URL node to `https://api.github.com/repos/OWNER/REPOSITORY/releases` to inspect
another repository.

This example is keyless and read-only. GitHub permits unauthenticated requests for
public releases, but applies lower unauthenticated rate limits. The request asks
for ten rows, uses a 20-second timeout, and caps the response at 500 KB. It does
not follow pagination and does not include tags that have no GitHub Release.

Expected outputs:

- `releases`: up to ten release objects for a Table or JSON panel;
- `status`: the provider HTTP status;
- `response`: a JSON response containing the bounded rows.

Provider: `api.github.com`. No external writes or paid operations occur. GitHub's
API terms and rate limits apply. Manually tested against a fixture only; live API
behavior should be checked on the target Subfork version before publishing it as
a composite.
