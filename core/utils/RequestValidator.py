class Validator(object):
    REQUIRED = True
    OPTIONAL = False


class CreateUnikernelValidator(Validator):
    __toplevel__ = {
        'meta': Validator.REQUIRED,
        'unikernel': Validator.REQUIRED,
        'config': Validator.REQUIRED,
        'backend': Validator.REQUIRED,
        'cron': Validator.OPTIONAL
    }

    __meta__ = {
        'name': Validator.OPTIONAL,
        'project': Validator.REQUIRED,
        'module': Validator.OPTIONAL
    }

    @staticmethod
    def validate(data: dict) -> bool:
        for key in data:
            if key not in CreateUnikernelValidator.__toplevel__:
                return False

        for key, value in CreateUnikernelValidator.__toplevel__.items():
            if value is Validator.REQUIRED and key not in data:
                return False

        for key in data['meta']:
            if key not in CreateUnikernelValidator.__meta__:
                return False

        for key, value in CreateUnikernelValidator.__meta__.items():
            if value is Validator.REQUIRED and key not in data['meta']:
                return False

        return True


if __name__ == '__main__':
    valid_POST_data = {
        'meta': {
            'name': None,
            'project': None,
            'module': []
        },
        'unikernel': None,
        'config': None,
        'backend': None,
        'cron': None
    }

    invalid_POST_data_1 = {
        'meta': {
            'name': None,
            # 'project': None,
            'module': []
        },
        'unikernel': None,
        'config': None,
        'backend': None,
        'cron': None
    }

    invalid_POST_data_2 = {
        'meta': {
            'name': None,
            'project': None,
            'module': []
        },
        'unikernel': None,
        'config': None,
        # 'backend': None,
        'cron': None
    }

    assert CreateUnikernelValidator.validate(valid_POST_data) == True
    assert CreateUnikernelValidator.validate(invalid_POST_data_1) == False
    assert CreateUnikernelValidator.validate(invalid_POST_data_2) == False
