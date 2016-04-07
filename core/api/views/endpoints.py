import os
from uuid import uuid4

from flask import Module, jsonify, request, Response
from flask.views import MethodView

from core.api import API
from core.api.decorators import jsonp
from core.backends.UNIX import UNIXBackend
from core.utils.RequestValidator import CreateUnikernelValidator
from ..RedisQueue import Q

api = Module(
    __name__,
    # url_prefix='/api'
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


@api.route('/static/<_id>/<file>')
def static(_id, file):
    work_dir = API.db.jobs.find_one(
        {
            '_id': _id
        },
        {
            '_id': 0,
            'work_dir': 1
        }
    )['work_dir']

    try:
        with open(os.path.join(work_dir, file), 'r') as f:
            content = f.read()
    except FileNotFoundError:
        return jsonify_status_code(
            code=404,
            message='Room no 404: File not found'
        )
    except UnicodeDecodeError:
        return jsonify_status_code(
            code=415,
            message='Access to binary data is forbidden'
        )

    return Response(content, mimetype="text/plain")


class CreateUnikernel(MethodView):
    @jsonp
    def get(self):
        return jsonify_status_code(
            code=405,
            message='HTTP method GET is not allowed for this URL'
        )

    @jsonp
    def post(self):
        content = request.get_json(force=False, silent=True)
        if not content:
            return jsonify_status_code(
                code=400,
                message='Bad HTTP POST request'
            )
        else:
            # Validate JSON
            if not CreateUnikernelValidator.validate(content):
                return jsonify_status_code(
                    code=400,
                    message='HTTP POST request data is invalid. Refer to the Dune API documentation for details.'
                )
            else:
                if content['backend'] == 'unix':
                    _id = uuid4().hex[:7]

                    content['_id'] = _id
                    content['status'] = None
                    content['created_at'] = None
                    content['started_at'] = None

                    backend_instance = UNIXBackend(
                        _id=_id,
                        project=content['meta']['project'],
                        module=content['meta']['module']
                    )

                    content['work_dir'] = backend_instance.work_dir

                    API.db.jobs.insert_one(
                        content
                    )

                    backend_instance.register(
                        content['config'],
                        content['unikernel']
                    )

                    Q.enqueue(
                        backend_instance.configure
                    )

                    Q.enqueue(
                        backend_instance.compile
                    )

                    Q.enqueue(
                        backend_instance.start
                    )

                    return jsonify_status_code(
                        code=200,
                        message='Unikernel execution started successfully',
                        _id=_id
                    )


class DetailsUnikernel(MethodView):
    @jsonp
    def get(self, _id):
        data = API.db.jobs.find_one(
            {
                '_id': _id
            }
        )

        return jsonify_status_code(
            code=200,
            data=data
        )

    @jsonp
    def post(self, _id):
        return jsonify_status_code(
            code=405,
            message='HTTP method POST is not allowed for this URL'
        )


CreateUnikernel_view = CreateUnikernel.as_view('create_unikernel')
api.add_url_rule(
    '/api/unikernel/create',
    view_func=CreateUnikernel_view,
    methods=['GET', 'POST']
)

DetailsUnikernel_view = DetailsUnikernel.as_view('details_unikernel')
api.add_url_rule(
    '/api/unikernel/<_id>',
    view_func=DetailsUnikernel_view,
    methods=['GET', 'POST']
)
