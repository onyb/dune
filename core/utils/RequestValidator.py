class Validator(object):
    pass


class CreateUnikernelValidator(Validator):
    __toplevel__ = {
        'meta': {
            'required': True,
            'type': dict
        },
        'unikernel': {
            'required': True,
            'type': str
        },
        'config': {
            'required': True,
            'type': str
        },
        'backend': {
            'required': True,
            'type': str
        },
        'cron': {
            'required': False,
            'type': str
        }
    }

    __meta__ = {
        'name': {
            'required': False,
            'type': str
        },
        'project': {
            'required': True,
            'type': str
        },
        'module': {
            'required': True,
            'type': list
        }
    }

    @staticmethod
    def validate(data: dict) -> bool:
        """
        Check whether the data corresponds to schema as given in class CreateUnikernelValidator.__toplevel__ and
        CreateUnikernelValidator.__meta__
        :param data: POST data in JSON format
        :return: True if data is valid, False otherwise
        """
        for key in data:
            # Check if payload contains any field not defined in the schema
            if key not in CreateUnikernelValidator.__toplevel__:
                return False

            # Check type of data in each field of payload
            elif type(data[key]) is not CreateUnikernelValidator.__toplevel__[key]['type']:
                return False

        # Check if all required fields are present in the payload
        for key, value in CreateUnikernelValidator.__toplevel__.items():
            if value['required'] is True and key not in data:
                return False

        # Check if all required fields are present in the payload
        for key in data['meta']:
            if key not in CreateUnikernelValidator.__meta__:
                return False

        # Check if all required fields in meta are present in the payload
        for key, value in CreateUnikernelValidator.__meta__.items():
            if value['required'] is True and key not in data['meta']:
                return False

        # meta fields cannot contain whitespace characters
        if ' ' in data['meta']['project'] or ' ' in ''.join(data['meta']['module']) or ' ' in data['meta']['name']:
            return False

        return True


if __name__ == '__main__':
    # Valid POST data
    data_1 = {
        'meta': {
            'name': 'foo',
            'project': 'bar',
            'module': ['baz']
        },
        'unikernel': 'Dummy OCaml program',
        'config': 'Dummy OCaml program',
        'backend': 'xen',
        'cron': 'crontab'
    }

    # POST data with missing required field
    data_2 = {
        'meta': {
            'name': 'foo',
            # 'project': None,
            'module': []
        },
        'unikernel': '',
        'config': '',
        'backend': 'unix',
        'cron': ''
    }

    # POST data with invalid type
    data_3 = {
        'meta': {
            'name': None,
            'project': None,
            'module': 'moduleX'
        },
        'unikernel': 1,
        'config': '',
        'backend': None,
        'cron': None
    }

    # POST data with an extra undefined field
    data_4 = {
        'meta': {
            'name': 'foo',
            'project': 'bar',
            'bose': True,
            'module': []
        },
        'unikernel': '',
        'config': '',
        'backend': 'unix',
        'cron': ''
    }

    # POST data with whitespaces in meta
    data_5 = {
        'meta': {
            'name': 'project name',
            'project': '',
            'module': ['a', 'game of', 'thrones']
        },
        'unikernel': '',
        'config': '',
        'backend': '',
        'cron': ''
    }

    assert CreateUnikernelValidator.validate(data_1) == True
    assert CreateUnikernelValidator.validate(data_2) == False
    assert CreateUnikernelValidator.validate(data_3) == False
    assert CreateUnikernelValidator.validate(data_4) == False
    assert CreateUnikernelValidator.validate(data_5) == False
