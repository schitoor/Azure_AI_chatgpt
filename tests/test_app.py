import json

import pytest
import quart.testing.app

import app


@pytest.mark.asyncio
async def test_missing_env_vars():
    quart_app = app.create_app()

    with pytest.raises(quart.testing.app.LifespanError) as exc_info:
        async with quart_app.test_app() as test_app:
            test_app.test_client()
        assert str(exc_info.value) == "Lifespan failure in startup. ''AZURE_OPENAI_EMB_DEPLOYMENT''"

@pytest.mark.asyncio
async def test_index(client):
    response = await client.get("/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_ask_request_must_be_json(client):
    response = await client.post("/ask")
    assert response.status_code == 415
    result = await response.get_json()
    assert result["error"] == "request must be json"


@pytest.mark.asyncio
async def test_ask_with_unknown_approach(client):
    response = await client.post("/ask", json={"approach": "test"})
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_ask_rtr_text(client, snapshot):
    response = await client.post(
        "/ask",
        json={
            "approach": "rtr",
            "question": "What is the capital of France?",
            "overrides": {"retrieval_mode": "text"},
        },
    )
    assert response.status_code == 200
    result = await response.get_json()
    snapshot.assert_match(json.dumps(result, indent=4), "result.json")


@pytest.mark.asyncio
async def test_ask_rtr_text_semanticranker(client, snapshot):
    response = await client.post(
        "/ask",
        json={
            "approach": "rtr",
            "question": "What is the capital of France?",
            "overrides": {"retrieval_mode": "text", "semantic_ranker": True},
        },
    )
    assert response.status_code == 200
    result = await response.get_json()
    snapshot.assert_match(json.dumps(result, indent=4), "result.json")


@pytest.mark.asyncio
async def test_ask_rtr_text_semanticcaptions(client, snapshot):
    response = await client.post(
        "/ask",
        json={
            "approach": "rtr",
            "question": "What is the capital of France?",
            "overrides": {"retrieval_mode": "text", "semantic_captions": True},
        },
    )
    assert response.status_code == 200
    result = await response.get_json()
    snapshot.assert_match(json.dumps(result, indent=4), "result.json")


@pytest.mark.asyncio
async def test_ask_rtr_hybrid(client, snapshot):
    response = await client.post(
        "/ask",
        json={
            "approach": "rtr",
            "question": "What is the capital of France?",
            "overrides": {"retrieval_mode": "hybrid"},
        },
    )
    assert response.status_code == 200
    result = await response.get_json()
    snapshot.assert_match(json.dumps(result, indent=4), "result.json")


@pytest.mark.asyncio
async def test_chat_request_must_be_json(client):
    response = await client.post("/chat")
    assert response.status_code == 415
    result = await response.get_json()
    assert result["error"] == "request must be json"


@pytest.mark.asyncio
async def test_chat_with_unknown_approach(client):
    response = await client.post("/chat", json={"approach": "test"})
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_chat_text(client, snapshot):
    response = await client.post(
        "/chat",
        json={
            "approach": "rrr",
            "history": [{"user": "What is the capital of France?"}],
            "overrides": {"retrieval_mode": "text"},
        },
    )
    assert response.status_code == 200
    result = await response.get_json()
    snapshot.assert_match(json.dumps(result, indent=4), "result.json")


@pytest.mark.asyncio
async def test_chat_text_semanticranker(client, snapshot):
    response = await client.post(
        "/chat",
        json={
            "approach": "rrr",
            "history": [{"user": "What is the capital of France?"}],
            "overrides": {"retrieval_mode": "text", "semantic_ranker": True},
        },
    )
    assert response.status_code == 200
    result = await response.get_json()
    snapshot.assert_match(json.dumps(result, indent=4), "result.json")


@pytest.mark.asyncio
async def test_chat_text_semanticcaptions(client, snapshot):
    response = await client.post(
        "/chat",
        json={
            "approach": "rrr",
            "history": [{"user": "What is the capital of France?"}],
            "overrides": {"retrieval_mode": "text", "semantic_captions": True},
        },
    )
    assert response.status_code == 200
    result = await response.get_json()
    snapshot.assert_match(json.dumps(result, indent=4), "result.json")


@pytest.mark.asyncio
async def test_chat_prompt_template(client, snapshot):
    response = await client.post(
        "/chat",
        json={
            "approach": "rrr",
            "history": [{"user": "What is the capital of France?"}],
            "overrides": {"retrieval_mode": "text", "prompt_template": "You are a cat."},
        },
    )
    assert response.status_code == 200
    result = await response.get_json()
    snapshot.assert_match(json.dumps(result, indent=4), "result.json")


@pytest.mark.asyncio
async def test_chat_prompt_template_concat(client, snapshot):
    response = await client.post(
        "/chat",
        json={
            "approach": "rrr",
            "history": [{"user": "What is the capital of France?"}],
            "overrides": {"retrieval_mode": "text", "prompt_template": ">>> Meow like a cat."},
        },
    )
    assert response.status_code == 200
    result = await response.get_json()
    snapshot.assert_match(json.dumps(result, indent=4), "result.json")


@pytest.mark.asyncio
async def test_chat_hybrid(client, snapshot):
    response = await client.post(
        "/chat",
        json={
            "approach": "rrr",
            "history": [{"user": "What is the capital of France?"}],
            "overrides": {"retrieval_mode": "hybrid"},
        },
    )
    assert response.status_code == 200
    result = await response.get_json()
    snapshot.assert_match(json.dumps(result, indent=4), "result.json")


@pytest.mark.asyncio
async def test_chat_vector(client, snapshot):
    response = await client.post(
        "/chat",
        json={
            "approach": "rrr",
            "history": [{"user": "What is the capital of France?"}],
            "overrides": {"retrieval_mode": "vector"},
        },
    )
    assert response.status_code == 200
    result = await response.get_json()
    snapshot.assert_match(json.dumps(result, indent=4), "result.json")


@pytest.mark.asyncio
async def test_chat_stream_request_must_be_json(client):
    response = await client.post("/chat_stream")
    assert response.status_code == 415
    result = await response.get_json()
    assert result["error"] == "request must be json"


@pytest.mark.asyncio
async def test_chat_stream_with_unknown_approach(client):
    response = await client.post("/chat_stream", json={"approach": "test"})
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_chat_stream_text(client, snapshot):
    response = await client.post(
        "/chat_stream",
        json={
            "approach": "rrr",
            "history": [{"user": "What is the capital of France?"}],
            "overrides": {"retrieval_mode": "text"},
        },
    )
    assert response.status_code == 200
    result = await response.get_data()
    snapshot.assert_match(result, "result.jsonlines")


@pytest.mark.asyncio
async def test_format_as_ndjson():
    async def gen():
        yield {"a": "I ❤️ 🐍"}
        yield {"b": "Newlines inside \n strings are fine"}

    result = [line async for line in app.format_as_ndjson(gen())]
    assert result == ['{"a": "I ❤️ 🐍"}\n', '{"b": "Newlines inside \\n strings are fine"}\n']
