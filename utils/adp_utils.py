"""ADP utilities

Author: Jungbeom Ko

Date: 2021/10/09
"""

def check_extension(path):
    extensions = ['wav', 'raw']
    extension = path[-3:]
    assert extension in extensions
    return extension
