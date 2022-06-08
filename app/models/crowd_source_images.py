import json
import os
import uuid

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
        id = str(uuid.uuid4())
        mfilename = "metadata_"+id+".json"
        self.boto_obj.save_metadata_file(payload, request, mfilename)

    def fetch_metadata(self):
        metadata, images = self.boto_obj.fetch_metadata()
        for data in metadata:
            if 'source' not in data:
                data['source'] = ""
        return metadata
