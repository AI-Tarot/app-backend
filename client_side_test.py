import requests
from src.models import User
from src.readings import pick_random_card
from datetime import datetime


test_user = User(username='John Smith', sex = 'male', age = 29, custom_info="Married, has 2 kids")
response_1 = requests.post(
    "http://localhost:8000/register/",
    json = test_user.dict()
)
print(f'request 1: {test_user.dict()}')
print(f'response 1:{response_1.json()["content"]}')


card = pick_random_card()
date = datetime.today().strftime('%Y-%m-%d')
test_question = "Is today a good day for a trip?"
request_2 = {
    "username": "John Smith",
    "question": test_question,
    "card_name": card.name,
    "date": date
}
response_2 = requests.post(
    "http://localhost:8000/get_reading/",
    json = request_2
)

print(f'request 2: {request_2}')
print(f'response 2:{response_2.json()["content"]}')