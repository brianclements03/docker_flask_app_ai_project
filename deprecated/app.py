#new flask app.py
from flask import Flask
# from decouple import config
from decouple import AutoConfig

app =  Flask(__name__)
# PORT = config('PORT',default=5000)
# config = AutoConfig(failure_cast=True) #this line seems to be problematic--the failure_cast=True part
config = AutoConfig(search_path='.')

@app.route('/')
def home():
     # return "Hello, Docker!"
     try:
          port = config('PORT')
          return f"Running on port {port}"
     except Exception as e:
          return f"PORT variable missing: {e}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
