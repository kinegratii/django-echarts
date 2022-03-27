"""
A shortcut method for builtin theme styles.
"""


def bootstrap_table_class(border=False, borderless=False, striped=False, size=None):
    class_list = ['table', 'table-responsive']
    if border:
        class_list.append('table-bordered')
    if borderless:
        class_list.append('table-borderless')
    if striped:
        class_list.append('table-striped')
    if size:
        class_list.append(f'table-{size}')
    return ' '.join(class_list)


def material_table_class(striped=False, center=False):
    class_list = ['responsive-table', ]
    if striped:
        class_list.append('striped')
    if center:
        class_list.append('centered')
    return ' '.join(class_list)
