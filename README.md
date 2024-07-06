Based on [RAGapp](https://github.com/ragapp/ragapp) and [FastAPI Template](https://github.com/idashevskii/fastapi-postgres-template)


## Deploy to Production

Generate DH params

```sh
openssl dhparam -out ./services/reverse-proxy/ssl/dh-params.pem 2048
```

Generate Self signed cert

```sh
openssl req -x509 -nodes -days 3650 -newkey rsa:2048 -keyout ./services/reverse-proxy/ssl/self-signed/key.pem -out ./services/reverse-proxy/ssl/self-signed/cert.pem
```

Copy file `.env.example` to `.env` and adjust configuration.

Run services in prod mode:

```bash
./bin/prod-run.sh
```
## Прозрачность кода

## Automatic Parser
Репозиторий: https://github.com/Nizier193/cp-24-skfo-parser

## TgBot
Демо: https://t.me/rustore_manager_bot

Репозиторий: https://github.com/Nizier193/cp-24-skfo-tg-bot

## Admin Page
Демо: https://cp-24-skfo.open-core.ru/admin

![img_1.png](docs/images/img_1.png)
## User Page
Демо: https://cp-24-skfo.open-core.ru/ui

![img.png](docs/images/img.png)

## Architecture

![img_2.png](docs/images/img_2.png)
