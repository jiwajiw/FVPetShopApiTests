import allure
import jsonschema
import pytest
import requests
from .schemas.store_schema import INVENTORY_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"

@allure.feature("Store")
class TestStore:

    @allure.title("Размещение заказа")
    def test_post_order(self):
        with allure.step("Отправка POST-запроса на создание заказа"):
            payload = {
                "id": 1,
                "petId": 1,
                "quantity": 1,
                "status": "placed",
                "complete": True
            }
            response = requests.post(url=f'{BASE_URL}/store/order', json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Not expected status code"
            assert isinstance(response_json, dict), "Not expected json"

        with allure.step("Проверка параметров заказа в ответе"):
            assert response_json['id'] == payload['id'], "Not expected id"
            assert response_json['petId'] == payload['petId'], "Not expected petId"
            assert response_json['quantity'] == payload['quantity'], "Not expected quantity"
            assert response_json['status'] == payload['status'], "Not expected status"
            assert response_json['complete'] == payload['complete'], "Not expected complete"

    @allure.title("Получение информации о заказе по ID")
    def test_get_order_id(self, create_order):
        with allure.step(f"Отправка запроса на получение информации по id"):
            order_id = create_order["id"]
            response = requests.get(url=f'{BASE_URL}/store/order/{order_id}')
            response_json = response.json()

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Not expected status code"

        with allure.step("Проверка данных заказа в ответе"):
            assert response_json['id'] == order_id, "Not expected id"
            assert isinstance(response_json, dict), "Not expected json"

    @allure.title("Удаление заказа по ID")
    def test_delete_order_id(self, create_order):
        with allure.step("Получение ID созданного заказа"):
            order_id = create_order["id"]

        with allure.step("Отправка запроса на удаление информации о заказе по ID"):
            response = requests.delete(url=f'{BASE_URL}/store/order/{order_id}')
            assert response.status_code == 200, "Not expected status code"

        with allure.step("Отправка запроса на получение информации о заказе по ID"):
            response = requests.get(url=f'{BASE_URL}/store/order/{order_id}')
            assert response.status_code == 404, "Not expected status code"

    @allure.title("Попытка получить информацию о несуществующем заказе")
    def test_get_unexistent_order(self):
        with allure.step("Отправить GET-запрос несуществующего заказа"):
            response = requests.get(url=f'{BASE_URL}/store/order/9999')

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Not expected status code"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Order not found", "Not expected text"

    @allure.title("Получение инвентаря магазина")
    def test_get_store_inventory(self):
        with allure.step("Отправить GET-запрос на получение инвентаря магазина"):
            response = requests.get(url=f'{BASE_URL}/store/inventory')
            response_json = response.json()

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Not expected status code"

        with allure.step("Валидация JSON-схемы"):
            jsonschema.validate(response_json, INVENTORY_SCHEMA)