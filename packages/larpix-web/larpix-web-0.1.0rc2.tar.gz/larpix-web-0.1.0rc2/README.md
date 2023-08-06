LArPix Web Interface
====================

Installation instructions
-------------------------

Create a new [virtual
environment](https://larpix-daq.readthedocs.io/en/latest/guide/install.html#virtual-environment)
or use one that already has larpix-daq installed.

Then install the web interface with ``pip install larpix-web``.

All the dependencies including larpix-daq will be installed. If you
want to use a specific version of larpix-daq, pip-install it first with
``pip install larpix-daq==x.y.z`` (specifying the version for
``x.y.z``). This version of larpix-web is compatible with v0.2.x of
larpix-daq.

Launching the web server
------------------------

To launch the web server, simply run:

```
python -m larpixweb.server
```

The server can then be accessed by visiting <http://localhost:5000>.

The server log is saved at the hardcoded location ``larpixweb.log`` in
the directory you start the server process.
