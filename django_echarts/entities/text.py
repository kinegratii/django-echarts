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
