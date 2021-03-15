import pytest

def test_static_route(app_factory):
    @app_factory.route('/home')
    def home(req, res):
        res.text = "ThatsATest"


def test_route_duplicate_exception(app_factory):
    @app_factory.route('/home')
    def home(req, res):
        res.text = "ThatsATest"
    
    with pytest.raises(AssertionError):
        @app_factory.route('/home')
        def home2(req, res):
            res.text = "IamADuplicate"


def test_test_client_works(app_factory, client):
    TEST_TEXT = "BellaCiao"

    @app_factory.route('/echo')
    def echo(req, res):
        res.text = TEST_TEXT
    
    assert client.get("http://testserv/echo").text == TEST_TEXT


def test_route_with_parameters(app_factory, client):
    @app_factory.route('/item/{identificator}')
    def get_item(req, res, identificator):
        res.text = identificator
    
    assert client.get("http://testserv/item/42").text == '42'
    assert client.get("http://testserv/item/keywordItem").text == 'keywordItem'


def test_route_not_found(app_factory, client):
    assert client.get("http://testserv/nosuchpage").text == "Not Found"
    assert client.get("http://testserv/nosuchpage").status_code == 404


def test_class_based_view_get_request(app_factory, client):
    @app_factory.route('/cbv')
    class SampleCBV:
        def get(self, req, res):
            res.text = 'thisiscbv'

    assert client.get("http://testserv/cbv").text == "thisiscbv"


def test_class_based_view_post_request(app_factory, client):
    @app_factory.route('/cbv_post')
    class SampleCBV:
        def post(self, req, res):
            res.text = 'postrequest'

    assert client.post("http://testserv/cbv_post").text == "postrequest"


def test_class_based_view_method_not_allowed(app_factory, client):
    @app_factory.route('/cbv_no_get')
    class SampleCBV:
        def post(self, req, res):
            res.text = 'postrequest'

    with pytest.raises(AttributeError):
        client.get("http://testserv/cbv_no_get")


def test_alternative_route(app_factory, client):
    response = "Alternative Way Of Creating Routes"

    def home(req, res):
        res.text = response
    
    app_factory.add_route('/alter', home)

    assert client.get("http://testserv/alter").text == response