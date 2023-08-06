##########################################################################
# NSAp - Copyright (C) CEA, 2016
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# System import
import unittest
import sys
import os
# COMPATIBILITY: since python 3.3 mock is included in unittest module
python_version = sys.version_info
if python_version[:2] <= (3, 3):
    import mock
    from mock import patch
    mock_builtin = "__builtin__"
else:
    import unittest.mock as mock
    from unittest.mock import patch
    mock_builtin = "builtins"

# pyConnectomist import
from pyconnectomist.wrappers import ConnectomistWrapper


class ConnectomistWrappers(unittest.TestCase):
    """ Test the Connectomist wrappers:
    'pyconnectomist.wrappers.ConnectomistWrapper'
    """
    @mock.patch("os.path")
    def test_badfileerror_raise(self, mock_path):
        """ Bad configuration file -> raise ValueError.
        """
        # Set the mocked functions returned values
        mock_path.isfile.side_effect = [False]

        # Test execution
        self.assertRaises(ValueError,
                          ConnectomistWrapper._connectomist_version_check,
                          "/my/path/mock_conf")

    @mock.patch("{0}.ValueError".format(mock_builtin))
    @mock.patch("{0}.open".format(mock_builtin))
    @mock.patch("os.path")
    def test_noreleaseerror_raise(self, mock_path, mock_open, mock_error):
        """ No PTK release found -> raise ValueError.
        """
        # Set the mocked functions returned values
        mock_path.isfile.side_effect = [True]
        mock_context_manager = mock.Mock()
        mock_open.return_value = mock_context_manager
        mock_file = mock.Mock()
        mock_file.read.return_value = "WRONG"
        mock_enter = mock.Mock()
        mock_enter.return_value = mock_file
        mock_exit = mock.Mock()
        setattr(mock_context_manager, "__enter__", mock_enter)
        setattr(mock_context_manager, "__exit__", mock_exit)

        # Test execution
        ConnectomistWrapper._connectomist_version_check("/my/path/mock_conf")
        self.assertEqual(len(mock_error.call_args_list), 1)

    @mock.patch("warnings.warn")
    @mock.patch("{0}.open".format(mock_builtin))
    @mock.patch("os.path")
    def test_normal_execution(self, mock_path, mock_open, mock_warn):
        """ Test the normal behaviour of the function.
        """
        # Set the mocked functions returned values
        mock_path.isfile.side_effect = [True]
        mock_context_manager = mock.Mock()
        mock_open.return_value = mock_context_manager
        mock_file = mock.Mock()
        mock_file.read.return_value = "PTK_RELEASE=4.0\n"
        mock_enter = mock.Mock()
        mock_enter.return_value = mock_file
        mock_exit = mock.Mock()
        setattr(mock_context_manager, "__enter__", mock_enter)
        setattr(mock_context_manager, "__exit__", mock_exit)

        # Test execution
        ConnectomistWrapper._connectomist_version_check("/my/path/mock_conf")
        self.assertEqual(len(mock_warn.call_args_list), 1)


if __name__ == "__main__":
    unittest.main()
