import unittest
from unittest.mock import  patch

from fastapi.testclient import TestClient

import api

class TestAgentAPI(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(api.app)

    def test_health_endpoint(self):
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    @patch("api.run_agent")
    def test_chat_success(self, mock_run_agent):
        mock_run_agent.return_value = (
            "The answer is 310.",
            [
                {
                    "step": 1,
                    "tool": "add_numbers",
                    "arguments": {"a": 210, "b":100},
                    "result": 310,
                }
            ],
        )

        response = self.client.post(
            "/chat",
            json={
                "message": "What is 210 plus 100?"
            },
        )

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data["answer"], "The answer is 310.")
        self.assertEqual(len(data["trace"]), 1)
        self.assertEqual(data["trace"][0]["tool"], "add_numbers")

        mock_run_agent.assert_called_once_with(
            "What is 210 plus 100?"
        )

    def test_blank_message_rejected(self):
        response = self.client.post(
            "/chat",
            json={"message": "   "},
        )

        self.assertEqual(response.status_code, 422)

    def test_missing_message_rejected(self):
        response = self.client.post(
            "/chat",
            json={},
        )
        self.assertEqual(response.status_code, 422)

    def test_message_too_long_rejection(self):
        response = self.client.post(
            "/chat",
            json={"message": "a" * 2001},
        )

        self.assertEqual(response.status_code, 422)

    @patch("api.run_agent", side_effect=RuntimeError("internal details"))
    def test_unexpected_agent_error_returns_generic_message(
        self,
        mock_run_agent,
    ):
        response = self.client.post(
            "/chat",
            json={"message": "Run a test"},
        )

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json()["detail"],
                         "The agent encountered an unexpected error.",)

        # Internal exception detauls should not be exposed to clients.
        self.assertNotIn("internal details", response.text)


if __name__ == "__main__":
    unittest.main()