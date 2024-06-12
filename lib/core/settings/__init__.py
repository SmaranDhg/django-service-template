import os
from dotenv import load_dotenv

mode = os.environ.get("MODE", "local").lower()

if mode in ["prod", "stage"]:
    from .prod import *
elif mode == "dev":
    from .dev import *
elif mode == "local":
    from .local import *
else:
    load_dotenv(override=True)
    from .local import *


print(os.environ.get("MODE"))
