# notify_me
```
# To start service:
docker-compose up -d --build

# To stop service:
docker-compose down
```

API check health:
REQUEST:  http://domain.local:5252/ping
RESPONSE: PONG

API url:
http://domain.local:5252/api/email
http://domain.local:5252/api/telegram

HEADER:
{
  'Content-Type': 'application/json',
  'X-NOTIFY-API-Key': '55585dcbd7'
}
BODY:
{
	"type": "email",
	"address": "who@mail.ru",
	"message": "I'm from INSOMNIA"
}
OR
{
	"type": "telegram",
	"address": "34795934857",
	"message": "I'm from INSOMNIA"
}
