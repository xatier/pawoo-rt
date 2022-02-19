# pawoo-rt

Server code used for my pawoo retweet iOS shortcut and [Tootthat](https://github.com/xatier/tootthat).

The shortcut makes the following `POST` request:

```bash
curl -LSsvX POST -d '{"token":"TOKEN", "status":"https://twitter.com/user/status/1111111111111111111"}' \
    -H "Content-Type: application/json" \
    'https://pawoo-rt.<azure region>.azurecontainer.io/do' | jq

# response
{
  "status": "<sanitized twitter content>"
}
```
