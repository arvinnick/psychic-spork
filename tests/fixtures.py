import pytest
from httpx import ASGITransport, AsyncClient

from db.database import get_db
from main import app
from tests.mock_database import MockDatabase


