from flask import Flask # Flask class from flask module
app=Flask(__name__) #instance of Flask class

@app.route('/')   #decorator   # '/' indicates the root URL of your application
def hello_world():
    return 'hello world'

# app.run(host='localhost' , port=5000)
if __name__ =='__main__':
    app.run() # Start the server
    #app.run(debug=True)  # Start the server with debug mode enabled



# from flask import Flask
# app=Flask(__name__)

# @app.route('/')
# def home():
#     return "hello"

# if __name__=='__main__':
#     app.run(debug=True)
