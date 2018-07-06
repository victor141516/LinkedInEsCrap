# LinkedIn email to profile

## How to use
```
$ docker build -t linkedinescrap.

$ docker run --rm -d \
    --name linkedinescrap \
    -e SCRAP_EMAIL=youremail@asd.com \
    -e SCRAP_PASS=yourpassword \
    linkedinescrap
```

SCRAP_EMAIL and SCRAP_PASS are any LinkedIn credentials
You may need to login to LinkedIn from the server once to avoid 2FA
