from flask import Flask, request, jsonify
from ocr import NNRecognizer, IncorrentImageSizeException, InvalidImageException
from http import HTTPStatus

nnRecognizer = NNRecognizer(model_file="nn_model.onnx")

app = Flask(__name__)


@app.before_request
def before_request():
    try:
        content_length = int(request.environ.get('CONTENT_LENGTH', 0))
        assert content_length < 3*1024
    except:
        return (jsonify({
            'error': 'image file too large',
            'result': None
        }), HTTPStatus.REQUEST_ENTITY_TOO_LARGE)


@app.route('/<path:path>', methods=['POST'])
@app.route('/', methods=['POST'])
def upload_file(path=''):
    image_files = request.files.getlist('image')
    if len(image_files) != 1:
        return (jsonify({
            'error': 'invalid request',
            'result': None
        }), HTTPStatus.NOT_ACCEPTABLE)
    image = image_files[0].read()
    try:
        result = nnRecognizer.recognize(image)
    except (IncorrentImageSizeException, InvalidImageException):
        return (jsonify({
            'error': 'invalid image file',
            'result': None
        }), HTTPStatus.UNSUPPORTED_MEDIA_TYPE)
    except:
        return (jsonify({
            'error': 'unexpected error',
            'result': None
        }), HTTPStatus.INTERNAL_SERVER_ERROR)

    return jsonify({
        'error': 'succeed',
        'result': result
    })


if __name__ == "__main__":
    app.run(debug=True)
