# coding: utf-8
# Copyright (c) 2016, 2019, Oracle and/or its affiliates. All rights reserved.

import os
import pkgutil
from os.path import abspath
from inspect import getsourcefile
CLIENT_MAP = {}
MODULE_TO_TYPE_MAPPINGS = {}
ALL_SERVICES_DIR = "services"

this_file_path = abspath(getsourcefile(lambda: 0))
if "site-packages" in this_file_path:
    python_cli_root_dir = this_file_path[0:this_file_path.index("oci_cli")]
else:
    python_cli_root_dir = this_file_path[0:this_file_path.index("/src/oci_cli")]
services_dir = os.path.join(python_cli_root_dir, ALL_SERVICES_DIR)

# Import client mappings from platformization directories.
# This imports the generated client_mappings which populates CLIENT_MAP and MODULE_TO_TYPE_MAPPINGS.
for importer1, modname1, ispkg1 in pkgutil.iter_modules(path=[services_dir]):
    for importer, modname, ispkg in pkgutil.iter_modules(path=[services_dir + '/' + modname1 + '/src']):
        if ispkg and modname.startswith("oci_cli_"):
            oci_cli_module_name = modname.split(".")[0]
            service_name = oci_cli_module_name[8:]
            oci_cli_module = __import__(ALL_SERVICES_DIR + '.' + modname1 + '.src.' + oci_cli_module_name)
            services_dir = oci_cli_module.__path__[0]
            service_dir = os.path.join(services_dir, modname1, 'src', oci_cli_module_name)
            generated_module = "client_mappings"
            if os.path.isfile(os.path.join(service_dir, 'generated', generated_module + ".py")):
                __import__(ALL_SERVICES_DIR + '.' + modname1 + '.src.' + oci_cli_module_name + ".generated." + generated_module)
