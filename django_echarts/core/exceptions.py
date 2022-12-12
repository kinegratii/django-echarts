__all__ = ['DJEAbortException', 'WidgetNotRegisteredError']


class DJEAbortException(BaseException):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


# ErrorMessageException / WarningMessageException

class ChartFuncCallError(BaseException):
    def __init__(self, char_name: str):
        super().__init__(f'ChartName:{char_name}')


class WidgetNotRegisteredError(BaseException):
    def __init__(self, widget):
        super().__init__(f'Unknown widget type:{widget.__class__.__name__}')


class ChartDoesNotExist(BaseException):
    def __init__(self, message: str = None, param_name: str = None, param_input=None, param_choices=None):
        if param_name:
            message = f'Invalid param value: {param_name}={param_input}. Choices are: {param_choices}'
        super().__init__(message)
