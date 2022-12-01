__all__ = ['DJEAbortException', 'WidgetNotRegisteredError']


class DJEAbortException(BaseException):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class ChartFuncCallError(BaseException):
    def __init__(self, char_name: str):
        super().__init__(f'ChartName:{char_name}')


class WidgetNotRegisteredError(BaseException):
    def __init__(self, widget):
        super().__init__(f'Unknown widget type:{widget.__class__.__name__}')
