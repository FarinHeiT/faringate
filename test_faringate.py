import pytest

from api import AppFactory

@pytest.fixture
def app_factory():
    return AppFactory()

def test_static_route(app_factory):
    @app_factory.route('/home')
    def home(req, res):
        rest.text = "ThatsATest"


def test_route_duplicate_exception(app_factory):
    @app_factory.route('/home')
    def home(req, res):
        rest.text = "ThatsATest"
    
    with pytest.raises(AssertionError):
        @app_factory.route('/home')
        def home2(req, res):
            rest.text = "IamADuplicate"
