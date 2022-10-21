import time

from flask import Flask, Response

app = Flask(__name__)


@app.route('/')
def long_response():
    def generate():
        for row in range(4):
            yield str(row) + '\n'
            time.sleep(1)
        yield 'Completed\n'
    return Response(generate())
