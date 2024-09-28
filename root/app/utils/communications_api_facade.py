import requests
 
class CommunicationAPIFacade:
    BASE_URL = 'https://l37z82o8xl.execute-api.us-east-1.amazonaws.com/prod/v1'
    HEADERS = {
            'x-api-key': 'XoxRJvm7UWaPtDsJFMnN32rrTjr9fbOB5CR7icLg',
            'Content-Type': 'application/json'
        }
 
    @staticmethod
    def post(endpoint, data=None):
        url = f"{CommunicationAPIFacade.BASE_URL}/{endpoint}"
        response = requests.post(url, headers=CommunicationAPIFacade.HEADERS, json=data)
        return response
   