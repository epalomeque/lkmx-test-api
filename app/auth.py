import os
import json
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
from urllib.request import urlopen
from dotenv import load_dotenv

load_dotenv()

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_API_AUDIENCE = os.getenv("AUTH0_API_AUDIENCE")
AUTH0_ALGORITHMS = os.getenv("AUTH0_ALGORITHMS", "RS256").split(",")

class VerifyToken:
    def __init__(self):
        jwks_url = f'https://{AUTH0_DOMAIN}/.well-known/jwks.json'
        self.jwks = json.loads(urlopen(jwks_url).read())

    def verify(self, token: str):
        try:
            unverified_header = jwt.get_unverified_header(token)
        except Exception as e:
            raise HTTPException(status_code=401, detail="Invalid header")

        rsa_key = {}
        for key in self.jwks['keys']:
            if key['kid'] == unverified_header['kid']:
                rsa_key = {
                    'kty': key['kty'],
                    'kid': key['kid'],
                    'use': key['use'],
                    'n': key['n'],
                    'e': key['e']
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=AUTH0_ALGORITHMS,
                    audience=AUTH0_API_AUDIENCE,
                    issuer=f'https://{AUTH0_DOMAIN}/'
                )
                return payload
            except jwt.ExpiredSignatureError:
                raise HTTPException(status_code=401, detail="Token expired")
            except jwt.JWTClaimsError:
                raise HTTPException(status_code=401, detail="Invalid claims")
            except Exception:
                raise HTTPException(status_code=401, detail="Unable to parse authentication token")
        raise HTTPException(status_code=401, detail="Invalid token")

token_auth_scheme = HTTPBearer()

def get_current_user(token: HTTPAuthorizationCredentials = Depends(token_auth_scheme)):
    # En un entorno real, no inicializaríamos VerifyToken en cada llamada.
    # Pero para este ejemplo sirve.
    result = VerifyToken().verify(token.credentials)
    return result
