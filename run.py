# run the app
from app import app
app.run(host = app.config['LOCAL_HOST'], port = app.config['LOCAL_PORT'], debug = True)
