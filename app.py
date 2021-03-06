from api import AppFactory
from middleware import Middleware

app = AppFactory()


class TestMiddleware(Middleware):
    def process_request(self, req):
        print("Processing request", req.url)


    def process_response(self, req, res):
        print("Processing response", req.url)

app.add_middleware(TestMiddleware)

def custom_exception_handler(request, response, exception_cls):
    response.text = 'Something went wrong. Please try again.'

app.add_exception_handler(custom_exception_handler)

@app.route('/home')
def home(request, response):
    response.text = "Hello from the HOME page"


@app.route('/about')
def about(request, response):
    response.text = "Hello from the ABOUT page"


@app.route('/passdigit/{digit:d}')
def pass_digit(request, response, digit):
    response.text = str(digit)

@app.route('/movie')
class MovieEndpoint:
    def get(self, req, res):
        res.text = 'HOLABUDDY'


@app.route('/welcome')
def welcome(req, res):
    res.body = app.template('index.html', context={'framework': 'faringate', 'title': 'My Very First Framework'}).encode()

    