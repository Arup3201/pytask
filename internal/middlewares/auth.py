from fastapi import Header, Depends, HTTPException
from typing import Annotated
from internal.utils import TokenUtil
from internal.dependencies import get_token_util
from internal.exceptions import TokenVerificationError

def get_current_user_id(token_util: TokenUtil = Depends(get_token_util), 
                        authorization: Annotated[str, Header()] = "") -> str:
    
    auth_h_splitted = authorization.split(" ")
    
    if len(auth_h_splitted) != 2:
        raise HTTPException(status_code=400, detail="Malformed token")
    elif auth_h_splitted[0] != "Bearer":
        raise HTTPException(status_code=400, detail="Token should be in 'Bearer token' format")
    
    try:
        claims = token_util.verify_token(auth_h_splitted[1])
    except TokenVerificationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Token verification failed")
    else:
        return claims.sub
    
