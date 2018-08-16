# clamdscan via REST in single container

## Abstraction

clamAV deamon, pattern update, REST endpoint with single container.
inspired by https://github.com/uktrade/dit-clamav-rest

## running

`docker build -t <yourtag> .`
`docker run -v <your volume>:/var/lib/clamav　-e "AUTH_USER=user" -e "AUTH_PASSWORD=password" -p 8080:8080 <yourtag>`

then, test by curl.

`curl -X POST -u user:password -F "file=@your.file" http://localhost:8080/scan`

OK response is below.

```json
{
  "reason": null,
  "time": 2.8135181999532506,
  "valid": true
}
```

NG response example is below.

```json
{
  "reason": "Eicar-Test-Signature",
  "time": 0.003237200027797371,
  "valid": false
}
```

## Volumes

I recomend to mount `/var/lib/clamav` directory as volume because ClamAV pattern files save at `/var/lib/clamav`. 

## ENV

+ AUTH_USER - user name for basic auth
+ AUTH_PASSWORD - user password for basic auth

