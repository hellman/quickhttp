"""
quickhttp - module for quick http requests
Usage:

import quickhttp
quickhttp.req("http://www.google.com",
    headers=headers     # dict or list of strings
    cookie=cookie       # dict or str like "a=b&c=d"
    data=post_data      # dict or str like "a=b&c=d"
    get=get_data        # dict or str like "a=b&c=d"
    auth=(user, pass)   # tuple (HTTP Basic Auth)
    proxy="host:port"   # both for http and https
    proxy_auth=(u, p)   # tuple for proxy auth
    timeout=10          # 10 seconds
)

Author: Author: hellman ( hellman1908@gmail.com )
License: GNU GPL v2 ( http://opensource.org/licenses/gpl-2.0.php )
"""

import sys
import urllib
import urllib2
from MultipartPostHandler import MultipartPostHandler as UploadHandler

_PASSWORD_MGR = urllib2.HTTPPasswordMgrWithDefaultRealm


class req():
    def __init__(self, url, headers=None, cookie=None, data=None, get=None,
                 auto_redirect=True, auth=None, proxy=None, proxy_auth=None,
                                                                timeout=10):
        self.url = url
        self.is_file_post = False
        self.data = None
        self.request_headers = {"User-Agent": "Mozilla/5.0"}

        if "://" not in url:
            self.url = "http://" + self.url

        if get:
            self.update_get(get)

        if headers:
            self.update_headers(headers)

        if cookie:
            self.update_cookie(cookie)

        if data:
            self.update_data(data)

        handlers = []
        if proxy:
            handlers.append(self.proxy_handler(proxy))
        if proxy_auth:
            handlers.append(self.proxy_auth_handler(proxy_auth))
        if auth:
            handlers.append(self.auth_handler(auth))
        if self.is_file_post:
            handlers.append(UploadHandler)

        opener = urllib2.build_opener(*handlers)
        if not auto_redirect:
            for code in [301, 302, 303, 307]:
                del opener.handle_error['http'][code]
        opener.addheaders = self.request_headers.items()
        
        try:
            res = opener.open(self.url, self.data, timeout)
        except urllib2.HTTPError as err:
            self.data = None
            self.status = err.getcode()
            self.msg = err.msg  # Code string
            self.headers = _raw_headers_to_dict(str(err.headers))
        else:
            self.data = res.read()
            self.status = res.code
            self.headers = res.headers.dict
        return

    def auth_handler(self, auth):
        h = urllib2.HTTPBasicAuthHandler(_PASSWORD_MGR())
        h.add_password(None, self.url, auth[0], auth[1])
        return h

    def proxy_handler(self, proxy):
        h = urllib2.ProxyHandler({'http': proxy, 'https': proxy})
        return h

    def proxy_auth_handler(self, proxy_auth):
        h = urllib2.ProxyBasicAuthHandler(_PASSWORD_MGR())
        h.add_password(None, self.url, proxy_auth[0], proxy_auth[1])
        return h

    def redirect_handler(self):
        return urllib2.HTTPRedirectHandler()
        
    def update_get(self, get):
        if type(get) == str:
            get = _dict_from_str(get, "&", "=")

        if "?" in self.url and self.url[-1] != "?":
            self.url += "&"
        if "?" not in self.url:
            self.url += "?"
        
        
        gets = []
        for key in get:
            gets.append(urllib.quote(str(key)) + "=" + urllib.quote(str(get[key])))
        get_str = "&".join(gets)

        self.url += get_str
        return

    def update_headers(self, headers):
        if type(headers) == dict:
            self.request_headers.update(headers)
        if type(headers) == list:
            for h in headers:
                if type(h) == str:
                    name, value = h.split(": ", 1)
                    self.request_headers[name] = value
                elif type(h) == tuple:
                    self.request_headers[str(h[0])] = str(h[1])
        return

    def update_cookie(self, cookie):
        if type(cookie) == str:
            cookie = _dict_from_str(cookie, "&", "=")

        cookies = []
        for key in cookie:
            cookies.append(urllib.quote(str(key)) + "=" + urllib.quote(str(cookie[key])))
        cookie_str = "; ".join(cookies)

        if "Cookie" in self.request_headers:
            c = ""
            if self.request_headers["Cookie"].strip()[-1] != ";":
                c = "; "
            self.request_headers["Cookie"] += c + cookie_str
        else:
            self.request_headers["Cookie"] = cookie_str
        return

    def update_data(self, data):
        if type(data) == str:
            data = _dict_from_str(data, "&", "=")

        str_data = {}
        for key, value in data.iteritems():
            if type(value) == file or hasattr(value, "upload_name"):
                self.is_file_post = True
                str_data[str(key)] = value
            else:
                str_data[str(key)] = str(value)
        
        if self.is_file_post:
            self.data = str_data  # Multipart handler encodes it byself
        else:
            self.data = urllib.urlencode(str_data)
        return


def _dict_from_str(data, item_sep, key_sep):
    lst = data.split(item_sep)
    d = {}
    for pair in lst:
        key, value = pair.split(key_sep, 1)
        d[key] = value
    return d


def _raw_headers_to_dict(s):
    headers = {}
    s = s.strip()
    for line in s.split("\n"):
        line = line.strip()
        pos = line.find(":")
        key, value = line[:pos], line[pos+1:].strip()
        key = key.lower()
        headers[key] = value
    return headers