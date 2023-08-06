


**iputils**

iputils is the wrapper of ipaddress.py, easy for use.


**Install**

pip install iputils



**Usage**

.. code-block:: python

    from iputils import IPUtils

    print(IPUtils.is_valid("1988.0.0.1/22"))
    print(IPUtils.is_ipv4("199.201.90.100/22"))
    print(IPUtils.is_ipv6("2001::1/64"))
    print(IPUtils.is_network("2001::/64"))
    print(IPUtils.get_network_addr("199.201.90.100/22"))
    print(IPUtils.with_prefix("199.201.90.100/255.255.252.0"))

    and more... see the api docs

