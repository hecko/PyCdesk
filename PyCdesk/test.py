import requests
import json
from pprint import pprint

class Cdesk:
    def __init__(self):
        self.base_url = "https://cmpp.seal.sk/apiportal/api"
        self.token = ""
        self.s = requests.Session()

    def logout(self):
        url = self.base_url + "/logout"
        print("Making request to {}".format(url))
        response = self.s.post(url)
        print(response.status_code)
        print(response.text)
        print(response.headers)
        return True

    def login(self, login, password):
        url = self.base_url + "/auth/login"
        print("Making request to {}".format(url))
        response = self.s.post(url, data={
            'login': login,
            'password': password,
        })
        try:
            self.token = response.json()['token']
            if self.token is "":
                raise Exception()
            self.s.headers.update({'Authorization': 'apitoken ' + self.token})
            return self.token
        except Exception as e:
            print("{}".format(e))
            print("{}".format(response.text))
            print("{}".format(response.headers))
            return ""

    def request_list(self):
        url = self.base_url + "/request"
        print("Making request to {}".format(url))
        response = self.s.get(url, headers={'Content-Type': 'application/json'})
        return response.json()

    def request_add(self):
        url = self.base_url + "/request"
        print("Making request to {}".format(url))
        response = self.s.post(url, data=json.dumps({
            'type': "H",
            'for_customer': "",
            'priority': 0,
            'status': 10,
            'title': "marec test",
            'id_company': 278610, # company ID from address book
            'id_solver': 140696, # assignee from Usersand groups
            'due_date': "2019-01-25T23:00:00+00:00",
            'reaction_due_date': "2019-01-25T23:00:00+00:00",
            'description': "<p>tento moj testt</p>",
            'notify': {},
        }), headers={'Content-Type': 'application/json'})
        # if response.status_code != 200:
        print(response.text)
        # return ID of the new request
        return response.json()['data']

if __name__ == "__main__":
    cd = Cdesk()
    token = cd.login("login", "password")
    if token is not "":
        print("Token: {}".format(token))
    else:
        print("Unable to log in")
    request_list = cd.request_list()
    pprint(request_list)
    for request in request_list['data']:
        print(request['description'])
    new_request_id = cd.request_add()
    print(new_request_id)
    cd.logout()
    new_request_id = cd.request_add()
    print(new_request_id)
