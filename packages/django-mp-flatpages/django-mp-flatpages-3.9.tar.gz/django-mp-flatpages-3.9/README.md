# MP-Flatpages

Django flatpages app.

### Installation

Install with pip:

```
$ pip install django-mp-flatpages
```

Add flatpages to urls.py:

```
urlpatterns = [

    path('', include('flatpages.urls'))
    
]
```

Add flatpages to settings.py:
```
from flatpages import DefaultFlatPagesConfig
from flatpages.constants import EDITOR_CKEDITOR_UPLOADER


class FlatPagesConfig(DefaultFlatPagesConfig):

    wising_editor = EDITOR_CKEDITOR_UPLOADER

    wising_editors = {
        'editor_name': 'path.to.widget.class'
    }
    
    default_template = 'custom_template.html'


INSTALLED_APPS = [
    'settings.FlatPagesConfig'
]
```

Run migrations:
```
python manage.py migrate
```

### Custom template

To rewrite default template you can create templates/flatpages/default.html template in your app 
or set `default_template` in your app config.

### App compatible with

* django-modeltranslation
