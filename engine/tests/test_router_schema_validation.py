"""
Tests to guard router schema validation for the API.

These cover the playthroughs and tempo routers to ensure Pydantic models
reject malformed payloads before heavy logic runs.
"""

from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest

from engine.infrastructure.api.playthroughs import create_playthroughs_router
from engine.infrastructure.api.tempo import create_tempo_router


@pytest.fixture
def playthroughs_client():
    """Test client for the playthroughs router."""
    app = FastAPI()
    router = create_playthroughs_router()
    app.include_router(router, prefix="/api")
    return TestClient(app)


@pytest.fixture
def tempo_client():
    """Test client for the tempo router."""
    app = FastAPI()
    router = create_tempo_router()
    app.include_router(router, prefix="/api")
    return TestClient(app)


class TestPlaythroughRouterValidation:
    """Schema validation for /api/playthroughs and /api/moment."""

    def test_playthrough_requires_player_name(self, playthroughs_client):
        response = playthroughs_client.post(
            "/api/playthrough/create",
            json={"scenario_id": "opening_scene"}
        )
        assert response.status_code == 422

    def test_playthrough_scenario_alias_requires_scenario_id(self, playthroughs_client):
        response = playthroughs_client.post(
            "/api/playthrough/scenario",
            json={"player_name": "Fog"}
        )
        assert response.status_code == 422

    def test_send_moment_requires_text(self, playthroughs_client):
        response = playthroughs_client.post(
            "/api/moment",
            json={"playthrough_id": "pt_missing_text"}
        )
        assert response.status_code == 422


class TestTempoRouterValidation:
    """Schema validation for the tempo router."""

    def test_set_speed_requires_speed(self, tempo_client):
        response = tempo_client.post(
            "/api/tempo/speed",
            json={"playthrough_id": "pt_tempo"}
        )
        assert response.status_code == 422

    def test_set_speed_rejects_invalid_literal(self, tempo_client):
        response = tempo_client.post(
            "/api/tempo/speed",
            json={"playthrough_id": "pt_tempo", "speed": "fast"}
        )
        assert response.status_code == 422

    def test_player_input_requires_text(self, tempo_client):
        response = tempo_client.post(
            "/api/tempo/input",
            json={"playthrough_id": "pt_tempo"}
        )
        assert response.status_code == 422

    def test_queue_size_requires_queue_length(self, tempo_client):
        response = tempo_client.post(
            "/api/tempo/queue-size",
            json={"playthrough_id": "pt_tempo"}
        )
        assert response.status_code == 422

