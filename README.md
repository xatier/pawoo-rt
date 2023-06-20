# pawoo-rt

<p align="center">
<a href="https://github.com/xatier/pawoo-rt/blob/master/.github/workflows/test.yaml"><img alt="Test Status" src="https://github.com/xatier/pawoo-rt/actions/workflows/test.yaml/badge.svg"></a>
</p>

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
