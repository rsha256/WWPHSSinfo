# Deploy 

### Automatically

1. Run the `prepdeploy.sh` script
2. Use the AppEngine Launcher to deploy


### Manually

##### Git:
1. Commit to git

##### static files:
1. Create `staticfiles` directory in project root
2. run: `python manage.py collectstatic`

##### Secret Key:
 This should be loaded automatically provided the 
 datastore is setup correctly. Ensure that ApplicationSettings 
 exists and has `SECRET_KEY`, `GAUTH_KEY` and `GAUTH_SECRET` entries set. 

##### AppEngine:
1. Use the AppEngine Launcher to deploy


_Note: Django 2.0 cannot be deployed on the AppEngine Standard Environment 
as python 3 is not supported. Do not upgrade to Django 2_