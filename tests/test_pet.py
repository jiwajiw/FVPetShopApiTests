import allure
import jsonschema
import pytest
import requests
from .schemas.pet_schema import PET_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"

@allure.feature("Pet")
class TestPet:

    @allure.title("Попытка удалить несуществующего питомца")
    def test_delete_nonexistent_pet(self):
        with allure.step("Отправить DELETE-запрос несуществующего питомца"):
            response = requests.delete(url=f'{BASE_URL}/pet/9999')

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Not expected status code"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet deleted", "Not expected text"

    @allure.title("Попытка обновить несуществующего питомца")
    def test_update_nonexistent_pet(self):
        with allure.step("Отправить PUT-запрос несуществующего питомца"):
            payload = {
                "id": 9999,
                "name": "Non-existent Pet",
                "status": "available"
            }
            response = requests.put(url=f'{BASE_URL}/pet', json=payload)

            with allure.step("Проверка статуса ответа"):
                assert response.status_code == 404, "Not expected status code"

            with allure.step("Проверка текстового содержимого ответа"):
                assert response.text == "Pet not found", "Not expected text"

    @allure.title("Попытка получить информацию о несуществующем питомце")
    def test_get_nonexistent_pet(self):
        with allure.step("Отправить GET-запрос несуществующего питомца"):
            response = requests.get(url=f'{BASE_URL}/pet/9999')

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Not expected status code"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet not found", "Not expected text"

    @allure.title("Добавление нового питомца")
    def test_add_pet(self):
        with allure.step("Подготовка данных для создания питомца"):
            payload = {
                "id": 1,
                "name": "Buddy",
                "status": "available"
            }

        with allure.step("Отправка запроса на создание питомца"):
            response = requests.post(url=f'{BASE_URL}/pet', json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа и валидация JSON-схемы"):
            assert response.status_code == 200, "Not expected status code"
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответе"):
            assert response_json['id'] == payload['id'], "Not expected id"
            assert response_json['name'] == payload['name'], "Not expected name"
            assert response_json['status'] == payload['status'], "Not expected status"

    @allure.title("Добавление нового питомца c полными данными")
    def test_add_pet_all_params(self):
        with allure.step("Подготовка данных для создания питомца"):
            payload = {
                "id": 10,
                "name": "doggie",
                "category": {
                    "id": 1,
                    "name": "Dogs"
                },
                "photoUrls": ["string"],
                "tags": [{"id": 0, "name": "string"}],
                "status": "available"
            }

        with allure.step("Отправка запроса на создание питомца"):
            response = requests.post(url=f'{BASE_URL}/pet', json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа и валидация JSON-схемы"):
            assert response.status_code == 200, "Not expected status code"
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответе"):
            assert response_json['id'] == payload['id'], "Not expected id"
            assert response_json['name'] == payload['name'], "Not expected name"
            assert response_json['category'] == payload['category'], "Not expected category"
            assert response_json['photoUrls'] == payload['photoUrls'], "Not expected photoUrls"
            assert response_json['tags'] == payload['tags'], "Not expected tags"
            assert response_json['status'] == payload['status'], "Not expected status"

    @allure.title("Получение информации о питомце по ID")
    def test_get_pet_by_id(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Отправка запроса на получение информации о питомце по ID"):
            response = requests.get(url=f'{BASE_URL}/pet/{pet_id}')

        with allure.step("Проверка статуса ответа и данных питомца"):
            assert response.status_code == 200, "Not expected status code"
            assert response.json()["id"] == pet_id, "Not expected id"

    @allure.title("Обновление информации о питомце")
    def test_update_id(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Подготовка данных для обновления питомца"):
            payload = {
                "id": pet_id,
                "name": "Buddy Updated",
                "status": "sold"
            }

        with allure.step("Отправка запроса на обновление информации о питомце по ID"):
            response = requests.put(url=f'{BASE_URL}/pet', json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа и данных питомца"):
            assert response.status_code == 200, "Not expected status code"
            assert response_json["id"] == pet_id, "Not expected id"
            assert response_json['status'] == payload['status'], "Not expected status"
            assert response_json['name'] == payload['name'], "Not expected name"

    @allure.title("Удаление питомца по ID")
    def test_delete_pet(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Отправка запроса на удаление информации о питомце по ID"):
            response = requests.delete(url=f'{BASE_URL}/pet/{pet_id}')
            assert response.status_code == 200, "Not expected status code"

        with allure.step("Отправка запроса на получение информации о питомце по ID"):
            response = requests.get(url=f'{BASE_URL}/pet/{pet_id}')
            assert response.status_code == 404, "Not expected status code"

    @allure.title("Получение списка питомцев по статусу")
    @pytest.mark.parametrize(
        "status, expected_status_code",
        [("available", 200), ("pending", 200), ("sold", 200), ("unexisted_status", 400), ("", 400)]
    )
    def test_get_pets_by_status(self, status, expected_status_code):
        with allure.step(f"Отправка запроса на получение питомца по статусу {status}"):
            response = requests.get(url=f'{BASE_URL}/pet/findByStatus', params={"status": status})

        with allure.step("Проверка статуса ответа и формата данных"):
            assert response.status_code == expected_status_code, "Not expected status code"

            response_json = response.json()

            if expected_status_code == 200:
                assert isinstance(response_json, list), "Not expected json"
            else:
                assert isinstance(response_json, dict), "Not expected json"