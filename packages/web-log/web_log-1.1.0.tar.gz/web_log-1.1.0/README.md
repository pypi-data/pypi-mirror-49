# web_log [![Build Status](https://travis-ci.org/equinor/weblog.svg?branch=master)](https://travis-ci.org/equinor/weblog)

The `web_log` (sic) module is a minimal logging module for logging
events to a server, in our case, a
[logstash](https://github.com/elastic/logstash) server.

To install it, the variables in `web_log.constants` need to be updated
according to your needs.

From a user perspective, either use the `wlog` executable, which takes
arguments `application`, `event`, and `extra`, e.g.

```bash
wlog MyApplication crash some_stacktrace_or_message
```

From an API perspective, one can use it with

```python
import web_log
web_log.log('MyApplication',
            'crash',
            'some_extra_stacktrace_or_message',
            async_=True)  # or False
```
