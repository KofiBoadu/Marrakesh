from flask_caching import Cache
from flask_login import LoginManager

cache = Cache(config={'CACHE_TYPE': 'simple'})

login_manager = LoginManager()
