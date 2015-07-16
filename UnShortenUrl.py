#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
logging.basicConfig(level=logging.DEBUG)

TIMEOUT = 10
class UnShortenUrl:
    def process(self, url, previous_url=None):
        logging.info('Init url: %s'%url)
        import urlparse
        import httplib
        try:
            parsed = urlparse.urlparse(url)
            if parsed.scheme == 'https':
                h = httplib.HTTPSConnection(parsed.netloc, timeout=TIMEOUT)
            else:
                h = httplib.HTTPConnection(parsed.netloc, timeout=TIMEOUT)
            resource = parsed.path
            if parsed.query != "": 
                resource += "?" + parsed.query
            h.request('HEAD', 
                      resource, 
                      headers={'User-Agent': 'curl/7.38.0'#'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.125 Safari/537.36'}
                               }
                      )
            try:
                response = h.getresponse()
            except:
                logging.error('Timeout for url: %s'%(url))
                raise
            logging.info('Response status: %d'%response.status)
            if response.status/100 == 3 and response.getheader('Location'):
                red_url = response.getheader('Location')
                if red_url.startswith('/'):
                    logging.info('Adding scheme and netloc to the red url')
                    import urlparse
                    parsed_prev_url = urlparse.urlparse(previous_url)
                    red_url = '%s://%s%s'%(parsed_prev_url.scheme, parsed_prev_url.netloc, red_url)
                logging.info('Red, previous: %s, %s'%(red_url, previous_url))
                if red_url == previous_url:
                    return red_url
                return self.process(red_url, previous_url=url) 
            else:
                return url 
        except:
            import traceback
            traceback.print_exc()
            return None
    
