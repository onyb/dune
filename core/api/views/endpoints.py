from flask import Module, jsonify
from flask.views import MethodView

from core.api.decorators import jsonp

api = Module(
    __name__,
    url_prefix='/api'
)


def jsonify_status_code(*args, **kw):
    response = jsonify(*args, **kw)
    response.status_code = kw['code']
    return response


@api.route('/')
def index():
    """
    The root of the API returns an error
    """
    return jsonify_status_code(
        code=400,
        message='Room no 404: File not found'
    )


class TestModelAPI(MethodView):
    @jsonp
    def get(self, id=None):
        if id:
            return jsonify(
                code=200,
                value=0
            )
        else:
            return jsonify(
                code=200,
                value=1
            )


TestModel_view = TestModelAPI.as_view('test_model_api')
api.add_url_rule(
    '/test',
    view_func=TestModel_view,
    methods=['GET']
)

api.add_url_rule(
    '/test/<string:id>',
    view_func=TestModel_view,
    methods=['GET']
)
