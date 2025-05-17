from fastapi import Security, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from fastapi.security import APIKeyHeader
from fastapi import Query
from fastapi import Request
from jose import JWTError, jwt
bearer_scheme = HTTPBearer()
SECRET_KEY = "rida_kee_secret_key"
ALGORITHM = "HS256"

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

def api_key_dependency(
    api_key: str = Query(None),  # Check for API key in query parameter
    auth_header: str = Security(api_key_header),  # Check for API key in Authorization header
    request: Request = None,  # Check for API key in middleware state
):
    """
    Validate API key passed as a query parameter, Authorization header, or middleware.
    """
    # Extract API key from query parameters, Authorization header, or middleware
    api_key = api_key or (auth_header.split("Bearer ")[1] if auth_header and "Bearer " in auth_header else None)
    api_key = api_key or getattr(request.state, "api_key", None)

    # Raise an error if the API key is not provided
    if not api_key:
        raise HTTPException(status_code=401, detail="API key is missing")

    payload = jwt.decode(api_key, SECRET_KEY, algorithms=[ALGORITHM])
    user_role = payload.get("role")
    if user_role is None:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

    if user_role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")  