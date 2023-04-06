class QRCodeNotFoundEx(Exception):
    def __init__(self, msg='qr code not found', *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = msg
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_QR_CODE_NOT_FOUND'

    pass
