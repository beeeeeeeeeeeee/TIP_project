# Change the file name under TIP_Project Folder

settings_please_change.py => settings.py

# Change the content of the settings

*# FOR MAP VISUALISATION*

GOOGLE_API_KEY = 'Your Key'



*# FOR S3 BUCKET*

ACCESS_KEY = "Your Key"

ACCESS_SECRET = "Your Access Secret"

BUCKET_NAME = "Your AWS Bucket Name"



*# FOR DataBase*

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'Your Database Name',
        'USER': 'Your MySql User Name',
        'PASSWORD': 'Your MySQL Password',
        'HOST': 'localhost',  # "127.0.0.1" == "localhost"
        'PORT': 3306,
    }
}