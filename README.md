# Floki Inu token metrics

Gather metrics from the official `Floki Inu` website periodically and post it to Prometheus logs. Visualize data with Grafana.

## Prerequisites:

- Create `grafana-storage` volume for Grafana persistent data:
```
$ docker volume create grafana-storage
```
- Create `.env` file the with following content:
```
# your password for Grafana user
GF_SECURITY_ADMIN_PASSWORD=xxxxx
```

## Running

Run Docker containers in detached mode:
```
$ docker compose up -d
```

Navigate to `localhost:3000` and login to Grafana using the `admin` user and your password. On `Floki Inu` dashboard you can find all metrics.

(Optional) You may check Prometheus logs on `localhost:9090`.

Use this command to stop services:
```
$ docker compose down
```
