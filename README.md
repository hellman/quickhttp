quickhttp
====================

Notice: <a href="http://python-requests.org">Requests: HTTP for Humans</a> (<a href="https://github.com/kennethreitz/requests">on github</a>) is much better than this one.
Use quickhttp only if you want to run some old script which needs it.

---

This library allows quick http requests with only one call:

```python
from quickhttp import req
print req("http://www.something.com").data
print req("http://www.google.com").headers

req("http://www.example.com",
    headers=headers     # dict or list of strings
    cookie=cookie       # dict or str like "a=b&c=d"
    data=post_data      # dict or str like "a=b&c=d"
    get=get_data        # dict or str like "a=b&c=d"
    auth=(user, pass)   # tuple (HTTP Basic Auth)
    proxy="host:port"   # both for http and https
    proxy_auth=(u, p)   # tuple for proxy auth
    timeout=10          # 10 seconds
)
```

About
---------------------

Author: hellman ( hellman1908@gmail.com )

License: GNU General Public License v2 (http://opensource.org/licenses/gpl-2.0.php)
