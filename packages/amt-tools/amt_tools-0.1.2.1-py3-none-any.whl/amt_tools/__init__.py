"""
Should be able to use the following import structures (e.g.):
------------------------------------------------------------
import amt_tools
amt_tools.train()
amt_tools.Estimator()
amt_tools.Evaluator()
------------------------------------------------------------
from amt_tools import train
train()
------------------------------------------------------------
from amt_tools.train import train
train()
"""

# Subpackages
from . import datasets
from . import features
from . import models
from . import tools

# Scripts
from . import evaluate
from . import train
from . import transcribe
