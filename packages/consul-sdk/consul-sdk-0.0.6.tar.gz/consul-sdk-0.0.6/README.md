# Consul SDK

Consul library to use locks on consul.

### Basic Usage

    In [1]: from consul_sdk import ConsulClient, ConsulLock, UnableToAcquireLock

    In [2]: client = ConsulClient(node_name=None, service_name=None, token="abc")

    In [3]: client
    Out[3]: <consul_sdk.client.ConsulClient at 0x10206add8>

    In [4]: with ConsulLock(client, "my-key"):
       ...:     import time
       ...:     print("Hi")
       ...:     time.sleep(5)
       ...:     print("Bye")
       ...:
    Hi
    Bye

### Releasing

- `make bump_patch_version`
- Update [the Changelog](https://github.com/Shuttl-Tech/pyshuttlis/blob/master/Changelog.md)
- Commit changes to `Changelog`, `setup.py` and `setup.cfg`.
- `make release` (this'll push a tag that will trigger a Drone build)
