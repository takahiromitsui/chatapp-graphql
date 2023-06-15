import datetime
import bcrypt
import jwt

def encrypt_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_encrypted_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


def generate_token(id:str, secret: str) -> str:
    token = jwt.encode({"id": id,"exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)}, secret, algorithm="HS256")
    return token


def decode_token(token: str, secret: str) -> str:
    try:
        decoded_token = jwt.decode(token, secret, algorithms=["HS256"])
        return decoded_token
    except:
        return "invalid token"
    
# if __name__ == "__main__":
#     # print(generate_token(id="123", secret="secret"))
#     print(decode_token(token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjEyMyIsImV4cCI6MTY4NjkwNjAzMn0.kbeFr-l3wN39RNe0tXLN63fk_QB4vLCusENQA4F2gjc", secret="secret"))