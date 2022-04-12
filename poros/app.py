from apps import create_app

app = create_app()


@app.route('/hello', methods=['GET'])
def hello():
    import datetime
    from flask import jsonify
    return  jsonify(datetime.datetime.now())


if __name__ == "__main__":
    app.run()