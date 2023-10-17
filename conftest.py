import pytest
from model_bakery import baker

from endpoints.models import Customer


@pytest.fixture
def customer(db):
    return baker.make(
        Customer,
        name="Ryan",
    )
