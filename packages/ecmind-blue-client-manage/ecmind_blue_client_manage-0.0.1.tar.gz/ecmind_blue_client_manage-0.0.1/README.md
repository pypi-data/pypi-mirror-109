# ECMind blue client: Manage

git remote add origin https://gitlab.ecmind.ch/open/ecmind_blue_client_manage.git. See discussion here: https://hub.ecmind.ch/t/119

## Installation

`pip install ecmind_blue_client_manage`


## Usage

```python
from ecmind_blue_client.tcp_client import TcpClient as Client
from ecmind_blue_client_manage import manage

client = Client(hostname='localhost', port=4000, appname='test', username='root', password='optimal')
print(manage.get_users(self.client))
```