# -*- coding:utf-8 -*-
import sys
print('importDeadline')
if sys.version_info[0] == 2:
    from .Deadline2 import DeadlineConnect
    print('importDeadline2')
else:
    from .Deadline3 import DeadlineConnect
    print('importDeadline3')