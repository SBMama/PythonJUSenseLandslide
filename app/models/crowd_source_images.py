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

    def fetch_metadata(self, folder, image):
        metadata = []
        for path in os.listdir(folder):
            filepath = os.path.join(folder, path)
            if os.path.isfile(filepath) and "gitignore" not in filepath:
                data = json.load(open(filepath, 'r', encoding="utf8"))
                data['imageFile'] = os.path.join(image, data['imageFile'])
                metadata.append(data)
        return metadata
