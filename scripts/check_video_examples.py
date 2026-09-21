#!/usr/bin/env python3
"""Offline video graph checks using --runtime-root path/to/subfork-new/backend/runtime."""
import argparse
import base64
from io import BytesIO
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--runtime-root', type=Path, required=True)
args, rest = parser.parse_known_args()
sys.path.insert(0, str(args.runtime_root.resolve()))
from PIL import Image
from subfork_runtime.artifacts import GraphDefinition, GraphEdge, GraphNode, GraphOutput
from subfork_runtime.execution_protocol import NodeExecutionResult
from subfork_runtime.executor import GraphExecutor
from subfork_runtime.runtime_nodes import FetchUrlNode

ROOT = Path(__file__).resolve().parents[1]


class VideoExamples(unittest.TestCase):
    def run_graph(self, image, size='1280x720'):
        slug = 'openai-image-to-video-job' if image else 'openai-video-generation-job'
        doc = json.loads((ROOT / 'graphs/ai/video' / (slug + '.subfork.json')).read_text())['definition']
        for n in doc['nodes']:
            if n['node_instance_id'] == 'image': n['params']['artifact_id'] = 'art_fixture'
            if n['node_instance_id'] == 'video_size': n['params']['text'] = size
        graph = GraphDefinition(**{**doc, 'graph_id': 'g_video_test', 'nodes': [GraphNode(**n) for n in doc['nodes']], 'edges': [GraphEdge(**e) for e in doc['edges']], 'graph_outputs': {k: GraphOutput(**v) for k, v in doc['graph_outputs'].items()}})
        writes=[]; calls=[]
        def writer(**payload):
            writes.append(payload)
            return {'artifact_id': 'art_resized', 'media_type': 'image/jpeg', 'url': 'https://example.com/preview', 'provider_url': 'https://example.com/resized?signature=fixture'}
        def fetch(_, req):
            calls.append(req.node_instance_id)
            if req.node_instance_id == 'resize':
                data=BytesIO();Image.new('RGB',(100,100),'red').save(data,format='PNG')
                return NodeExecutionResult(outputs={'status':200,'body_base64':base64.b64encode(data.getvalue()).decode()})
            if req.node_instance_id == 'submit':
                body=req.inputs['body']
                self.assertEqual(body['size'],size)
                if image:
                    self.assertEqual(body['input_reference']['image_url'],'https://example.com/resized?signature=fixture')
                    self.assertEqual(Image.open(BytesIO(writes[0]['data'])).size,tuple(map(int,size.split('x'))))
                else: self.assertNotIn('input_reference',body)
                return NodeExecutionResult(outputs={'status':202,'json':{'id':'video_test'}})
            if req.node_instance_id == 'poll':
                return NodeExecutionResult(outputs={'status':200,'json':{'id':'video_test','status':'completed'}})
            self.assertEqual(req.node_instance_id,'fetch_video')
            return NodeExecutionResult(outputs={'status':200,'media':{'url':'https://example.com/video.mp4','content_type':'video/mp4'}})
        with patch.object(FetchUrlNode,'execute',fetch):
            record=GraphExecutor(artifact_writer=writer).execute(graph,execution_profile={'artifacts':{'art_fixture':{'url':'https://example.com/source.png','media_type':'image/png'}}})
        self.assertEqual(record.status,'completed',record.error)
        self.assertEqual(calls,['resize','submit','poll','fetch_video'] if image else ['submit','poll','fetch_video'])

    def test_text_only_still_omits_image(self):
        self.run_graph(False)

    def test_one_size_drives_resize_and_request(self):
        for size in ['1280x720','720x1280']:
            with self.subTest(size=size): self.run_graph(True,size)


if __name__ == '__main__':
    unittest.main(argv=[sys.argv[0], *rest])
