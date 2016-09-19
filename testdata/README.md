TESTDATA
========

The files in this directory compromise a set of test data from a
C-Worker 4 (and possibly other vehicles) manufactured by ASV Global
Ltd. Data logged natively by the C-Worker 4 is done so in a
proprietary format which must be convered to an ASCII CSV file using
the "Data Export Tool" provided by ASV Global. The Data Export Tool
configuraiton can be saved to XML and loaded for subsequent
downloads. A template export configuration can be found in
../bash/bin/ and the script `create_export_config.sh <outputdir>` will
modify the template to produce a new export configuration with the
specified output directory. When the new configuration is loaded
into the GUI or command line export tool, and the export subsequently
run on a log directory, the native logs will be dumped to CSV in
separate files corresponding to major log type, as shown here. 

These log file formats will likely change, requiring versioning of
these test data sets (and code written against them). To be done!
