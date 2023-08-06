import requests
from requests.structures import CaseInsensitiveDict
class Client:
  def __init__(self, user_id, key):
    self.user_id=user_id
    self.key=key
  def send_sms(self, number, msg):
#    print(self.user_id)

    url = "https://oursms.app/api/v1/SMS/Add/SendOneSms"

    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    data = '{"userId": ' + str(self.user_id) + ', "key": "' + self.key + '", "phoneNumber": "' + number + '", "message": "' + msg + '"}'


#    print(data)

    resp = requests.post(url, headers=headers, data=data)
    return(resp.json()['data'])


  def send_otp(self, number, otp):
    url = "https://oursms.app/api/v1/SMS/Add/SendOtpSms"

    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"

    data = '{"userId": ' + str(self.user_id) + ', "key": "' + self.key + '", "phoneNumber": "' + number + '", "otp": "' + otp + '"}'


    resp = requests.post(url, headers=headers, data=data)
    return(resp.json()['data'])

  def msg_status(self, msg_id):
    url = "https://oursms.app/api/v1/SMS/Get/GetStatus/"+msg_id

    resp = requests.get(url)
    return(resp.json()['data'])

