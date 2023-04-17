class UserNotHaveAddressEx(Exception):
    def __init__(self, msg='User not have address', *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = msg
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_USER_NOT_HAVE_ADDRESS'

    pass

