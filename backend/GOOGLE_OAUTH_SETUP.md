GOOGLE OAUTH SETUP INSTRUCTIONS
=============================

1. GO TO GOOGLE CLOUD CONSOLE
----------------------------
- Visit: https://console.cloud.google.com/
- Sign in with your Google account

2. CREATE A NEW PROJECT
----------------------
- Click on the project dropdown at the top → New Project
- Name: Resume Builder
- Click 'Create'

3. ENABLE OAUTH 2.0
------------------
- Select your project
- Go to "APIs & Services" → "OAuth consent screen"
- Choose "External" user type
- Click "Create"

4. CONFIGURE OAUTH CONSENT SCREEN
------------------------------
App Information:
- App name: Resume Builder
- User support email: your-email@domain.com
- Developer contact email: your-email@domain.com

Authorized domains:
- Add your domain (for development: localhost)

5. CREATE OAUTH 2.0 CLIENT ID
---------------------------
- Go to "APIs & Services" → "Credentials"
- Click "Create Credentials" → "OAuth client ID"
- Application type: Web application
- Name: Resume Builder Web Client

Authorized JavaScript origins:
- http://localhost:8000
- http://localhost:3000 (if you have a frontend)

Authorized redirect URIs:
- http://localhost:8000/api/v1/auth/google/callback
- http://localhost:3000/auth/callback (if you have a frontend)

6. GET YOUR CREDENTIALS
---------------------
After creating, you'll get:
- Client ID
- Client Secret
- Save these securely

7. UPDATE YOUR .env FILE
----------------------
# Existing database configuration
POSTGRES_USER=resumeuser
POSTGRES_PASSWORD=Abc@123
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=resumebuilder
DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}

# Add Google OAuth credentials
GOOGLE_CLIENT_ID=your_client_id_here
GOOGLE_CLIENT_SECRET=your_client_secret_here
GOOGLE_REDIRECT_URI=http://localhost:8000/api/v1/auth/google/callback

8. ENABLE GOOGLE APIS
-------------------
- Go to "APIs & Services" → "Library"
- Search for and enable:
  - Google+ API
  - Google People API

9. TESTING THE SETUP
------------------
- Start your application
- Visit: http://localhost:8000/docs
- Try the /api/v1/auth/google endpoint
- You should be redirected to Google login

10. SECURITY NOTES
----------------
- Never commit .env file with credentials
- Use different OAuth credentials for development and production
- Regularly rotate client secrets
- Monitor OAuth usage in Google Cloud Console

TROUBLESHOOTING
--------------
1. If redirect URI doesn't work:
   - Double-check the URI in Google Console matches exactly
   - Ensure no trailing slashes
   - Check for correct protocol (http/https)

2. If authentication fails:
   - Verify credentials in .env
   - Check if APIs are enabled
   - Look for error messages in console

3. Common Issues:
   - Redirect URI mismatch
   - Invalid client ID/secret
   - APIs not enabled
   - Wrong application type
   - Consent screen not configured

ADDITIONAL NOTES
--------------
1. For Production:
   - Use https URLs
   - Add production domain to authorized origins
   - Configure production redirect URIs
   - Set up proper consent screen
   
2. Best Practices:
   - Keep credentials secure
   - Use environment variables
   - Implement proper error handling
   - Add user session management
   - Regular security audits

3. Useful Links:
   - Google Cloud Console: https://console.cloud.google.com/
   - OAuth 2.0 Documentation: https://developers.google.com/identity/protocols/oauth2
   - FastAPI OAuth Documentation: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/

END OF GOOGLE OAUTH SETUP INSTRUCTIONS 