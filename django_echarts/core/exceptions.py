__all__ = ['DJEAbortException']


class DJEAbortException(BaseException):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class ChartFuncCallError(BaseException):
    def __init__(self, char_name: str):
        super().__init__(f'ChartName:{char_name}')
