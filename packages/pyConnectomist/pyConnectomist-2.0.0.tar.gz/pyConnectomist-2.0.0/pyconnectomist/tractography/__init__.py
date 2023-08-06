##########################################################################
# NSAp - Copyright (C) CEA, 2015 - 2016
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html for details.
##########################################################################

"""
Each tractography step (i.e. one Connectomist tab) can be run through the use
of a dedicated function of the package.

All the tractography steps can be done at once calling the
'complete_tractography' function.
"""

from .all_steps import complete_tractography
from .all_steps import STEPS
