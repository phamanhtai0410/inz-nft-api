class UserTemplateIsUsedEx(Exception):
    def __init__(self, msg="User's template is used.", *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = msg
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_USER_TEMPLATE_USED'

    pass
