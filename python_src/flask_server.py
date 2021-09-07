import json
from flask import Flask, request, jsonify

import uuid

import Sample as S

app = Flask(__name__)

sample = S.Sample()

@app.route('/api/get_samples/', methods=['GET'])
def get_samples():
    # content = request.json
    # print(content)
    samples = sample.query_unread()
    samples = list(map(lambda s: {'timestamp': int(s['timestamp']), 'values': s['values']}, samples))
    return jsonify({"samples":samples})

@app.route('/api/get_number_samples/', methods=['GET'])
def get_number_samples():
    # content = request.json
    # print(content)
    samples = sample.query_unread()
    return jsonify({"number_of_samples": len(samples)})

@app.route('/api/put_sample/<timestamp>', methods=['PUT'])
def put_sample(timestamp):
    payload = request.json
    # print(payload)

    put_sample = sample.make_sample(payload)
    if put_sample != None:
        sample.write(put_sample)

    return jsonify({"timestamp":timestamp})

@app.route('/api/mark_sample/<timestamp>', methods=['PUT'])
def mark_read(timestamp):
    # payload = request.json
    # print(payload)
    put_sample = sample.mark_read(timestamp, True)

    return jsonify({"timestamp":timestamp})

@app.route('/api/unmark_sample/<timestamp>', methods=['PUT'])
def unmark_read(timestamp):
    # payload = request.json
    # print(payload)
    put_sample = sample.mark_read(timestamp, False)

    return jsonify({"timestamp":timestamp})

if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=6789, debug=True)