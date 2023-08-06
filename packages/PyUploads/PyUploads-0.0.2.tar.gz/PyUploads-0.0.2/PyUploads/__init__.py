import requests

class CreationError(Exception):
    pass


# I will use seperate files for each later
class Throwbin():
    def Create(title, file_content):
        r = requests.put(
            'https://api.throwbin.io/v1/store', 
            data={
                'title': title, 
                'id': None, 
                'paste': file_content
            }
        )
        if r.status_code == 200:
            return 'throwbin.io/{id}'.format(id=r.json()['id']) 
        else: 
            raise CreationError('Failed to create throwbin item: {e}'.format(e=r.text))
 
class Hastebin():
    def Create(file_content):
        r = requests.post(
            'https://hastebin.com/documents', 
            data=file_content
        )
        try:
            return(f'https://hastebin.com/{r.json()["key"]}')
        except:
            raise(CreationError('Failed to create Hastebin item {e}'.format(e=r.text)))