import allure
import requests

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