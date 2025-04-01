import io
import logging

import numpy as np
import requests
from flask import Flask, request
from flask import jsonify

from models.plate_reader import PlateReader, InvalidImage
from image_provider_client import ImageProviderClient


app = Flask(__name__)
plate_reader = PlateReader.load_from_file('./model_weights/plate_reader_model.pth')
image_provider_client = ImageProviderClient("http://89.169.157.72:8080/images")


@app.route('/')
def hello():
    user = request.args['user']
    return f'<h1 style="color:red;"><center>Hello {user}!</center></h1>'


# <url>:8080/greeting?user=me
# <url>:8080 : body: {"user": "me"}
# -> {"result": "Hello me"}
@app.route('/greeting', methods=['POST'])
def greeting():
    if 'user' not in request.json:
        return {'error': 'field "user" not found'}, 400

    user = request.json['user']
    return {
        'result': f'Hello {user}',
    }


# <url>:8080/readPlateNumber : body <image bytes>
# {"plate_number": "c180mv ..."}
@app.route('/readPlateNumber', methods=['POST'])
def read_plate_number():
    im = request.get_data()
    im = io.BytesIO(im)

    try:
        res = plate_reader.read_text(im)
    except InvalidImage:
        logging.error('invalid image')
        return {'error': 'invalid image'}, 400

    return {
        'plate_number': res,
    }


@app.route('/readPlateNumberById/<int:img_id>', methods=['GET'])
def read_plate_number_by_image_id(img_id: int):
    logging.debug(f"read_plate_number_by_image_id({img_id})")
    img = image_provider_client.get_image(img_id)
    if isinstance(img, str):
        return {"reason": img}, 400  # Bad Request
    plate_number = plate_reader.read_text(io.BytesIO(img))
    return {"plate_number": plate_number}


@app.route('/readPlateNumberByMultipleIds/<string:img_ids_separated_by_comma>', methods=['GET'])
def read_plate_number_by_multiple_image_ids(img_ids_separated_by_comma: str):
    logging.debug(f"recognize_multiple_images({img_ids_separated_by_comma})")
    try:
        img_ids = list(map(int, img_ids_separated_by_comma.split(",")))
    except Exception as ex:
        return {"reason": repr(ex)}, 422  # Unprocessable Entity
    ing_id_to_bytes = {}
    for img_id in img_ids:
        img = image_provider_client.get_image(img_id)
        if isinstance(img, str):
            return {"reason": img}, 400  # Bad Request
        ing_id_to_bytes[img_id] = img
    img_id_to_plate_number = {}
    for img_id, bytes in ing_id_to_bytes.items():
        img_id_to_plate_number[img_id] = plate_reader.read_text(io.BytesIO(bytes))
    return img_id_to_plate_number


if __name__ == '__main__':
    logging.basicConfig(
        format='[%(levelname)s] [%(asctime)s] %(message)s',
        level=logging.INFO,
    )

    app.config['JSON_AS_ASCII'] = False
    app.run(host='0.0.0.0', port=8080, debug=True)
