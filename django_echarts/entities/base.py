class DwString(str):
    """This is a str for django template string."""

    @classmethod
    def login_name(cls, login_text: str = '{{ request.user.username }}', un_login_text: str = 'Unknown'):
        code_list = [
            '{% if request.user.is_authenticated %}',
            login_text,
            '{% else %}',
            un_login_text,
            '{% endif %}'
        ]
        return cls(''.join(code_list))





# entity_uri
class ChartIdentification:
    __slots__ = ['name', 'params']

    def __init__(self, name: str, params: dict = None):
        self.name = name
        self.params = params or {}

    def generate_url(self):
        url = []
        for k, v in self.params.items():
            url.extend([str(k), '/', str(v), '/'])
        return ''.join(url)
