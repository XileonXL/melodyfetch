import requests
from flask import Flask, request

# import downloadApiFunctions
from downloadApiFunctions import DownloadApiFunctions
from apiManager import ApiManager

app = Flask(__name__)

downloadApiFunctions = DownloadApiFunctions()

@app.route("/artist", methods=["GET", "POST", "DELETE"])
def manage_artist():
    payload = request.get_json()

    if DownloadApiFunctions.validate_payload(payload, request.path):
        if request.method == 'GET':
            response = downloadApiFunctions.get_artist(payload)
        elif request.method == 'POST':
            response = downloadApiFunctions.insert_artist(payload)
        elif request.method == 'DELETE':
            response = downloadApiFunctions.delete_artist(payload)
        else:
            response = DownloadApiFunctions.build_response(status=400, description=f"Method {request.method} not allowed")
    else:
        response = DownloadApiFunctions.build_response(status=400, description="Payload does not contains 'name': '<ARTIST-NAME>'")

    return ApiManager.encodeResponse(response)

@app.route("/artist/bulk", methods=["POST"])
def insert_artists_bulk():
    payload = request.get_json()

    if DownloadApiFunctions.validate_payload(payload, request.path):
        response = downloadApiFunctions.insert_artists(payload)
    else:
        response = DownloadApiFunctions.build_response(status=400, description="One of the artists in payload does not contains 'name': '<ARTIST-NAME>'")
    return ApiManager.encodeResponse(response)

@app.route("/reset", methods=["POST"])
def reset_database():
    response = downloadApiFunctions.reset_database()
    return ApiManager.encodeResponse(response)

@app.route("/songs", methods=["GET", "POST", "DELETE"])
def manage_songs():
    payload = request.get_json()

    if DownloadApiFunctions.validate_payload(payload, request.path):
        if request.method == 'GET':
            response = downloadApiFunctions.get_songs(payload)
        elif request.method == 'POST':
            response = downloadApiFunctions.insert_songs(payload)
        elif request.method == 'DELETE':
            response = downloadApiFunctions.delete_songs(payload)
        else:
            response = DownloadApiFunctions.build_response(status=400, description=f"Method {request.method} not allowed")
    else:
        response = DownloadApiFunctions.build_response(status=400, description="Payload does not contains 'name': '<ARTIST-NAME>'")

    return ApiManager.encodeResponse(response)




if __name__ == '__main__':
    app.run(debug=True)
