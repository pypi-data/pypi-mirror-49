HitBTC Library
-------------------

A library for better communication with HitBTC Exchange API
(`HitBTC API Documentation <https://api.hitbtc.com>`_)

Installation:
~~~~~~~~~~~~~~~
.. code:: bash

    pip install HitBTCMonster


Example:
~~~~~~~~~

API
**********

.. code:: python

    from HitBTCMonster.api.core import HitBTC
    from HitBTCMonster.api.market import Market
    from HitBTCMonster.api.trading import Trading

    CORE = HitBTC(
        public='YOUR_PUBLIC_KEY_HERE',
        secret='YOUR_SECRET_KEY_HERE',
    )
    MARKET = Market(CORE)
    TRADING = Trading(CORE)

    # do stuff


WebSocket
****************

.. code:: python

    from HitBTCMonster.wss.core import HitBTC
    from HitBTCMonster.wss.market import Market
    from HitBTCMonster.wss.trading import Trading

    CORE = HitBTC(
        public='YOUR_PUBLIC_KEY_HERE',
        secret='YOUR_SECRET_KEY_HERE',
    )
    MARKET = Market(CORE)
    TRADING = Trading(CORE)

    # do stuff