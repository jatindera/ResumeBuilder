from fastapi import Depends, HTTPException, status, Security
from fastapi.security import OAuth2AuthorizationCodeBearer
from google.oauth2 import id_token
from google.auth.transport import requests
from app.core.config import settings
from app.models.user import User
from sqlalchemy.orm import Session
from app.db.session import get_db
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://accounts.google.com/o/oauth2/v2/auth",
    tokenUrl="https://oauth2.googleapis.com/token",
)

async def get_current_user(
    token: str = Security(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    try:
        # Log the received token (first 10 characters for security)
        logger.info(f"Received token starting with: {token[:10]}...")
        
        # For debugging purposes, let's try to decode the token first
        try:
            # Verify Google token
            idinfo = id_token.verify_oauth2_token(
                token, 
                requests.Request(), 
                settings.GOOGLE_CLIENT_ID
            )
            logger.info(f"Token verification successful. Email: {idinfo.get('email', 'No email found')}")
            
            # Get user from database or create if doesn't exist
            user = db.query(User).filter(User.email == idinfo['email']).first()
            if not user:
                logger.info(f"Creating new user with email: {idinfo['email']}")
                user = User(email=idinfo['email'])
                db.add(user)
                db.commit()
                db.refresh(user)
                logger.info("New user created successfully")
            else:
                logger.info(f"Existing user found with email: {idinfo['email']}")
            
            return user

        except ValueError as ve:
            logger.error(f"Token verification failed: {str(ve)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token: {str(ve)}",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
    except Exception as e:
        logger.error(f"Authentication error: {str(e)}")
        # Log the full error for debugging
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Optional: Add a test function to verify token manually
async def verify_token_manually(token: str):
    try:
        idinfo = id_token.verify_oauth2_token(
            token, 
            requests.Request(), 
            settings.GOOGLE_CLIENT_ID
        )
        return {"status": "success", "token_info": idinfo}
    except Exception as e:
        return {"status": "error", "message": str(e)} 