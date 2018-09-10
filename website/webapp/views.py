from webapp import app
from .images import views as images_views  # noqa: F401


@app.route('/')
def home():
    return 'Welcome to Flask based webclient of Docker!'
