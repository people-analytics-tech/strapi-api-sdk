from decouple import config

# API Constants
API_TOKEN = config("STRAPI_API_TOKEN")
API_BASE_URL = config("STRAPI_BASE_URL")

# Request config
TIMEOUT = config("TIMEOUT", default=600, cast=int) # Default set to 600 seconds (10 minutes)
