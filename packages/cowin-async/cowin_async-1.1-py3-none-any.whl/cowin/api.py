# Standard imports
import datetime
from abc import ABC, abstractmethod

# Third party imports
from httpx import Client, AsyncClient

# local imports
from .constants import DATE_FORMAT, Endpoints, UserAgents, Languages
from .exceptions import BadRequest, ServerError
from .utils import is_mobile_number_valid, hash_otp


class BaseAPI(ABC):
    """Base Class for API client"""
    @property
    def base_url(self):
        """returns base url of the API"""
        return Endpoints.BASE

    @abstractmethod
    def get_states(self, language: str):
        """get list of states"""
        raise NotImplementedError()

    @abstractmethod
    def get_districts(self, state_id: int, language: str):
        """get list of districts for a state"""
        raise NotImplementedError()

    @abstractmethod
    def get_available_sessions_by_pincode(self, pincode: int, date: datetime.date):
        """get planned vaccination sessions on a specific date in a given
        pincode
        """
        raise NotImplementedError()

    @abstractmethod
    def get_otp(self, mobile: str):
        """sends OTP to supplied mobile number and returns txn ID"""
        raise NotImplementedError()

    @abstractmethod
    def confirm_otp(self, txn_id: str, otp: int):
        """confirm otp"""
        raise NotImplementedError()

    @abstractmethod
    def get_certificate(self, token: str, beneficiary_id: str):
        """download certificate as pdf for beneficiary"""
        raise NotImplementedError()

    @classmethod
    def process_response(cls, status_code, msg):
        """check response status code and raise exception if required"""
        if 400 <= status_code < 500:
            raise BadRequest(f"{status_code} - {msg}")
        if 500 <= status_code <= 599:
            raise ServerError(f"{status_code} - {msg}")


class Cowin(BaseAPI):
    """Cowin API client

    This client makes blocking synchronous http request to the server.
    """

    def __init__(self):
        self.__client = Client(base_url=self.base_url)

    def get_states(self, language=Languages.ENGLISH_US):
        headers = {
            'User-Agent': UserAgents.random(),
            'Accept-Language': language
        }
        response = self.__client.get(Endpoints.STATES, headers=headers)
        self.process_response(response.status_code, response.text)
        return response.json()

    def get_districts(self, state_id: int, language="en_US"):
        headers = {
            'User-Agent': UserAgents.random(),
            'Accept-Language': language
        }
        endpoint = f"{Endpoints.DISTRICTS}/{state_id}"
        response = self.__client.get(endpoint, headers=headers)
        self.process_response(response.status_code, response.text)
        return response.json()

    def get_available_sessions_by_pincode(self, pincode: int, date=None):
        if not date:
            date = datetime.date.today().strftime(DATE_FORMAT)

        headers = {'User-Agent': UserAgents.random()}
        query = {'pincode': pincode, 'date': date}
        response = self.__client.get(
            Endpoints.APPOINTMENT_PINCODE,
            headers=headers,
            params=query
        )
        self.process_response(response.status_code, response.text)
        return response.json()

    def get_otp(self, mobile: str):
        if not is_mobile_number_valid(mobile):
            raise BadRequest("Invalid mobile number")
        headers = {'User-Agent': UserAgents.random()}
        payload = {'mobile': mobile}
        response = self.__client.post(
            Endpoints.GET_OTP,
            headers=headers,
            json=payload
        )
        self.process_response(response.status_code, response.text)
        return response.json()

    def confirm_otp(self, txn_id: str, otp: str):
        headers = {'User-Agent': UserAgents.random()}
        payload = {
            'otp': hash_otp(otp),
            'txnId': txn_id
        }
        response = self.__client.post(
            Endpoints.CONFIRM_OTP,
            headers=headers,
            json=payload
        )
        self.process_response(response.status_code, response.text)
        return response.json()

    def get_certificate(self, token: str, beneficiary_id: str) -> bytes:
        headers = {
            'User-Agent': UserAgents.random(),
            'Authorization': f'Bearer {token}'
        }
        params = {'beneficiary_reference_id': beneficiary_id}
        response = self.__client.get(
            Endpoints.DOWNLOAD_CERT,
            headers=headers,
            params=params
        )
        self.process_response(response.status_code, response.text)
        if response.headers['content-type'] != 'application/pdf':
            raise ServerError("Content is not PDF")
        return response.content


class AsyncCowin(BaseAPI):
    """Cowin API Client

    This client makes non-blocking asynchronous http request to server.
    """

    async def get_states(self, language=Languages.ENGLISH_US):
        headers = {
            'User-Agent': UserAgents.random(),
            'Accept-Language': language
        }
        async with AsyncClient(base_url=self.base_url) as client:
            response = await client.get(Endpoints.STATES, headers=headers)
        self.process_response(response.status_code, response.text)
        return response.json()

    async def get_districts(self, state_id: int, language="en_US"):
        headers = {
            'User-Agent': UserAgents.random(),
            'Accept-Language': language
        }
        endpoint = f"{Endpoints.DISTRICTS}/{state_id}"
        async with AsyncClient(base_url=self.base_url) as client:
            response = await client.get(endpoint, headers=headers)
        self.process_response(response.status_code, response.text)
        return response.json()

    async def get_available_sessions_by_pincode(self, pincode: int, date=None):
        if not date:
            date = datetime.date.today().strftime(DATE_FORMAT)

        headers = {'User-Agent': UserAgents.random()}
        query = {'pincode': pincode, 'date': date}
        async with AsyncClient(base_url=self.base_url) as client:
            response = await client.get(
                Endpoints.APPOINTMENT_PINCODE,
                headers=headers,
                params=query
            )
        self.process_response(response.status_code, response.text)
        return response.json()

    async def get_otp(self, mobile: str):
        if not is_mobile_number_valid(mobile):
            raise BadRequest("Invalid mobile number")
        headers = {'User-Agent': UserAgents.random()}
        payload = {'mobile': mobile}
        async with AsyncClient(base_url=self.base_url) as client:
            response = await client.post(
                Endpoints.GET_OTP,
                headers=headers,
                json=payload
            )
        self.process_response(response.status_code, response.text)
        return response.json()

    async def confirm_otp(self, txn_id: str, otp: int):
        headers = {'User-Agent': UserAgents.random()}
        payload = {
            'otp': hash_otp(otp),
            'txnId': txn_id
        }
        async with AsyncClient(base_url=self.base_url) as client:
            response = await client.post(
                Endpoints.CONFIRM_OTP,
                headers=headers,
                json=payload
            )
        self.process_response(response.status_code, response.text)
        return response.json()

    async def get_certificate(self, token: str, beneficiary_id: str) -> bytes:
        headers = {
            'User-Agent': UserAgents.random(),
            'Authorization': f'Bearer {token}'
        }
        params = {'beneficiary_reference_id': beneficiary_id}
        async with AsyncClient(base_url=self.base_url) as client:
            response = await client.get(
                Endpoints.DOWNLOAD_CERT,
                headers=headers,
                params=params
            )
        self.process_response(response.status_code, response.text)
        if response.headers['content-type'] != 'application/pdf':
            raise ServerError('Content is not PDF')
        return response.content
