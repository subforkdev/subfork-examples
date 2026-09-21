#!/usr/bin/env python3
"""Offline graph execution checks. Pass --runtime-root path/to/subfork-new/backend/runtime."""
import argparse
from copy import deepcopy
import json
from pathlib import Path
import sys
import unittest

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--runtime-root', type=Path, required=True)
args, test_args = parser.parse_known_args()
sys.path.insert(0, str(args.runtime_root.resolve()))
from subfork_runtime.artifacts import GraphDefinition, GraphNode, GraphEdge, GraphOutput
from subfork_runtime.executor import GraphExecutor
from subfork_runtime.registry import RuntimeNodeRegistry
from subfork_runtime.runtime_nodes import FetchUrlNode, RuntimeNode
from subfork_runtime.execution_protocol import NodeExecutionResult

ROOT = Path(__file__).resolve().parents[1]


class ProviderFixture(RuntimeNode):
    manifest = FetchUrlNode.manifest

    def __init__(self, response):
        self.response = response
        self.calls = []

    def execute(self, request):
        self.calls.append(request)
        if request.node_instance_id == 'narration_request':
            body = request.inputs['body']
            assert body['store'] is False
            assert body['input'][0]['content'][0]['file_url'].startswith('https://')
            assert body['max_output_tokens'] == 900
            return NodeExecutionResult(outputs={'json': self.response, 'status': 200})
        assert request.params['url'].endswith('/audio/speech')
        assert 0 < len(request.inputs['body']['input']) <= 3500
        return NodeExecutionResult(outputs={'status': 200, 'json': None, 'media': {'url': 'https://example.com/fixture.mp3', 'content_type': 'audio/mpeg'}})


def execute(pdf=False, overrides=None, response=None, uploaded=True, media_type='application/pdf'):
    slug = 'openai-pdf-narration' if pdf else 'openai-read-aloud'
    doc = json.loads((ROOT / 'graphs' / 'ai' / 'audio' / (slug + '.subfork.json')).read_text())['definition']
    doc['graph_id'] = 'g_narration_test'
    for n in doc['nodes']:
        n['params'].update((overrides or {}).get(n['node_instance_id'], {}))
        if pdf and uploaded and n['node_instance_id'] == 'file':
            n['params']['artifact_id'] = 'art_fixture'
    registry = RuntimeNodeRegistry()
    # Verify every node and edge against the real node catalog before mocking HTTP.
    node_map = {n['node_instance_id']: n for n in doc['nodes']}
    for n in doc['nodes']:
        registry.get(n['node_id'], n['node_version'])
    for e in doc['edges']:
        source, target = node_map[e['source_node_id']], node_map[e['target_node_id']]
        sm = registry.get(source['node_id'], source['node_version']).manifest
        tm = registry.get(target['node_id'], target['node_version']).manifest
        assert e['source_output'] in sm.outputs
        assert e['target_input'] in tm.inputs or e['target_input'] in target.get('custom_inputs', {}) or tm.parameters.get(e['target_input'], {}).get('exposable')
    fixture = ProviderFixture(response if response is not None else {'status': 'completed', 'output': [{'type': 'reasoning'}, {'type': 'message', 'content': [{'type': 'output_text', 'text': 'A short, clear narration.'}]}]})
    registry.register(fixture)
    doc['nodes'] = [GraphNode(**n) for n in doc['nodes']]
    doc['edges'] = [GraphEdge(**e) for e in doc['edges']]
    doc['graph_outputs'] = {k: GraphOutput(**v) for k, v in doc['graph_outputs'].items()}
    profile = {'artifacts': {'art_fixture': {'url': 'https://example.com/document.pdf?signature=fixture', 'media_type': media_type, 'filename': 'sample.pdf', 'size_bytes': 100}}} if uploaded else {}
    result = GraphExecutor(registry).execute(GraphDefinition(**doc), execution_profile=profile)
    return result, fixture.calls


class NarrationExamples(unittest.TestCase):
    def test_read_aloud_preserves_text_and_delivery(self):
        script = 'Quotes " and newlines\nremain unchanged.'
        result, calls = execute(overrides={'script': {'text': script}})
        self.assertEqual(result.status, 'completed', result.error)
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].inputs['body']['input'], script)
        self.assertIn('unhurried', calls[0].inputs['body']['instructions'])

    def test_bad_text_voice_and_direction_prevent_calls(self):
        for node, value in [('script', ''), ('script', '  \n'), ('script', 'x' * 3501), ('voice', 'invented'), ('delivery', 'x' * 1001)]:
            with self.subTest(node=node, length=len(value)):
                result, calls = execute(overrides={node: {'text': value}})
                self.assertEqual(result.status, 'failed')
                self.assertEqual(calls, [])

    def test_pdf_upload_to_transcript_to_speech(self):
        result, calls = execute(pdf=True)
        self.assertEqual(result.status, 'completed', result.error)
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[1].inputs['body']['input'], 'A short, clear narration.')

    def test_missing_or_wrong_file_prevents_calls(self):
        for kw in [{'uploaded': False}, {'media_type': 'text/plain'}]:
            result, calls = execute(pdf=True, **kw)
            self.assertEqual(result.status, 'failed')
            self.assertEqual(calls, [])

    def test_invalid_prompt_prevents_calls(self):
        result, calls = execute(pdf=True, overrides={'prompt': {'text': 'x' * 2001}})
        self.assertEqual(result.status, 'failed')
        self.assertEqual(calls, [])

    def test_bad_provider_result_never_reaches_speech(self):
        for response in [
            {'error': {'message': 'provider error'}},
            {'status': 'completed', 'output': []},
            {'status': 'completed', 'output': [{'type': 'message', 'content': [{'type': 'refusal', 'refusal': 'No'}]}]},
            *[{'status': status, 'output': [{'type': 'message', 'content': [{'type': 'output_text', 'text': text}]}]} for status, text in [('incomplete', 'Partial'), ('completed', ''), ('completed', 'x' * 3501)]],
        ]:
            with self.subTest(response=str(response)[:80]):
                result, calls = execute(pdf=True, response=deepcopy(response))
                self.assertEqual(result.status, 'failed')
                self.assertEqual([c.node_instance_id for c in calls], ['narration_request'])


if __name__ == '__main__':
    unittest.main(argv=[sys.argv[0], *test_args])
