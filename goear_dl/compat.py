import six

if six.PY2:
    from urllib import quote as url_quote
else:
    from urllib.parse import quote as url_quote