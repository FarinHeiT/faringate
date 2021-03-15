from api import AppFactory


app = AppFactory()

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

    