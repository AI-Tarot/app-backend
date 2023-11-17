from typing import List
from fastapi import FastAPI, Depends, HTTPException
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.models import User

# 1. Chain definition
template = """You are AI Tarot card reader. 
You possess great knowledge and wisdom and enchanced by magical powers. 
You can give accurate readings of specific tarot cards for users and answer on user's question.
You will be provided with information about user, today's date, chosen Tarot card and user's question.
You will provide reading based on given information. 
Reading must contain 10 sentences."""
human_template = "Now give explanations and readings for user who just pick his card of the day and thats card is {card}, today's date is {date}, and user is {age} year old {sex}. {custom_info}. User's question is: {question} "

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", template),
    ("human", human_template),
])

model = ChatOpenAI(model_name="gpt-3.5-turbo")

get_reading_chain = chat_prompt | model

# 2. App definition
app = FastAPI(
  title="LangChain Server",
  version="1.0",
  description="A simple api server using Langchain's Runnable interfaces",
)

# DB setup

DATABASE_URL = "sqlite:///./tarot_db.db"
Base = declarative_base()

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    sex = Column(String)
    age = Column(Integer)
    custom_info = Column(String)


# Create the database tables
try:
    Base.metadata.create_all(bind=engine)
except:
    print('tables not created')

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register/")
async def register_user(user: User, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    new_user = UserModel(username=user.username, sex=user.sex, age=user.age, custom_info=user.custom_info)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"username": new_user.username}

@app.post("/get_reading")
async def get_tarot_reading(request:dict, db: Session = Depends(get_db)):
    username = request["username"]
    question = request["question"]
    card_name = request["card_name"]
    date = request["date"]

    # Authenticate the user
    db_user = db.query(UserModel).filter(UserModel.username == username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Username not found")

    updated_human_template = human_template.format(
        card=card_name,  # Example card, replace with actual card
        date=date,  # Example date, replace with actual date
        age=db_user.age,
        sex=db_user.sex,
        custom_info=db_user.custom_info,
        question=question
    )

    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", template),
        ("human", updated_human_template),
    ])

    model = ChatOpenAI(model_name="gpt-3.5-turbo")
    get_reading_chain = chat_prompt | model

    # Execute the chain to get the reading
    input = {
        "card":card_name,  
        "date":date,  
        "age":db_user.age,
        "sex":db_user.sex,
        "custom_info":db_user.custom_info,
        "question":question
        }
    response = get_reading_chain.invoke(input)
    return response



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)