from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, decode_token
from flask import redirect, url_for
from flask import request, make_response
from datetime import datetime, timezone, timedelta

def jwt_view_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request(locations=["cookies"])  # checks access token in headers or cookies
        except:
            # Access token missing or expired → try refresh token
            refresh_token = request.cookies.get("refresh_token_cookie")
            if not refresh_token:
                return redirect(url_for("login_page")) # redirect to login if refresh token invalid/expired
            
            try:
                decoded = decode_token(refresh_token)
                # # Optional: check expiration manually
                # exp = datetime.fromtimestamp(decoded["exp"], tz=timezone.utc)
                # if exp < datetime.now(tz=timezone.utc):
                #     return redirect(url_for("login"))

                # Refresh token is valid → issue new access token
                user_identity = decoded["sub"]
                from flask_jwt_extended import create_access_token
                new_access = create_access_token(identity=user_identity, expires_delta=timedelta(minutes=15))

                # Set new access token cookie
                resp = make_response(fn(*args, **kwargs))
                resp.set_cookie("access_token_cookie", new_access, httponly=True, samesite="Lax")
                return resp
            
            except Exception:
                # Refresh token invalid → redirect to login
                return redirect(url_for("login_page"))
  
        return fn(*args, **kwargs)
    return wrapper
