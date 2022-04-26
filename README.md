# ddi_api

Device data ingestion API

## Technology
- [python (3.10)](https://www.python.org/downloads/release/python-3100/);
- [aiohttp](https://docs.aiohttp.org/en/stable/);
- [fastapi](https://fastapi.tiangolo.com/);
- [influxdb](https://www.influxdata.com/);
- [pandas](https://pandas.pydata.org/);
- [pydantic](https://pydantic-docs.helpmanual.io/);
- [pytest](https://docs.pytest.org/en/7.1.x/);
- [docker](https://www.docker.com/);
- [docker-compose](https://docs.docker.com/compose/).


## Architecture

This is **lightweight** DDD application. The api is the adapter, the use_cases are the domain and the repository
is the bridge between domain and infrastructure.

## Configurations

Following [twelve factor app](https://12factor.net/) rules, all configurations is strictly separated from the application:

| Parameter                          | Description             | Value            |
| ---------------------------------- | ----------------------- | ---------------- |
| `API_HOST`                         | api host                | 0.0.0.0          |
| `API_PORT`                         | api port                | 8000             |
| `INFLUXDB_HOST`                    | influx db host          | influxdb         |
| `INFLUXDB_PORT`                    | influx db port          | 8086             |
| `DOCKER_INFLUXDB_INIT_MODE`        | dev init mode indicator | setup            |
| `DOCKER_INFLUXDB_INIT_BUCKET`      | dev initial bucket      | devices          |
| `DOCKER_INFLUXDB_INIT_USERNAME`    | dev initial user        | influxdbusername |
| `DOCKER_INFLUXDB_INIT_PASSWORD`    | dev initial password    | influxdbpassword |
| `DOCKER_INFLUXDB_INIT_ORG`         | dev initial org         | influxdborg      |
| `DOCKER_INFLUXDB_INIT_ADMIN_TOKEN` | dev initial token       | influxdbtoken    |

## Developing

### Installing

1 - Clone the project

```
git clone git@github.com:rafaeltardivo/ddi-api.git
```

2 - Rename .env_template to .env and populate it with the configurations:

```
mv .env_template .env
// populate env vars...
```

3 - Build the application:

```
make build
```

4 - Run the application:

```
make up
```

### Testing

```
make test
```

### Simulator

```
make simulate
```


## API docs:
[http://localhost:8000/docs](http://localhost:8000/docs)



### Final Considerations

- This project is not "production ready". There's **a lot** to be improved here;
- The async nature of the project is way to compensate for the lack of stream processing (the service is event drive and kafka would do a better job);
- (Unfortunatelly) I was not able to create integrations tests (or even unit tests for the simulator). This would be my next step if I had more time;
- The API is not fully documented;
