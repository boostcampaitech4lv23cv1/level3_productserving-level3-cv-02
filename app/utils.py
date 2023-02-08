import bcrypt
import random
import string
import smtplib, ssl
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.encoders import encode_base64

from PIL import Image 
import io
import os
from constant import paths
from db.session import bucket

try:
    from secret import ID, TOKEN
except:
    print("예외가 발생했습니다. secret.py를 만들어 Gmail ID, PWD를 명시하세요.")

def hashpw(pw: str):
    return bcrypt.hashpw(password=pw.encode('iso-8859-1'), salt=bcrypt.gensalt())

def checkpw(inputpw: str, dbpw: str):
    return bcrypt.checkpw(inputpw.encode('utf-8'), dbpw.encode('utf-8'))

def randChar(num: int):
    return ''.join(random.choice(string.ascii_letters+string.digits) for _ in range(num))

def send_email(address: str) -> str:
    rand_number = "".join([str(random.randint(0,9)) for _ in range(6)])
    sender_email = ID 
    receiver_email = address
    password = TOKEN 
    
    message = MIMEMultipart("alternative")
    message["Subject"] = f"Maestro 회원가입 인증용 번호는 {rand_number}입니다."
    message["From"] = sender_email 
    message["To"] = receiver_email  
    
    html = f"""
    <h1> 안녕하세요, 고객님! <h1>
    <h2> Maestro 서비스를 이용해주셔서 감사합니다.</h2>
    <div class="check">
      <h2 class="display1"> Email Verification</h2>
      <div class="display2">
        <h4 class="text"> 인증용 번호는 {rand_number}입니다.</h4>
        <h4 class="text"> 5분안에 번호를 입력해주세요!</h4>
      </div>
    """
    
    html_part = MIMEText(html, "html")
    message.attach(html_part)
    context = ssl.create_default_context()
    
    print("메일을 보내는 중입니다...")
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )
    
    return rand_number

def send_mp3_email(address: str, img_path:str = None , mp3_path: str = None) -> str:
    sender_email = ID 
    receiver_email = address
    password = TOKEN 
    
    message = MIMEMultipart("alternative")
    message["Subject"] = f"[Maestro] 신청하신 mp3 파일입니다."
    message["From"] = sender_email 
    message["To"] = receiver_email  
    
    html = f"""
    <h1> 안녕하세요, 고객님! <h1>
    <h2> Maestro 서비스를 이용해주셔서 감사합니다.</h2>
    <h4> 예약해주셨던 사진과 파일명입니다.</h4>
    <h4> 데모버전인 관계로 정확도가 떨어질 수 있으나, 예쁘게 봐주시면 감사하겠습니다!</h4>
    """
    html_part = MIMEText(html, "html")
    message.attach(html_part)
    
    
    #Attach files
    files = []
    if img_path is not None:
        for file in os.listdir(img_path):
            fname = os.path.join(img_path, file)
            files.append(fname)
    if mp3_path is not None:
        files.append(mp3_path)
    
    for file in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(file, "rb").read())
        encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file))
        message.attach(part)
    
    context = ssl.create_default_context()
    
    print("메일을 보내는 중입니다...")
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )
    
    return True

















def save_images(images, id):
    IMAGE_PATH = os.path.join(paths['img_path'], id)
    os.makedirs(IMAGE_PATH)

    for order, image_file in enumerate(images):
        image = Image.open(io.BytesIO(image_file.file.read()))
        file_name = f"{IMAGE_PATH}/{order}_{image_file.filename}"
        image.save(file_name)
        print(f"{id}/{image_file.filename} 저장되었습니다.")
    return [(f"{IMAGE_PATH}/{fname}", fname) for fname in os.listdir(IMAGE_PATH)]

def upload_files(file_paths, type, id):
    paths = []
    for path, name in file_paths:
        print(path)
        file_name = os.path.join(type, f"{id}/{name}")
        blob = bucket.blob(file_name)
        blob.upload_from_filename(path)
        paths.append(file_name)
    return paths
