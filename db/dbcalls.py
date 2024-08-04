from log.logger import log
import certifi
import datetime as dt
import os
from pydantic import SecretStr
from pymongo.mongo_client import MongoClient
from pymongo.collation import Collation
from models.Models import NewUser, User, Part, Sentiment


#Mongodb connection and data collection function
def connection()->MongoClient|str:
    """Creates the connection needed to access the database."""
    try:
        pword = os.environ['KEY1']
        uri = f"mongodb+srv://temp:{pword}@sentixai.tyiq05h.mongodb.net/?retryWrites=true&w=majority&appName=SentixAI"
        client = MongoClient(uri, tlsCAFile=certifi.where())
        return client
    except Exception as e:
        log(f'Mongo Connection: {e}')


#Get existing user information function
def getuser(client: MongoClient, username: str, password: SecretStr)->tuple[bool, Collation]|tuple[bool,str]:
    """Returns an instance of a user or an error."""
    db = client['SentixAI']
    collection = db['Users']
    try:
        data = collection.find_one({'username': username, 'password': password}, {'password':0, 'repassword':0, 'age':0})
        log('Data collected and returned')
        user = User(**dict(data))
        return True, user
    except Exception as e:
        log(f'Get User Error: {e}')
        return False, f'No user found with this username/password'


#Create a new user fuction
def createuser(client: MongoClient, data: dict)->bool|str:
    """Creates a new user and stores the information in the database."""
    db = client['SentixAI']
    collection = db['Users']
    try:
        newuser = NewUser(**data)            

    except Exception as e:
        log(f'User Data Input Error: {e}')
        return f'User Data Input Error: {e}'
        
    
    try:
        collection.insert_one(newuser.__dict__)
        log('Successfully created the user')
        return True
    except Exception as e:
        log(f'Create User Error: {e}')
        return f'Create User Error: {e}'


def createpart(client: MongoClient, data: dict)->tuple[bool,str]|tuple[bool,str]:
    """Creates a new part and stores the information in the database."""
    db = client['SentixAI']
    collection = db['Parts']
    try:
        part = Part(**data)
    except Exception as e:
        log(f'Part Data Input Error: {e}')
        return f'Part Data Input Error: {e}'
    try:
        collection.insert_one(part.__dict__)
        log('Successfully created the part')
        return True, 'Part create successfully'
    except Exception as e:
        log(f'Create Part Error: {e}')
        return False, f'Create Part Error: {e}'


def getallparts(client: MongoClient, company:str):
    """Retrieves all parts from the database based on the company."""
    db = client['SentixAI']
    collection = db['Parts']
    try:
        data = collection.find({'company': company}, {'partname'})
        log('Part data collected and returned')
        parts = [i['partname'] for i in data]
        return True, parts
    except Exception as e:
        log(f'Get Parts Error: {e}')
        return False, f'No parts found with company: {e}'



def recordsentiment(client: MongoClient, data:dict)->tuple[bool,str]:
    """Records the performed sentimet analysis"""
    db = client['SentixAI']
    collection = db['Analysis']
    try:
        sentiment = Sentiment(**data)
    except Exception as e:
        log(f'Sentiment Anlysis Error: {e}')
        return False, f'Sentiment Anlysis Error: {e}'
    try:
        collection.insert_one(sentiment.__dict__)
        return True, 'Sentiment recorded'
    except Exception as e:
        log(f'Sentiment Analysis Upload Error: {e}')
        return False, f'Sentiment Analysis Upload Error: {e}'
    

def sentimentoverview(client: MongoClient, company:str, productname:str, start_date:dt.datetime, end_date:dt.datetime):
    """Retrieves the full history of sentiment anlaysis"""
    db = client['SentixAI']
    collection = db['Analysis']
    try:
        query = { "timestamp": { "$gte": start_date, "$lte": end_date }, "company": company, "productname": productname }
        sentiments = collection.find(query, {'_id':0, 'tasks': 0})
        log('Part data collected and returned')
        return True, sentiments
    except Exception as e:
        log(f'Get Parts Error: {e}')
        print(e)
        return False, f'No parts found with company: {e}'