Overview
========

Provides functions to access files on HBASE. For example, connect to Hortonworks (HDP).
This package exposes the `com.ibm.streamsx.hbase` toolkit as Python methods.


Sample
======

A simple hello world example of a Streams application writing string messages to
a file to HBASE. Scan for created file on HBASE and read the content::

    from streamsx.topology.topology import *
    from streamsx.topology.schema import CommonSchema, StreamSchema
    from streamsx.topology.context import submit
    import streamsx.hbase as hbase

    topo = Topology('test_hbase_scan')

    if self.hbase_toolkit_location is not None:
        tk.add_toolkit(topo, self.hbase_toolkit_location)

        if (hbase.generate_hbase_site_xml(topo)):
            tester = Tester(topo)
            scanned_rows = hbase.scan(topo, table_name=_get_table_name(), max_versions=1 , init_delay=2)
            scanned_rows.print()
            tester.tuple_count(scanned_rows, 2, exact=False)

            cfg = {}
            job_config = streamsx.topology.context.JobConfig(tracing='info')
            job_config.add(cfg)
            cfg[streamsx.topology.context.ConfigParams.SSL_VERIFY] = False     

            # Run the test
            tester.test(self.test_ctxtype, cfg, always_collect_logs=True)
        else:
            print("hbase_site_xml file doesn't exist")


Documentation
=============

* `streamsx.hbase package documentation <http://streamsxhbase.readthedocs.io/>`_


