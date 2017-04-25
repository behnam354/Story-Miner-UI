from flask import Flask
#import ui_test_outputDF
import os

app = Flask(__name__)

@app.route("/")
def hello():
    df = execfile("ui_test_outputDf.py")
    return df
    #return os.system("ui_test_outputDf.py")

if __name__ == "__main__":
    app.run()
