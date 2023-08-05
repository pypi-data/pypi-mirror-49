# jupyter-extension-publish

for publish notebook to remote storage

v0.2 is tested on minio backend only + python 2.7 + --notebook-dir option

## usage
click button and write version.
then find your notebook on s3
![Screenshot](docs/screenshot.png)


## install
```
pip install jupyter_extension_publish
jupyter nbextension install --py jupyter_extension_publish
jupyter nbextension enable --py jupyter_extension_publish
jupyter serverextension enable --py jupyter_extension_publish
```

## config
```
c.PublishSettings.s3_access_key_id = 'YOUR_ACCESS_KEY'
c.PublishSettings.s3_secret_access_key = 'YOUR_SECRET_KEY'
c.PublishSettings.s3_endpoint_url = 'YOUR_S3_ENDPOINT'
c.PublishSettings.s3_region_name = 'REGION_NAME'
c.PublishSettings.s3_bucket = 'BUCKET_NAME'
```

## referenced
https://github.com/mozilla/jupyter-notebook-gist

https://github.com/nteract/bookstore
