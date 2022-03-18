import vk_captchasolver as vc
from random import randint
import requests
import random
import time
import sys


token_vk = "TOKEN"

message = "TEXT"

while True:
    if True:

        user = input("Введите ссылку: ")

        try:
            messages = input('Сколько постов создать: ')
            messages = int(messages)
            messages += 1
        except:
            print('Количество сообщений должно быть числом')
            sys.exit()

        def deleting_characters(users):
            parts = users.split("/")

            if users.lower().startswith(("https://", "http://")):
                user_name = parts[3]
                get_user_id(user_name)

            elif users.lower().user.startswith("vk.com/"):
                user_name = parts[1]
                get_user_id(user_name)

            else:
                print("❌ Неверная ссылка ❌")
                sys.exit()

        def get_user_id(user_name):

            data_get_user_id = {
                "user_ids": user_name,
                "access_token": token_vk,
                "v": "5.131"
            }

            response = requests.post("https://api.vk.com/method/users.get", data = data_get_user_id)
            data = response.json()
            if not data["response"]:
                print("❌ Неверный ид, проверьте ссылку ❌")
                sys.exit()

            else:
                user_id = data["response"][0]["id"]
                print(f"ID: {user_id}")
                for i in range(1, messages):
                    create_post(user_id)
            print(data)

        def create_post(user_id):
            data_create_post = {
                "access_token": token_vk,
                "owner_id": user_id,
                "message": message,
                "v": "5.131"
            }

            response = requests.post("https://api.vk.com/method/wall.post", data=data_create_post)
            creates_post = response.json()
            print(creates_post)
            if "response" in creates_post:
                print(f"✅ Создал пост на странице: {user}")

            elif "error" in creates_post:
                if creates_post["error"]["error_code"] == 14:
                    print("❌ КАПЧА")

                    captcha_img = creates_post["error"]["captcha_img"]
                    img = requests.get(captcha_img)
                    file = open("captcha.png", "wb")
                    file.write(img.content)
                    file.close()
                    captcha_answer = vc.solve(image="captcha.png")

                    captcha_sid = creates_post["error"]["captcha_sid"]
                    data_captcha = {
                        "access_token": token_vk,
                        "owner_id": user_id,
                        "message": message,
                        "captcha_sid": captcha_sid,
                        "captcha_key": captcha_answer,
                        "v": "5.131"
                    }

                    requests.post("https://api.vk.com/method/wall.post", data=data_captcha)

                elif creates_post["error"]["error_code"] == 9:
                    print("❌ ФЛУД")
                    print(creates_post)

                elif creates_post["error"]["error_code"] == 29:
                    print("Достигнут количественный лимит на вызов метода"
                          "Подробнее об ограничениях на количество вызовов см. на странице "
                          "https://vk.com/dev/data_limits")
                    print(creates_post)

                elif creates_post["error"]["error_code"] == 214:
                    print("❌ МНОГО ПОСТОВ")
                    print(creates_post)

                elif creates_post["error"]["error_code"] == 5:
                    print("❌ ТОКЕН НЕ РАБОТАЕТ")
                    print(creates_post)

                else:
                    print("❌ НЕИЗВЕСТНАЯ ОШИБКА")
                    print(creates_post)

        if __name__ == "__main__":
            deleting_characters(user)
