Building Kornia packages for release
====================================

Wheels
------

Linux
#####

In order to generate wheels define ```KORNIA_BUILD_VERSION```.

.. code:: bash

    KORNIA_BUILD_VERSION=0.x.x ./build_wheel.sh

This will produce a ```*whl``` file under ```OUT_DIR```, by default to ```/tmp```.
You can upload the wheels using `Twine <https://pypi.org/project/twine/>`_

.. code:: bash

    cd /tmp/remote
    python3 -m twine upload *.whl
