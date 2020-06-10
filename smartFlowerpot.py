#2018038092 안준
#데이터베이스와 라즈베리파이를 연결하는 클래스
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

class DatabaseControl:
    def __init__(self,userID):
        #2018038092 안준
        #초기화를 위한 생성자. userID를 받아야 함.
        self.userID = userID #userID는 DB에 저장된 어떤 사용자를 제어할지 정해준다. 
        self.db_url = 'https://smart-flowerpot-5676e.firebaseio.com/'
        #라즈베리 파이에 인증키 json 파일을 저장하고 그 경로를 cred 변수에 지정해준다.
        self.cred = credentials.Certificate(r"여기에 경로 입력\smart-flowerpot-5676e-firebase-adminsdk-1u31n-2c2b1f2aec.json")
        self.default_app = firebase_admin.initialize_app(self.cred, {'databaseURL':self.db_url})

    def updatePotState(self, temp, moisture, Pump,LED,Fan):
        #2018038092 안준
        #db에 화분의 상태값을 업데이트 하는 함수
        #센서에서 측정한 값을 updatePotState( )에 매개변수로 전달하고, 
        #전달받은 매개변수를 데이터베이스의 flowerpot에 입력
        ref = db.reference('Users/' + self.userID)
        ref.update({
            'flowerpot' : {
                'Cur_temp' : temp, 
                'Cur_moisture' : moisture, 
                'Pump_state' : Pump, 
                'LED_state' : LED, 
                'Fan_state' : Fan
         }})

    def manualControl(self):
        #2018038092 안준
        #화분의 상태값 반환 
        #안드로이드 앱에서 수동 조작을 명령하면 db에 저장된 각 장치의 bool값이 True로 변경된다.
        #그 값을 가져와서 각 장치를 제어하는 코드에 True를 넘겨주고 작동한다. 
        ref = db.reference('Users/' + self.userID + '/flowerpot')
        snapshot =  ref.order_by_key().get()
        Pump = snapshot['Pump_state']
        LED = snapshot['LED_state']
        Fan = snapshot['Fan_state']
        #파이썬은 return 문으로 여러개의 반환 값을 보낼 수 있다. 
        #함수를 호출한 쪽에서는 반환된 데이터의 개수만큼 변수를 준비해야 한고.
        #반환된 순서대로 대입된다.
        return Pump,LED,Fan #하드웨어의 상태를 각각의 변수에 담아서 리턴
    
    def bringPlantRequireInfo(self):
        #2018038092 안준
        #식물이 필요한 상태값 가져오기 
        #화분을 제어하기 위해 각 식물에게 필요한 값을 DB로부터 전달 받아야한다. 
        #화분이 필요로하는 값들을 반환하고 그 값을 기준으로 펌프나,LED.팬 등을 작동시킨다.
        ref = db.reference('Users/' + self.userID + '/myPlant')
        snapshot =  ref.order_by_key().get()
        MaxMoisture = snapshot['plant_MaxMoisture']
        MinMoisture = snapshot['plnat_MinMoisture']
        MaxTemp = snapshot['plnat_MaxTemp']
        MinTemp = snapshot['plant_MinTemp']
        return MaxMoisture,MinMoisture,MaxTemp,MinTemp


# 사용 예시
database = DatabaseControl('gomdori1234') #gomdori1234이라는 사용자가 사용할 database 객체 선언 & 초기화


database.updatePotState(20,50,True,False,False) #화분의 상태값을 db에 전달

pump,led,fan = database.manualControl() #각각의 반환 값을 받아서 저장.
print(pump,led,fan )

