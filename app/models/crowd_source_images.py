import json
import os

from werkzeug.utils import secure_filename

from app.models.boto_crud import BotoCRUD


class CrowdSource:
    """
    this class is to save crowd sourced data
    """
    def __init__(self):
        self.boto_obj = BotoCRUD()

    def save_image(self, file, request):
        filename = ""
        if file:
            file = file['image']
            filename = self.boto_obj.save_image_file(file, request)
        return filename

    def save_metadata(self, payload, filename, request):
        payload['imageFile'] = filename
        mfilename = "metadata_"+filename.split(".")[0]+".json"
        self.boto_obj.save_metadata_file(payload, request, mfilename)

    def fetch_metadata(self, folder, image):
        metadata = []
        for path in os.listdir(folder):
            filepath = os.path.join(folder, path)
            if os.path.isfile(filepath) and "gitignore" not in filepath:
                data = json.load(open(filepath, 'r', encoding="utf8"))
                data['imageFile'] = os.path.join(image, data['imageFile'])
                metadata.append(data)
        return metadata
