from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from google.oauth2 import id_token
from google.auth.transport import requests
from google.auth.exceptions import GoogleAuthError
from app.core.database import get_db
from app.core.config import settings
from app.models.user_models import User
import httpx
from datetime import timedelta
from app.core.security import create_access_token, create_token_pair, verify_token
from typing import Dict

router = APIRouter()

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v1/userinfo"


class GoogleAuthException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


@router.get("/login/google")
async def login_google():
    """Generate Google login URL"""
    try:
        params = {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "response_type": "code",
            "scope": "email profile",
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "prompt": "select_account",
        }

        query_string = "&".join(f"{k}={v}" for k, v in params.items())
        auth_url = f"{GOOGLE_AUTH_URL}?{query_string}"

        return {"auth_url": auth_url}  # Return URL instead of redirecting

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate authentication URL",
        )


@router.get("/callback")
async def auth_callback(
    code: str = None, error: str = None, db: Session = Depends(get_db)
) -> Dict[str, str]:
    """Handle Google OAuth2 callback"""

    # Handle OAuth2 errors
    if error:
        error_details = {
            "access_denied": "User denied access",
            "invalid_request": "Invalid request",
            "invalid_scope": "Invalid scope",
            "server_error": "Server error during authentication",
        }
        raise GoogleAuthException(error_details.get(error, "Authentication failed"))

    if not code:
        raise GoogleAuthException("No authorization code provided")

    try:
        # Exchange code for tokens
        async with httpx.AsyncClient() as client:
            token_response = await client.post(
                GOOGLE_TOKEN_URL,
                data={
                    "client_id": settings.GOOGLE_CLIENT_ID,
                    "client_secret": settings.GOOGLE_CLIENT_SECRET,
                    "code": code,
                    "grant_type": "authorization_code",
                    "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                },
                timeout=10.0,  # Add timeout
            )

            if token_response.status_code != 200:
                raise GoogleAuthException("Failed to obtain access token")

            token_data = token_response.json()

            # Get user info using access token
            user_response = await client.get(
                GOOGLE_USERINFO_URL,
                headers={"Authorization": f"Bearer {token_data['access_token']}"},
                timeout=10.0,
            )

            if user_response.status_code != 200:
                raise GoogleAuthException("Failed to get user info")

            user_data = user_response.json()

        # Verify email domain if needed
        email = user_data.get("email")
        if not email:
            raise GoogleAuthException("Email not provided by Google")

        # Optional: Restrict to specific email domains
        # if not email.endswith("@yourdomain.com"):
        #     raise GoogleAuthException("Email domain not allowed")

        # Check if user exists, create if not
        user = db.query(User).filter(User.email == email).first()
        if not user:
            user = User(
                email=email,
                full_name=user_data.get("name", ""),
                google_id=user_data["id"],
                picture=user_data.get("picture"),
            )
            try:
                db.add(user)
                db.commit()
                db.refresh(user)
            except Exception as e:
                db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Database error while creating user",
                )

        # Create access token
        access_token = create_access_token(
            data={
                "sub": user.email,
                "google_id": user.google_id,
                "full_name": user.full_name,
            }
        )

        # Return token directly instead of redirecting
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "email": user.email,
                "full_name": user.full_name,
                "picture": user.picture,
            },
        }

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Authentication request timed out",
        )
    except httpx.RequestError:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Could not communicate with authentication server",
        )
    except GoogleAuthException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# Add a test endpoint to verify token
@router.get("/verify-token")
async def verify_token(current_user: User = Depends(get_current_user)):
    return {
        "email": current_user.email,
        "full_name": current_user.full_name,
        "picture": current_user.picture,
    }


@router.post("/refresh-token")
async def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    """Refresh access token using refresh token"""
    try:
        # Verify refresh token
        payload = verify_token(refresh_token, "refresh")
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
            )

        # Get user
        user = db.query(User).filter(User.email == payload.get("sub")).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
            )

        # Create new token pair
        access_token, new_refresh_token = create_token_pair(
            {
                "sub": user.email,
                "google_id": user.google_id,
                "full_name": user.full_name,
            }
        )

        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not refresh token"
        )
