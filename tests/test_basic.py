import pytest
import flynn
from flynn import server, handlers

def test_version():
    assert flynn.__version__ == "1.0.0"

def test_server_initialization():
    assert server.server.name == "flynn"

def test_handlers_timeout():
    assert handlers.DockerHandlers.TIMEOUT_AMOUNT == 200
