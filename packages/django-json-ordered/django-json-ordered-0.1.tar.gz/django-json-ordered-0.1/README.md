Django Json Ordered
====================

# Install:
    pip install -e git+https://github.com/rafaelgontijo/django-json-ordered.git@master#egg=django_json_ordered

# Usage:

Create your model:

    from django.db import models
    from django_json_ordered.fields import JsonOrderedField

    class YourModel(models.Model):
        your_field = JsonOrderedField()
