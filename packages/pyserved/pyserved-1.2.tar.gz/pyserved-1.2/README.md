# Pyserved 1.2

## Made by Shaurya Pratap Singh

Transfer files from devices the quickest way possible.
By Shaurya Pratap Singh 2021 | MIT Licence

## Info

This package is used to send files over a network server using sockets. The maximum size of file is 100 mbs.


## Tutorial

Reciever code: 

```python

from pyserved.client import Client

client = Client('0.0.0.0', 5001)
client.listen()
_, address = client.accept()
client.receive()
client.write()
client.close()
```

Sender code:

```python
from pyserved.server import send_file

send_file('LICENSE.txt', '0.0.0.0', 5001)
```

The host and server of client and server should be the same!

## Licence

This project is licensed under the MIT license.The MIT license gives users express permission to reuse code for any purpose, sometimes even if code is part of proprietary software. As long as users include the original copy of the MIT license in their distribution, they can make any changes or modifications to the code to suit their own needs.

## Contribution

Contribute in the code any way you want. Make sure you are following the rules written above in the Licence section.

<!-- #### Dont hesitate the make this code better! -->
<!-- #### © Shaurya Pratap Singh 2021 -->

#### Huge thanks to my dad for inspiration!
