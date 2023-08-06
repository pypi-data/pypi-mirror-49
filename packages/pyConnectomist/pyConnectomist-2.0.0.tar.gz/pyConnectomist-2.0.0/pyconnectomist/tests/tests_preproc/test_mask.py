##########################################################################
# NSAp - Copyright (C) CEA, 2016
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

"""
Mocking Popen directly - need to construct a Mock to return, and adjust its
communicate() return_value.
The benefit of this approach is in not needing to do the strip/split on your
fake return string.
"""

# System import
import unittest
import sys
import os
import nibabel
import numpy
# COMPATIBILITY: since python 3.3 mock is included in unittest module
python_version = sys.version_info
if python_version[:2] <= (3, 3):
    import mock
    from mock import patch
else:
    import unittest.mock as mock
    from unittest.mock import patch

# pyConnectomist import
from pyconnectomist.preproc.mask import rough_mask_extraction
from pyconnectomist.exceptions import ConnectomistBadFileError


class ConnectomistMask(unittest.TestCase):
    """ Test the Connectomist 'Rough mask' tab:
    'pyconnectomist.preproc.mask.rough_mask_extraction'
    """
    def setUp(self):
        """ Run before each test - the mock_popen will be available and in the
        right state in every test<something> function.
        """
        # Mocking popen
        self.popen_patcher = patch("pyconnectomist.wrappers.subprocess.Popen")
        self.mock_popen = self.popen_patcher.start()
        mock_process = mock.Mock()
        attrs = {
            "communicate.return_value": ("mock_OK", "mock_NONE"),
            "returncode": 0
        }
        mock_process.configure_mock(**attrs)
        self.mock_popen.return_value = mock_process
        self.kwargs = {
            "outdir": "/my/path/mock_outdir",
            "raw_dwi_dir": "/my/path/mock_rawdwidir",
            "registration_dir": "/my/path/mock_registrationdir",
            "morphologist_dir": "/my/path/mock_morphologistdir",
            "subject_id": "Lola",
            "level_count": 32,
            "lower_theshold": 0.0,
            "apply_smoothing": True
        }
        self.t1img = nibabel.Nifti1Image(numpy.zeros((2, 3, 4)), numpy.eye(4))

    def tearDown(self):
        """ Run after each test.
        """
        self.popen_patcher.stop()

    def test_badfileerror_raise(self):
        """ A wrong input -> raise ConnectomistBadFileError.
        """
        # Test execution
        self.assertRaises(ConnectomistBadFileError,
                          rough_mask_extraction, **self.kwargs)

    @mock.patch("pyconnectomist.preproc.mask.ConnectomistWrapper."
                "_connectomist_version_check")
    @mock.patch("pyconnectomist.preproc.mask.ConnectomistWrapper."
                "create_parameter_file")
    @mock.patch("os.path")
    @mock.patch("pyconnectomist.preproc.registration.glob.glob")
    @mock.patch("pyconnectomist.preproc.registration.nibabel.load")
    def test_normal_execution(self, mock_load, mock_glob, mock_path,
                              mock_params, mock_version):
        """ Test the normal behaviour of the function.
        """
        # Set the mocked functions returned values
        mock_load.return_value = self.t1img
        mock_glob.side_effect = [
            [self.kwargs["morphologist_dir"] + os.sep +
             "{0}.nii.gz".format(self.kwargs["subject_id"])],
            []]
        mock_params.return_value = "/my/path/mock_parameters"
        mock_path.isfile.side_effect = [True, True, True, False]

        # Test execution
        outdir = rough_mask_extraction(**self.kwargs)
        self.assertEqual(outdir, self.kwargs["outdir"])
        self.assertTrue(len(mock_params.call_args_list) == 1)


if __name__ == "__main__":
    unittest.main()
