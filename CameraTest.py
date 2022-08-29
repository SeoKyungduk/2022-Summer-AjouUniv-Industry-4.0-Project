import cv2              # pip install opencv-python
import pyzbar.pyzbar as pyzbar          # pip install pyzbar
import speech_recognition as sr         # pip install SpeechRecognition
import re
import os.path
from playsound import playsound         # pip install playsound

# TTS(Text To Speech)
def run_quickstart(INPUT,NAME):
    from google.cloud import texttospeech

    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=INPUT)

    voice = texttospeech.VoiceSelectionParams(
        language_code="ko-KR", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open(NAME, "wb") as out:
        out.write(response.audio_content)
        print('Audio content written to file ' + NAME)
        


# 약 종류 딕셔너리 (Key= 바코드 , Value = 상품명[mp3파일 영문저장명])
dic_medicine = {'8802260004246':"[대일밴드]band", '8801260610211':"[감기약]cold", '0652508442112':"[해열제]hot"}

p = re.compile(r"\[(.+)\](.+)")  # 정규표현 괄호구분

cap = cv2.VideoCapture(0) 

data_list = []

while True:
    bol, frame = cap.read()
    
    if bol:
        try:
            for code in pyzbar.decode(frame):
                barcode = code.data.decode('utf-8')
                
                # 이미 같은 바코드가 인식된 경우 이미 인식된 바코드라는 mp3 재생
                if barcode in data_list:
                    print("이미 인식된 바코드에요.")
                    playsound("already_detected.mp3")
                    break
                else:
                    # 바코드를 처음 인식하는 경우
                    data_list.append(barcode)  
                    print("Detection OK :",barcode) # 바코드 숫자를 출력 
                    playsound("beep.mp3")  # 인식했을때 효과음 출력
                    
                    # 인식한 바코드가 약 딕셔너리에 있을 때 Value 값으로 부터 약 이름과 파일명 추출
                    if barcode in dic_medicine:
                        value_medicine = dic_medicine.get(barcode)
                        m = p.match(value_medicine)
                        name_medicine = m.group(1); file_medicine = m.group(2)
                        file = file_medicine+".mp3"
                        
                        # 이미 mp3 파일이 있을 때 그 파일을 재생
                        if os.path.isfile(file):
                            print("파일이 이미 존재하므로 생성없이 그대로 재생합니다.")
                            print("이건 "+name_medicine+" 에요")
                            playsound(file)
                        
                        # mp3 파일이 존재하지 않을 때 mp3파일을 TTS로 생성 후 재생
                        else: 
                            if __name__ == "__main__":
                                run_quickstart("이건 "+name_medicine+" 에요",file)
                            print("파일이 존재하지 않아 생성 후 재생합니다.")
                            playsound(file)
                    
                    # 바코드가 약 딕셔너리에 없을 때 목록에 없다는 mp3파일 재생
                    else:
                        print("목록에 없는 제품이에요. 혹은 인식불량 일수도 있으니 다시 바코드를 갖다 대어 주세요")
                        playsound("not_in_list.mp3")
                                          

        except Exception as e:
            print(e)   
        
    
            
        cv2.imshow('cam',frame)
        key = cv2.waitKey(1)
        if key == 27:
            break
        
print("인식된 바코드 목록:",data_list)

cap.release()
cv2.destroyAllWindows()