import time
import pytest
import requests

BASE_URL = "http://5.181.109.28:9090/api/v3"

def generate_id():
    return int(time.time() * 1000)

@pytest.fixture(scope="function")
def create_pet():
    pet_id = generate_id()

    payload = {
        "id": pet_id,
        "name": "Buddy",
        "status": "available"
    }

    response = requests.post(url=f'{BASE_URL}/pet', json=payload)
    assert response.status_code == 200
    return response.json()

@pytest.fixture(scope="function")
def create_order(create_pet):
    order_id = generate_id()

    payload = {
        "id": order_id,
        "petId": create_pet["id"],
        "quantity": 1,
        "status": "placed",
        "complete": True
    }

    response = requests.post(url=f'{BASE_URL}/store/order', json=payload)
    assert response.status_code == 200
    return response.json()