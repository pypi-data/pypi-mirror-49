<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
https://pypi.org/project/django-readme-generator/
-->

[![](https://img.shields.io/pypi/pyversions/django-base-url.svg?longCache=True)](https://pypi.org/project/django-base-url/)

#### Installation
```bash
$ [sudo] pip install django-base-url
```

#### How it works
settings `BASE_URL` if defined, else scheme+`request.get_host()`

#### `settings.py`
```python
TEMPLATE_CONTEXT_PROCESSORS = (
    "django_base_url.context_processors.base_url",
)
```

#### Examples
`settings.py`:
```python
BASE_URL="http://host/"
```

```html
<base href="{{ BASE_URL }}">
```

<p align="center">
    <a href="https://pypi.org/project/django-readme-generator/">django-readme-generator</a>
</p>