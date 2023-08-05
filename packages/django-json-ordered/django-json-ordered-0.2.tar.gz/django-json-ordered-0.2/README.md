Django Json Ordered
====================

# Install:
    pip install django-json-ordered

# Usage:

Create your model:

    from django.db import models
    from django_json_ordered.fields import JsonOrderedField

    class YourModel(models.Model):
        your_field = JsonOrderedField()
