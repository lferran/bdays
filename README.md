# bdays
simple app to get reminders about friend's birthdays



## Docker compose


## Docker development

Create a newtwork
```
docker network create --driver bridge network-test
```

Start postgresql container
```
docker run -dit --rm --name pg --network network-test -e POSTGRES_DB=guillotina postgres:9.6.16
```

Build bdays backend image
```
docker build --network host -t bdays .
```

Run it

```
docker run --rm -dit --name bdays --network network-test -p 8080:8080 -d bdays:latest
```

You can now create new bdays and list them

```
curl -XPOST "http://localhost:8080/bday" --data-binary '{"name": "FooBar", "day": 12, "month": 11, "year": 1991}'

curl "http://localhost:8080/bdays/list"
[{"id":1,"name":"FooBar","surname":null,"day":12,"month":11,"year":1991}]
```
