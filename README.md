
# bdays

Simple toy app to keep track of friends & family birthdays.

![Screenshot from 2021-03-15 10-07-26](https://user-images.githubusercontent.com/11825427/111129387-53976d00-8576-11eb-8d76-756732c09881.png)

- Sqlalchemy and postgresql for storage
- Fast-api and uvicorn for rest-api serving
- VueJS front-end

## Front-end

```
cd src/frontend
npm install
npm run serve
```

## Backend

### Docker compose

```
docker-compose up
```

### Docker development

Create a docker network
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
