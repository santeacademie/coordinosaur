COORDINOSAUR
============

![Coordinosaur](./asset/coordinosaur.png)

Coordinosaur is a simple task coordinator able to:
- Coordinate multiple clients over MQTT
- Concurrently grant job execution privilege
- Handle rate limit over an arbitrary interval duration
- Use channels to separate different coordinator logic  

**It doesn't execute jobs but allows a client to execute a job according to pre-defined rules.**

Rules:
-
- `MAX_CONCURRENT_JOBS`: `int` = How many job in parallel can be executed
- `TIMEOUT_OFFSET`: `int` = Add timeout offset value to registration timeout value
- `QUOTAS_PER_INTERVAL`: `json` 
```js
var exemple = {
  60:   {"name": "minute", "limit": 15, "log": "v"},  // Only 15 requests per minute (log quotas is verbose)
  3600: {"name": "hour", "limit": 100, "log": "q"}    // Only 100 requests per hour (log quotas is quiet) 
}
```
- `CHANNEL_OPTIONS`: `json` = Custom rules per channel (using regex)
```js
var exemple = {
  "test(.+)": {
      "TIMEOUT_OFFSET": 1,
      "MAX_CONCURRENT_JOBS": 2,
      "QUOTAS_PER_INTERVAL": {}
  }
}
``` 

Client API:
-

>Registration (Publish):
- **Topic** = `/coordinosaur/{channel}/register`
- **Payload** : `json`
```js
var exemple = {
  "uid": "string (client muse choose a job uid)",
  "timeout": "int"
}
```

>Go (Subscribe):
- **Topic** = `/coordinosaur/{channel}/go/{uid}`
- **Payload** : `str` = Job `uid` value

>Finished (Publish):
- **Topic** = `/coordinosaur/{channel}/finished`
- **Payload** : `str` = Job `uid` value

>Aborted (Publish):
- **Topic** = `/coordinosaur/{channel}/aborted`
- **Payload** : `str` = Job `uid` value

>Set concurrency for channel (Publish):
- **Topic** = `/coordinosaur/{channel}/concurrency/set`
- **Payload** : `int` = New `MAX_CONCURRENT_JOB` value for `{channel}`
