# proxy
proxy fetcher from hidemyna.me
Can either be used as a class and return a list of proxies, or can work as standalone script and save proxies to the file.

import proxy

proxy_list = proxy.fetch(512)  # Will return 512 different proxies as list of strings with ip:port pattern
