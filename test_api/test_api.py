import requests
import uuid

ENDPOINT = "http://127.0.0.1:8000/api"

def test_can_create_user():
    """ Создание нового пользователя
    
    Сначал получаем данные
    Потом отправляем запрос и тестим по статус коду
    """
    user_payload = new_user_payload()
    create_user_response = create_user(user_payload)
    assert create_user_response.status_code == 201
    
def test_user_login():
    """ Тест Логин юзера
    
    Сначал создаем нового юзера
    Потом отправляем запрос чтобы логинится
    """
    user_payload = new_user_payload()
    create_user_response = create_user(user_payload)
    assert create_user_response.status_code == 201
    
    data = create_user_response.json()
    email = user_payload["email"]
    password = "Astana2024"
    login_user_response = login_user(
        {
            "email": email,
            "password": password
        }
    )
    assert login_user_response.status_code == 200
    
def test_info_user():
    """ Тест Профиль юзера
    
    Сначал создаем нового юзера
    Потом получаем токен от json данных
    Отправляем запрос через токен к эндпойнту
    """
    user_payload = new_user_payload()
    create_user_response = create_user(user_payload)
    assert create_user_response.status_code == 201
    
    email = user_payload["email"]
    name = user_payload["name"]
    
    token = create_user_response.json()["token"]["access"]
    header = {
        "Authorization": f"Bearer {token}"
    }
    get_profile_response = info_user(header=header)
    data = get_profile_response.json()
    assert email == data["email"]
    assert name == data["name"]
    
def test_can_create_board():
    """ Тест для создания досок
    
    Создаем нового юзера
    Получаем токен
    получаем данные для новой доски
    Отправляем запрос и проверяем
    
    """
    user_payload = new_user_payload()
    create_user_response = create_user(user_payload)
    assert create_user_response.status_code == 201
    
    token = create_user_response.json()["token"]["access"]
    header = {
        "Authorization": f"Bearer {token}"
    }
    
    board_payload = new_board_payload()
    create_board_response = create_board(board_payload, header)
    assert create_board_response.status_code == 200
    
    data = create_board_response.json()
    board_id = data["id"]
    get_board_response = get_board(board_id, header)
    assert get_board_response.status_code == 200
    get_board_data = get_board_response.json()
    assert get_board_data["name"] == board_payload["name"] 
    

    
def create_user(payload):
    """ Send request for create user """
    return requests.post(ENDPOINT + "/user/register/", json=payload)

def login_user(payload):
    """ Send request for login user """
    return requests.post(ENDPOINT + "/user/login/", json=payload)

def info_user(header):
    """ Send request for profile user """
    return requests.get(ENDPOINT + "/user/profile/", headers=header)

def create_board(payload, header):
    """ Send request for create board """
    return requests.post(ENDPOINT + "/v1/board", json=payload,  headers=header)

def get_board(board_id, header):
    """ Send request for get board with id """
    return requests.get(ENDPOINT + f"/v1/board/{board_id}",  headers=header)

def new_user_payload():
    """Создание данных для нового пользователя
    
    Используем uuid чтобы каждый генерировать рандомные символы
    """
    email = f"email_{uuid.uuid4().hex}@gmail.com"
    username = f"username_{uuid.uuid4().hex}"
    payload = {
        "email": email,
        "name": username,
        "password": "Astana2024",
        "password2": "Astana2024"
    }
    return payload
    
    
def new_board_payload():
    """Создание данных для новой доски
    
    Используем uuid чтобы каждый генерировать рандомные символы
    """
    name = new_board_name()
    payload = {
        'name': name,
    }
    return payload


def new_board_name():
    return f"test_board_{uuid.uuid4().hex}"