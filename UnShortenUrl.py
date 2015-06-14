#!/usr/bin/env python
# -*- coding: utf-8 -*-



class UnShortenUrl:
    def process(self, url, previous_url=None):
        import urlparse
        import httplib
        try:
            parsed = urlparse.urlparse(url)
            if parsed.scheme == 'https':
                h = httplib.HTTPSConnection(parsed.netloc)
            else:
                h = httplib.HTTPConnection(parsed.netloc)
            resource = parsed.path
            if parsed.query != "": 
                resource += "?" + parsed.query
            h.request('HEAD', resource )
            response = h.getresponse()
            if response.status/100 == 3 and response.getheader('Location'):
                red_url = response.getheader('Location')
                if red_url == previous_url:
                    return red_url
                return self.process(red_url, previous_url=url) 
            else:
                return url 
        except:
            import traceback
            traceback.print_exc()
            return None
    