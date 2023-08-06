import requests
import urllib

class ReescritorRequest():

    def spinner(api_key, text_in, protected, provider='reescritor.com'):
        url = f'https://{provider}/tools/spinner-api.php'
        myobj = {'api_key': api_key,
		 'text_in': text_in,
		 'protected': protected}
        
        response = requests.post(url, data = myobj)
        
        return response.json()
