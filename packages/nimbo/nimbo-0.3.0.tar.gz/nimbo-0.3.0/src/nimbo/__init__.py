import re
import sys

import pkg_resources
import pydantic

import nimbo.core.config
import nimbo.tests.aws.config
from nimbo.core.constants import IS_TEST_ENV

version = pkg_resources.get_distribution("nimbo").version


try:
    if IS_TEST_ENV:
        CONFIG = nimbo.tests.aws.config.make_config()
    else:
        CONFIG = nimbo.core.config.make_config()
except pydantic.error_wrappers.ValidationError as e:
    e_msg = str(e)
    e_num = len(e.errors())
    title_end = e_msg.index("\n", 1)
    new_title = f"{e_num} error{'' if e_num == 1 else 's'} in nimbo-config.yml\n"
    print(new_title + re.sub(r"\(type=.*\)", "", e_msg[title_end:]))
    sys.exit(1)
