#!/bin/sh
'''exec' "/home/greva/Downloads/Cybersecurity/Challenge/Software/da risolvere/FrittoDisordinato/python/bin/python3" "$0" "$@"
' '''
# -*- coding: utf-8 -*-
import re
import sys
from rpyc.cli.rpyc_registry import main
if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(main())