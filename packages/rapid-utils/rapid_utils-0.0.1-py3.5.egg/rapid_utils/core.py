import requests
import uuid
from urllib.parse import unquote

def allowed_file(filename, formats):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in formats

def download_file(url, dirname=".", add_prefix=False):
    if add_prefix:
        filename = unquote('/'.join([dirname, uuid.uuid1().hex + url.split("/")[-1]]))
    else:
        filename = unquote('/'.join([dirname, url.split("/")[-1]]))
    file = requests.get(url, stream=True)
    with open(filename,"wb") as f:
        for chunk in file.iter_content(chunk_size=512 * 1024): 
            if chunk:
                f.write(chunk)
    return filename