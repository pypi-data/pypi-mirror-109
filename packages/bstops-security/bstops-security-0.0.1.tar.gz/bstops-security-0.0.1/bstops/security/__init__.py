import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from .pass64 import pass_encode, pass_decode
from .totp import TOTP
