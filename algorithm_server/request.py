# define the data of the request
# its baesd on the particular business
import flask

class Request_algorithm_input():
    def __init__(self, input:flask.Request.json):
        self.data = []
        for item in flask.Request.json:
            self.data.append(item)

    def get_image(self):
        return self.image

    def set_image(self, image):
        self.image = image

    #提供与json的互相转换形式
