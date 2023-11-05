from SQLiteDAO import SQLiteDAO
from exceptionHandler import NotFoundError

class DownloadApiFunctions:
    API_KEY = "04003e6048d9a7ad9dfc1755c49f07e5"
    SHARED_SECRET = "d3de495af61411c5adb4c4fd3763491e"
    API_BASE_URL = "http://ws.audioscrobbler.com/2.0/"
    db = SQLiteDAO("database.db")
    
    def __init__(self):
        self.db.connect()

    def __del__(self):
        self.db.disconnect()

    def insert_artist(self, payload):
        try:
            self.db.insert_row("artists", payload)
            status = 200
            description = f"Artist {payload['name']} inserted successfully"
        except Exception as e:
            status = 409
            description = f"Error when inserting artist {payload['name']}: {e}"
        return self.build_response(status=status, description=description)
    
    def insert_artists(self, payload):
        payload["name"] = payload["name"].capitalize()
        try:
            self.db.insert_rows("artists", payload)
            status = 200
            description = f"Artists {payload['name']} inserted successfully"
        except Exception as e:
            status = 500
            description = f"Error when inserting artist {payload['name']}: {e}"
        return self.build_response(status=status, description=description)
    
    def insert_songs(self, payload):
        artist_name = {
            "name": payload["artist_name"]
        }
        artist_id, _ = self.db.get_rows("artists", artist_name)[0]
        for song in payload["songs"]:
            song_info = {
                "artist_id": artist_id,
                "title": song.capitalize(),
            }
            try:
                self.db.insert_row("songs", song_info)
                status = 200
                description = f"Songs {payload} inserted successfully"
            except Exception as e:
                status = 409
                description = f"Error when inserting songs {payload}: {e}"
        return self.build_response(status=status, description=description)

    def get_artist(self, payload):
        try:
            result = self.db.get_rows("artists", payload)
            if result:
                response = self.build_response(200, "OK", result)
            else:
                response = self.build_response(404, f"Artist {payload['name']} was not found")
        except Exception as e:
            response = self.build_response(500, f"Error when getting artist {payload['name']}: {e}")
        return response
    
    def get_songs(self, payload):
        artist_name = {
            "name": payload["artist_name"]
        }
        artist_id, _ = self.db.get_rows("artists", artist_name)[0]
        song_info = {
            "artist_id": artist_id
        }
        try:
            result = self.db.get_rows("songs", song_info)
            if result:
                response = self.build_response(200, "OK", result)
            else:
                response = self.build_response(404, f"Artist {payload['name']} was not found")
        except Exception as e:
            response = self.build_response(500, f"Error when getting artist {payload['name']}: {e}")
        return response
    
    def delete_songs(self, payload):
        artist_name = {
            "name": payload["artist_name"]
        }
        artist_id, _ = self.db.get_rows("artists", artist_name)[0]
        song_info = {
            "artist_id": artist_id
        }
        if "songs" in payload:

            
        try:
            self.db.delete_rows("songs", song_info)
            status = 200
            description = f"Artist {payload['name']} deleted successfully"
        except Exception as e:
            status = 400
            description = f"Error deleting artist {payload['name']}: {e}"
        return self.build_response(status=status, description=description)
    
    def delete_artist(self, payload):
        try:
            self.db.delete_rows("artists", payload)
            status = 200
            description = f"Artist {payload['name']} deleted successfully"
        except Exception as e:
            status = 400
            description = f"Error deleting artist {payload['name']}: {e}"
        return self.build_response(status=status, description=description)
    
    def reset_database(self):
        try:
            self.db.reset_database()
            status = 200
            description = f"DB restored successfully"
        except Exception as e:
            status = 500
            description = f"Error restoring database: {e}"
        return self.build_response(status=status, description=description)

    @staticmethod
    def validate_payload(payload, path):
        valid_payload = True
        return valid_payload

    @staticmethod
    def build_response(status=200, description="OK", data=None):
        response = {
            "status": status,
            "description": description
        }
        if data:
            response['data'] = data
        return response

# payload = {
#     "method": "artist.gettoptracks",
#     "artist": "Saiko",
#     "api_key": API_KEY,
#     "format": "json"
# }
#
# r = requests.get(API_BASE_URL, params=payload)
#
# r_json = r.json()
#
# tracks = []
# for track in r_json["toptracks"]["track"]:
#     tracks.append({
#         "artist_name": track["artist"]["name"],
#         "song_name": track["name"]
#     })
#
# for t in tracks:
#     print(t)
