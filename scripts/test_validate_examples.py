"""Offline coverage for the optional target-catalog validation."""
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import URLError

import validate_examples as validator


class CatalogValidationTests(unittest.TestCase):
    def test_fetch_is_bounded_and_parses_catalog(self):
        response = io.BytesIO(b'[{"node_id":"n_text_value"}]')
        with patch.object(validator, "urlopen", return_value=response) as fetch:
            self.assertEqual(validator.fetch_node_types("https://example.com/api/v1/nodes"), {"n_text_value"})
        request = fetch.call_args.args[0]
        self.assertEqual(request.get_method(), "GET")
        self.assertIsNone(request.data)
        self.assertEqual(fetch.call_args.kwargs["timeout"], 15)

    def test_bad_catalogs_fail(self):
        for body in [b'{}', b'null', b'<html>bad gateway</html>', b'[{}]', b'[{"node_id":[]}]']:
            with self.subTest(body=body), patch.object(validator, "urlopen", return_value=io.BytesIO(body)):
                with self.assertRaises(ValueError):
                    validator.fetch_node_types("https://example.com/api/v1/nodes")

    def test_oversized_response_fails(self):
        with patch.object(validator, "CATALOG_MAX_BYTES", 10), patch.object(validator, "urlopen", return_value=io.BytesIO(b' ' * 11)):
            with self.assertRaisesRegex(ValueError, "response limit"):
                validator.fetch_node_types("https://example.com/api/v1/nodes")

    def test_invalid_url_never_fetches(self):
        for url in ["file:///tmp/catalog.json", "https://user:password@example.com/nodes"]:
            with self.subTest(url=url), patch.object(validator, "urlopen") as fetch:
                with self.assertRaises(ValueError):
                    validator.fetch_node_types(url)
                fetch.assert_not_called()

    def test_cli_offline_success_online_match_mismatch_and_unavailable(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            graphs = root / "graphs"
            graphs.mkdir()
            document = {"format": "subfork.graph/1", "definition": {"name": "Test", "nodes": [{"node_instance_id": "source", "node_id": "n_text_value"}], "edges": []}}
            (graphs / "test.subfork.json").write_text(json.dumps(document))
            (graphs / "test.notes.md").write_text("Test notes")
            with patch.object(validator, "ROOT", root), patch.object(validator, "GRAPH_ROOT", graphs):
                with patch.object(validator, "fetch_node_types") as fetch, contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(validator.main([]), 0)
                    fetch.assert_not_called()
                for result, failure, code in [({"n_text_value"}, None, 0), ({"n_other"}, None, 1), (set(), None, 1), (None, URLError("unavailable"), 1)]:
                    with self.subTest(result=result, failure=failure), patch.object(validator, "fetch_node_types", return_value=result, side_effect=failure) as fetch:
                        output = io.StringIO()
                        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
                            self.assertEqual(validator.main(["--node-catalog-url", "https://example.com/api/v1/nodes"]), code)
                        fetch.assert_called_once()
                        if result == {"n_other"}:
                            self.assertIn("graphs/test.subfork.json", output.getvalue())
                            self.assertIn("source", output.getvalue())
                            self.assertIn("n_text_value", output.getvalue())
                        if failure:
                            self.assertIn("could not validate against node catalog", output.getvalue())


if __name__ == "__main__":
    unittest.main()
