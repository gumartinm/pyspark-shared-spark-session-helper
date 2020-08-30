import os
import sys

from pylint.config import find_pylintrc


src = os.path.join(os.path.dirname(find_pylintrc()), 'src')
tests = os.path.join(os.path.dirname(find_pylintrc()), 'tests')
current = os.path.dirname(find_pylintrc())

sys.path.append(src)
sys.path.append(tests)
sys.path.append(current)
