import os
from pathlib import Path

default_dict = dict(
    output_path = "./",
    use_tf = False,
    without_deskew = True,
    save_cache = False
)

fast_only_dict = dict(thresh = 768, step_size = 256)
slow_only_dict = dict(thresh = 2048,step_size = 128)

fast_dict = {**default_dict, **fast_only_dict}
slow_dict = {**default_dict, **slow_only_dict}

paths = {'img_path': '../image',
         'xml_path': '../xml',
         'mp3_path': '../sound'}

BUCKET_NAME = "maestro-bucket1"
BUCKET_URL = "https://storage.googleapis.com/maestro-bucket1/"

#(TODO) DB로 바꿔야함.
MODULE_PATH = "../oemer"

DEFAULT_EMAIL = "unkwon@unkwon.com"


for k,v in paths.items():
    if not os.path.exists(v):
        os.makedirs(v, exist_ok = True)
