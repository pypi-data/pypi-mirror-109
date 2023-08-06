import os
import unittest

from worker.mixins.rollbar import payload_handler
from worker.test.utils import file_to_json


class TestRollbarPayloadHandler(unittest.TestCase):
    def test_rollbar_payload_handler(self):
        original_payload = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', 'resources', 'test', 'original_rollbar_payload.json')
        )
        original_payload = file_to_json(original_payload)
        self.assertEqual(len(original_payload["data"]["body"]["trace"]["frames"][1]["locals"]["dataset"]), 23)

        trimmed_payload = payload_handler(original_payload)
        self.assertEqual(len(trimmed_payload["data"]["body"]["trace"]["frames"][1]["locals"]["dataset"]), 3)
