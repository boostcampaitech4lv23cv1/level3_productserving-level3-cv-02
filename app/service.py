from PIL import Image 
import io
import os
from argparse import Namespace, ArgumentParser
from constant import fast_dict, slow_dict, paths
import sys 
sys.path.append("..")
sys.path.append(".")
from MusicXML2Audio.main import main as xml2mp3
from constant import BUCKET_URL
from db.service import sound as sound_service
from utils import send_mp3_email

from MusicXML2Audio.main import main as xml2mp3

import urllib
from oemer.ete import extract

def predict_model(db, image_bundle_id):
    img_path = os.path.join(paths['img_path'], image_bundle_id)
    xml_path = os.path.join(paths['xml_path'], image_bundle_id)
    os.makedirs(xml_path)
    mp3_path = os.path.join(paths['mp3_path'], image_bundle_id)
    os.makedirs(mp3_path)
    filename='result'

    results=[]
    for fpath in os.listdir(img_path):
        fname = os.path.join(img_path, fpath)
        fast_dict["img_path"] = fname
        fast_dict["output_path"] = xml_path
        dict_args = Namespace(**fast_dict)
        result_path = extract(dict_args)  
        results.append(result_path)
    
    xml2mp3(filename, xml_path, mp3_path, True, True, False)
    mp3_url = sound_service.upload_sound(db, image_bundle_id)
    
    return mp3_url

def predict_model_hard(address, img_path = paths['img_path'], img_bundle_id = ''):
    img_path = os.path.join(img_path, img_bundle_id)
    xml_path = os.path.join(paths['xml_path'], img_bundle_id)
    mp3_path = os.path.join(paths['mp3_path'], img_bundle_id)
    os.makedirs(xml_path)
    os.makedirs(mp3_path)
    filename='result'

    results=[]  
    
    for fpath in os.listdir(img_path):
        fname = os.path.join(img_path, fpath)
        slow_dict["img_path"] = fname
        slow_dict["output_path"] = xml_path
        dict_args = Namespace(**slow_dict)
        result_path = extract(dict_args)  
        results.append(result_path)
    
    xml2mp3(filename, xml_path, mp3_path, True, True, False)
    mp3_path = os.path.join(mp3_path, f"{filename}_0.mp3")
    
    send_mp3_email(address, img_path, mp3_path)    
    print("전송 완료했습니다.")

if __name__ == "__main__":
    parser =  ArgumentParser()
    parser.add_argument("--address", type=str, help="이메일을 보내기 위한 경로")
    parser.add_argument("--img_path", type=str, default = paths["img_path"], help="이미지가 있는 경로")
    parser.add_argument("--bundle_id", type=str, help="bundle id를 명시하세요")
    args = parser.parse_args() 
    print("args:", args)
    predict_model_hard(args.address, args.img_path, args.bundle_id)
    
    
    