import jwt
from uuid import uuid4
from datetime import datetime, timedelta, timezone
from django.conf import settings


def generate_token(user):
    payload = {
        'user_id': user.id,
        'exp': datetime.now(timezone.utc) + timedelta(hours=settings.JWT_EXPIRE_HOURS),
        'token_uid': str(uuid4())
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

    return token
