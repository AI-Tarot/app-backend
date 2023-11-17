from langchain.llms import OpenAI
from src.models import User, TarotCard
from src.tarot_cards import tarot_cards
import random


def pick_random_card() -> TarotCard:
    return random.choice(tarot_cards)

# Initialize the LangChain LLM
llm = OpenAI()

def generate_reading(user: User, card: TarotCard, question: str) -> str:
    # Use LangChain to generate a reading based on user info and selected card
    prompt = f"Given a user with the following attributes: sex: {user.sex}, age: {user.age}, and additional info: '{user.custom_info}', along with their question '{question}' and having drawn the tarot card '{card.name}' with the description '{card.description}', provide a detailed tarot reading."
    response = llm.complete(
        prompt=prompt,
        temperature=0.7,
        max_tokens=150,
    )
    return response["choices"][0]["text"].strip()