from src.server import create_app

app = create_app()

@app.route('/',methods=["GET"])
def getHello():
    return {"message": "Hello World!"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=3333,debug=True,load_dotenv=True)