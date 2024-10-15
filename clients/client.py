class Client:
    def __init__(self):
        pass

    def capabilities(self):
        raise NotImplementedError

    def get(self, url, cookies):
        raise NotImplementedError

    def post(self, url, postData, cookies):
        raise NotImplementedError


class ClientResponse:
    def __init__(self, status, message, solution):
        self.status = status
        self.message = message
        self.solution = solution

    def toDict(self):
        return {
            'status': self.status,
            'message': self.message,
            'solution': self.solution.toDict() if self.solution else None,
            'versiom': '1.0.0'
        }


class Solution:
    def __init__(self, url, status, response, cookies, userAgent):
        self.url = url
        self.status = status
        self.response = response
        self.cookies = cookies
        self.userAgent = userAgent

    def toDict(self):
        return {
            'url': self.url,
            'status': self.status,
            'response': self.response,
            'cookies': self.cookies,
            'userAgent': self.userAgent
        }
