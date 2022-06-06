import json
import os

from werkzeug.utils import secure_filename


class CrowdSource:
    """
    this class is to save crowd sourced data
    """

    def save_image(self, file, folder):
        if file:
            file = file['image']
            file.save(os.path.join(folder, secure_filename(file.filename)))

    def save_metadata(self, payload, file, folder):
        imageFile = file['image'].filename if file else ""
        payload['imageFile'] = imageFile
        filename = "metadata_"+imageFile+".json"
        f = open(os.path.join(folder, filename), "w")
        json.dump(payload, f)