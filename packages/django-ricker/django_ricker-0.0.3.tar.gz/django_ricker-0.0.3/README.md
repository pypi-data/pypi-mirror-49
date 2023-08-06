
There are some django utils, make it convenient for work.
Now only support django 1.9,  1.9+ may aslo work.


## 1 install

```
pip install django-ricker

```

## 2 get all urls


```shell
cd project_home
python manage.py shell
from django_ricker.urls import get_all_urls
print get_all_urls()

```