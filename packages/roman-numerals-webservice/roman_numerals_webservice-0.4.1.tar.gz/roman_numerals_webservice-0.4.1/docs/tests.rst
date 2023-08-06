====================================
Tests
====================================

To run the unit tests type

.. code-block:: shell
    
    make test

To run code coverage analysis type

.. code-block:: shell
    
    make coverage

This will open a html report in a browser once finished.



..warning ::
    
    The tests will start servers at :code:`localhost:8080`.
    Make sure that this port is free before running the tests
    otherwise the tests might not run properly.