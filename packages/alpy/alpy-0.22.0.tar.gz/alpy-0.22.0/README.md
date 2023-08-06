# Alpy

*Test network virtual appliance using Docker containers*

This project is a Python library for testing network virtual appliances.

The appliance being tested is referred to as a *device under test* or *DUT*.

This repository includes scripts and modules to build a simple appliance called
Rabbit. Rabbit is Alpine Linux with a few packages pre-installed. Having this
simple DUT allows to quickly test the alpy library and to demonstrate its
features.

The tests for the Rabbit device share a lot of code so the code is organized as
a library. The library is called *carrot*.

Author
------

Alexey Bogdanenko

License
-------

Alpy is licensed under:

    SPDX-License-Identifier: GPL-3.0-or-later

See COPYING for more details.

Network design
--------------

The DUT communicates with containers attached to each of its network links.

Guest network adapters are connected to the host via tap devices (Figure 1).

```
+-----QEMU hypervisor------+
|                          |   +-------------+
| +-----Guest OS-----+     |   |             |
| |                  |     |   |  docker     |
| | +--------------+ |     |   |  container  |
| | |              | |     |   |  network    |
| | |  NIC driver  | |     |   |  namespace  |
| | |              | |     |   |             |
| +------------------+     |   |   +-----+   |
|   |              |       |   |   |     |   |
|   | NIC hardware +---+-----------+ tap |   |
|   |              |   |   |   |   |     |   |
|   +--------------+   |   |   |   +-----+   |
|                      |   |   |             |
+--------------------------+   +-------------+
                       |
                       |
                       v
                 +-----------+
                 |           |
                 | pcap file |
                 |           |
                 +-----------+
```

*Figure 1. Network link between QEMU guest and a docker container.*

Each tap device lives in its network namespace. This namespace belongs to a
dedicated container - a *node*. The node's purpose is to keep the namespace
alive during the lifetime of a test.

For an application to be able to communicate with the DUT the application is
containerized. The application container must be created in a special way: it
must share network namespace with one of the nodes.

Figure 2 shows an example where application containers *app0* and *app1* share
network namespace with node container *node0*. Application container *app2*
shares another network namespace with *node2*.

This sharing is supported by Docker. All we have to do is to create the
application container with the `--network=container:NODE_NAME` Docker option.
For example, if we want to send traffic to the DUT via its first link, we create
a traffic generator container with Docker option `--network=container:node0`.

```
+----QEMU---+   +------shared network namespace-----+
|           |   |                                   |
|           |   |    eth0                           |
|   +---+   |   |   +---+   +-----+ +----+ +----+   |
|   |NIC+-----------+tap|   |node0| |app0| |app1|   |
|   +---+   |   |   +---+   +-----+ +----+ +----+   |
|           |   |                                   |
|           |   +-----------------------------------+
|           |
|           |
|           |
|           |   +------shared network namespace-----+
|           |   |                                   |
|           |   |    eth0                           |
|   +---+   |   |   +---+   +-----+                 |
|   |NIC+-----------+tap|   |node1|                 |
|   +---+   |   |   +---+   +-----+                 |
|           |   |                                   |
|           |   +-----------------------------------+
|           |
|           |
|           |
|           |   +------shared network namespace-----+
|           |   |                                   |
|           |   |    eth0                           |
|   +---+   |   |   +---+   +-----+ +----+          |
|   |NIC+-----------+tap|   |node2| |app2|          |
|   +---+   |   |   +---+   +-----+ +----+          |
|           |   |                                   |
+-----------+   +-----------------------------------+
```

*Figure 2. Application containers attached to the DUT links.*

A note about GitLab Container Registry
--------------------------------------

Many CI jobs use one of the custom images built on the "build-docker-images"
stage. The images are stored in the GitLab Container Registry.

The images are pulled from locations specified by GitLab variables. By default,
the variables point to the registry of the current GitLab project.

If you forked this project and GitLab Container Registry is disabled in your
project, override the variables on a project level so that the images are pulled
from some other registry.

For example, set `IMAGE_ALPINE=registry.gitlab.com/abogdanenko/alpy/alpine`.
