# Djangoldp Uploader

File upload for djangoldp framework

## Install
- Add `djangoldp_uploader` on DJANGOLDP_PACKAGES in your `settings.py`
- install the module : `pip install djangoldp_uploader`
- migrate the db : `./manage.py migrate`

## Settings 

Add the following on settings.py :

```
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
``` 

## Demo
- Run the module on a djangoldp server has djangoldp packages
- go to `your_server_url/upload_home/`

