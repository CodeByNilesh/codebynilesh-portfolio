# Security settings for production
if not DEBUG:
    # Don't use SECURE_SSL_REDIRECT on Railway (they handle SSL)
    # SECURE_SSL_REDIRECT = True  # ❌ COMMENTED OUT
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    # SECURE_HSTS_SECONDS = 31536000  # ❌ COMMENTED OUT for now
    # SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    # SECURE_HSTS_PRELOAD = True
