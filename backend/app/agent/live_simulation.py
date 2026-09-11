"""Explicit in-memory SDK simulation. This module cannot create a network transport."""

import json

import httpx
from openai import OpenAI
from pydantic import SecretStr

from app.agent.openai_planner import OpenAIPlanner
from app.agent.planner import DeterministicTestPlanner
from app.agent.requirements import TravelRequirements

MOCK_MODEL = "offline-simulation"  # Synthetic fixture label, never a real provider model choice.


def response_body(text):
    return {
        "id": "resp_mock",
        "object": "response",
        "created_at": 0,
        "model": MOCK_MODEL,
        "status": "completed",
        "error": None,
        "incomplete_details": None,
        "instructions": None,
        "metadata": {},
        "output": [
            {
                "id": "msg_mock",
                "type": "message",
                "role": "assistant",
                "status": "completed",
                "content": [{"type": "output_text", "text": text, "annotations": []}],
            }
        ],
        "parallel_tool_calls": False,
        "temperature": 1,
        "tool_choice": "auto",
        "tools": [],
        "top_p": 1,
        "usage": None,
    }


def simulated_planner(settings, handler=None):
    def default_handler(request):
        body = json.loads(request.content)
        requirements = TravelRequirements.model_validate_json(body["input"])
        decision = DeterministicTestPlanner().plan(requirements)
        # Deliberately different order to prove the evaluator measures capabilities.
        decision.tool_requests.reverse()
        return httpx.Response(200, json=response_body(decision.model_dump_json()))

    configured = settings.model_copy(
        update={"openai_api_key": SecretStr("offline-placeholder"), "openai_model": MOCK_MODEL}
    )
    client = OpenAI(
        api_key="offline-placeholder",
        max_retries=0,
        http_client=httpx.Client(transport=httpx.MockTransport(handler or default_handler)),
    )
    return OpenAIPlanner(configured, client=client)
