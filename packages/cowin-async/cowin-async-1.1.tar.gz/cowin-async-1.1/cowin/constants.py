# standard imports
from enum import Enum
from random import randint


DATE_FORMAT = "%d-%m-%Y"
MOBILE_PATTERN = r'[6-9]+[0-9]{9}'

class Endpoints(str, Enum):
    APPOINTMENT_PINCODE = "appointment/sessions/public/calendarByPin"
    APPOINTMENT_DISTRICT = "appointment/sessions/public/calendarByDistrict"
    BASE = "https://cdn-api.co-vin.in/api/v2"
    CONFIRM_OTP = "auth/public/confirmOTP"
    DISTRICTS = "admin/location/districts"
    DOWNLOAD_CERT = "registration/certificate/public/download"
    GET_OTP = "auth/public/generateOTP"
    STATES = "admin/location/states"

    def __str__(self):
        return str.__str__(self)


class UserAgents(str, Enum):
    FF_88 = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0"
    FF_87 = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/87.0"
    CHROME_92 = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) Chrome/92.0 Safari/537.36"
    CHROME_91 = "Mozilla/5.0 (Windows NT 6.2) Chrome/91.0 Safari/537.36"

    @staticmethod
    def random():
        ua_list = [ua.value for ua in UserAgents]
        return ua_list[randint(0, len(ua_list)-1)]


class Languages(str, Enum):
    TAMIL = 'ta_IN'
    ENGLISH_US = 'en_US'
    ENGLISH_UK = 'en_UK'
    HINDI = 'hi_IN'

    def __str__(self):
        return str.__str__(self)
