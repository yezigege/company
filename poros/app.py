from apps import create_app

app = create_app()


@app.route('/hello', methods=['GET'])
def hello():
    return "Hello World!"


if __name__ == "__main__":
    app.run()