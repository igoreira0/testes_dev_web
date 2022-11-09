import random
import string
import requests
import json

base_url = 'http://localhost:3000'

blueprint_peticao = '/peticao'

blueprint_auth = '/auth'

blueprint_health = '/health'

class TestPeticoes():

    def __init__(self) -> None:
        self.email = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)) + '@gmail.com'
        self.password = '1234'
        self.token = ''
        self.created_peticao = ''

    def test_liveness(self):
        resp = requests.get(base_url + blueprint_health + '/liveness')
        assert resp.status_code == 200
        assert resp.text == '{"status":"ok"}'
        print('test liveness success')

    def test_get_all_peticao(self):
        resp = requests.get(base_url + blueprint_peticao)
        assert resp.status_code == 200
        print('test get all peticao success')

    def test_specific_peticao(self):
        peticao_id = '634f2c6d5f9c0b784ea03e0e'
        resp = requests.get(base_url + blueprint_peticao + f'/{peticao_id}')
        assert resp.status_code == 200
        print(f'test get peticao id: {peticao_id} success')

    def test_get_invalid_specific_peticao(self):
        peticao_id = 'invalid'
        resp = requests.get(base_url + blueprint_peticao + f'/{peticao_id}')
        assert resp.status_code == 404
        print(f'test get invalid peticao id: {peticao_id} success')

    def test_register_new_user(self):
        resp = requests.post(base_url + blueprint_auth + '/register', {'name': 'test_name', 'email': self.email, 'password': self.password})
        assert resp.status_code == 200
        print(f'test register new user success\nuser: {self.email}\npass:{self.password}')

    def test_login(self):
        resp = requests.post(base_url + blueprint_auth + '/authenticate', {'email': self.email, 'password': self.password})
        token_obj = json.loads(resp.text)
        assert token_obj
        self.token = token_obj['token']
        assert resp.status_code == 200
        assert len(self.token) > 0
        print(f'test login with user \nemail: {self.email}\npass:{self.password}')

    def test_create_peticao(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        resp = requests.post(base_url + blueprint_peticao + '/newpeticao', headers=headers, 
                            data={'title': 'test peticao title', 'description': 'test peticao description' })
        obj = json.loads(resp.text)
        self.created_peticao = obj['_id']
        assert resp.status_code == 200
        print('test creating new peticao success')

    def test_update_peticao(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        resp = requests.put(base_url + blueprint_peticao + '/updatpeticao', 
                        {'_id': self.created_peticao, 'title': 'new_title', 'description': 'new description'}, headers=headers)
        assert resp.status_code == 200
        print(f'test update peticao id: {self.created_peticao} success')

    def test_sign_peticao(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        peticao_id = '634f2c6d5f9c0b784ea03e0e'
        resp = requests.post(base_url + blueprint_peticao + f'/sign/{peticao_id}', headers=headers)
        assert resp.status_code == 200
        print(f'test sign peticao success')
        
    def test_delete_peticao(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        resp = requests.delete(base_url + blueprint_peticao + f'/delete/{self.created_peticao}', headers=headers)
        assert resp.status_code == 204
        print(f'test delete peticao success')

classe = TestPeticoes()
classe.test_liveness()
classe.test_get_all_peticao()
classe.test_specific_peticao()
classe.test_get_invalid_specific_peticao()
classe.test_register_new_user(),
classe.test_login()
classe.test_create_peticao()
classe.test_update_peticao()
classe.test_sign_peticao()
classe.test_delete_peticao()