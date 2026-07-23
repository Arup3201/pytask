import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timezone, timedelta
from typing import Tuple
from internal.dataclasses import JWTClaim
from internal.exceptions import TokenVerificationError

class TokenUtil:
    def __init__(self, key: str, alg: str):
        self.secret_key = key
        self.algorithm = alg

    def generate_token(self, user_id: str, email: str) -> Tuple[str, datetime]:
        now = datetime.now(tz=timezone.utc)
        exp = now+timedelta(days=1)
        payload = JWTClaim(sub= user_id, email= email, iat= now, exp=exp)
        return jwt.encode(payload.__dict__, 
                          self.secret_key, 
                          self.algorithm), exp
    
    def verify_token(self, token: str) -> JWTClaim:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except ExpiredSignatureError:
            raise TokenVerificationError("Token has expired.")
        except InvalidTokenError:
            raise TokenVerificationError("Token is invalid")
        except Exception:
            raise
        else:
            if "sub" not in payload or "email" not in payload:
                raise TokenVerificationError("Token has missing field values.")

            return JWTClaim(sub=payload["sub"], 
                            email=payload["email"], 
                            iat=payload["iat"], 
                            exp=payload["exp"])
