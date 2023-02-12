from datetime import datetime


class DateConverter:
    regex = '[0-9]{8}'

    def to_python(self, value):
        return datetime.strptime(value, '%Y%m%d').date()

    def to_url(self, value):
        return value.strftime('%Y%m%d')


DJE_CONVERTERS = {
    'date': DateConverter()
}
