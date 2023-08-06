##########################################################################
# NSAp - Copyright (C) CEA, 2015
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html for details.
##########################################################################

"""
Wrapper to Connectomist's 'DWI & Q-space' tab.
"""

# System import
import os
import shutil
import numpy as np
import nibabel
import warnings

# pyConnectomist import
from pyconnectomist import DEFAULT_CONNECTOMIST_PATH
from pyconnectomist.manufacturers import MANUFACTURERS
from pyconnectomist.exceptions import ConnectomistError
from pyconnectomist.exceptions import ConnectomistBadManufacturerNameError
from pyconnectomist.exceptions import ConnectomistBadFileError
from pyconnectomist.wrappers import ConnectomistWrapper
from pyconnectomist.utils.dwitools import read_bvals_bvecs
from pyconnectomist.utils.filetools import ptk_nifti_to_gis

# Define axis mapping
AXIS = {
    "x": 0,
    "y": 1,
    "z": 2
}


def gather_and_format_input_files(
        outdir,
        dwis,
        bvals,
        bvecs,
        b0_magnitude=None,
        b0_phase=None):
    """ Gather all files needed to start the preprocessing in the right format
    (Gis format for images and B0 maps).

    Parameters
    ----------
    outdir: str
        path to directory where to gather all files.
    dwis: str
        path to input Nifti files to be preprocessed.
    bvals: str
        path to .bval files associated to Nifti.
    bvecs: str
        path to .bvec files associated to Nifti.
    b0_magnitude: str (optional, default None)
        path to B0 magnitude map, may also contain phase.
        Required only if you want to make fieldmap-based
        correction of susceptibility distortions.
    b0_phase: str (optional, default None)
        not required if phase is already contained in
        b0_magnitude or if you don't want to make fieldmap-based
        correction of susceptibility distortions.

    Returns
    -------
    raw_dwi_dir:
        Connectomist's import data directory with files in Gis format.
    """
    # Check that files exist
    files = dwis + bvals + bvecs
    if b0_magnitude is not None:
        files.append(b0_magnitude)
    if b0_phase is not None:
        files.append(b0_phase)
    for path in files:
        if not os.path.isfile(path):
            raise ConnectomistBadFileError(path)

    # Create the directory if not existing
    if not os.path.isdir(outdir):
        os.mkdir(outdir)

    # If there is only one b0 map file and if this file contains 2 volumes,
    # split it in 2 files: magnitude and phase, assuming the first one is
    # magnitude
    if b0_magnitude and not b0_phase:
        b0_maps = nibabel.load(b0_magnitude)
        if b0_maps.shape[-1] == 2:
            voxels = b0_maps.get_data()
            header = b0_maps.get_header()
            affine = b0_maps.get_affine()
            magnitude = nibabel.Nifti1Image(voxels[..., 0], affine, header)
            phase = nibabel.Nifti1Image(voxels[..., 1], affine, header)
            b0_magnitude = os.path.join(outdir, "b0_magnitude.nii.gz")
            b0_phase = os.path.join(outdir, "b0_phase.nii.gz")
            magnitude.to_filename(b0_magnitude)
            phase.to_filename(b0_phase)

    # Go through all DWI data that must be converted
    copied_dwis = []
    copied_bvals = []
    copied_bvecs = []
    nb_of_sequences = len(dwis)
    for index, (dwi, bval, bvec) in enumerate(zip(dwis, bvals, bvecs)):

        # One sequence name special case
        if nb_of_sequences == 1:
            index = ""

        # Convert Nifti to Gis
        copied_dwis.append(ptk_nifti_to_gis(
            dwi, os.path.join(outdir, "dwi{0}.ima".format(index))))

        # Copy bval and bvec files, with homogeneous names
        bval_copy = os.path.join(outdir, "dwi{0}.bval".format(index))
        bvec_copy = os.path.join(outdir, "dwi{0}.bvec".format(index))
        shutil.copyfile(bval, bval_copy)
        shutil.copyfile(bvec, bvec_copy)
        copied_bvals.append(bval_copy)
        copied_bvecs.append(bvec_copy)

    # Convert and rename B0 map(s) if they are given
    if b0_magnitude is not None:
        b0_magnitude = ptk_nifti_to_gis(
            b0_magnitude, os.path.join(outdir, "b0_magnitude.ima"))

    if b0_phase is not None:
        b0_phase = ptk_nifti_to_gis(
            b0_phase, os.path.join(outdir, "b0_phase.ima"))

    return copied_dwis, copied_bvals, copied_bvecs, b0_magnitude, b0_phase


def data_import_and_qspace_sampling(
        outdir,
        subject_id,
        dwis,
        bvals,
        bvecs,
        manufacturer,
        flipX=False,
        flipY=False,
        flipZ=False,
        invertX=True,
        invertY=False,
        invertZ=False,
        b0_magnitude=None,
        b0_phase=None,
        phase_axis="y",
        slice_axis="z",
        path_connectomist=DEFAULT_CONNECTOMIST_PATH):
    """ Wrapper to Connectomist's 'DWI & Q-space' tab.

    Parameters
    ----------
    outdir: str
        path to Connectomist's output directory.
    subject_id: str
        the subject code in study.
    dwis: list of str
        path to Nifti diffusion-weighted datasets.
    bvals: list of str
        path to .bval files associated to the Nifti.
    bvecs: list of str
        path to .bvec files associated to the Nifti.
    manufacturer: str
        name of the manufacturer (e.g. "Siemens", "GE", "Philips" or "Bruker").
    flipX, flipY, flipZ: bool (optional, default False)
        if True invert the x, y or z-axis of data.
    invertX: bool (optional, default True)
        if True invert x-axis of diffusion model.
    invertY, invertZ: bool (optional, default False)
        if True invert y or z-axis of diffusion model.
    b0_magnitude: str (optional, default None)
        path to the magnitude fieldmap (if fieldmap-based correction of
        susceptibility distortions is to be used).
    b0_phase: str (optional, default None)
        path to phase fieldmap (if fieldmap-based correction of susceptibility
        distortions is to be used).
    phase_axis: str (optional, default 'y')
        the acquistion phase axis 'x', 'y' or 'z'.
    slice_axis: str (optional, default 'z')
        the acquistion slice axis 'x', 'y' or 'z'.
    path_connectomist: str (optional)
        path to the Connectomist executable.

    Returns
    -------
    outdir: str
        path to Connectomist's output directory.
    """
    # Check input parameters
    for axis in (phase_axis, slice_axis):
        if axis not in AXIS:
            raise ValueError("Invalid axis '{0}'.".format(axis))
    if len(set(map(len, (dwis, bvecs, bvals)))) != 1:
        raise ValueError("The DWIs, BVECs and BVALs must have the same number "
                         "of elements.")

    # Create the Connectomist's import data directory
    dwis, bvals, bvecs, b0_magnitude, b0_phase = gather_and_format_input_files(
        outdir,
        dwis,
        bvals,
        bvecs,
        b0_magnitude,
        b0_phase)

    # Dict with all parameters for connectomist
    algorithm = "DWI-Data-Import-And-QSpace-Sampling"
    parameters_dict = {
        # Parameters are ordered as they appear in connectomist's GUI

        # ---------------------------------------------------------------------
        # Field: "Diffusion weighted-images"
        "fileNameDwi":  ";".join(dwis),  # "DW data"
        "sliceAxis":    AXIS[slice_axis],  # "Slice axis", default "Z-axis"
        "phaseAxis":    AXIS[phase_axis],  # "Phase axis", default "Y-axis"
        "manufacturer": None,

        # Subfield: "Advanced parameters"
        "flipAlongX":           2 if flipX else 0,  # "Flip data along x"
        "flipAlongY":           2 if flipY else 0,
        "flipAlongZ":           2 if flipZ else 0,
        "numberOfDiscarded":    0,  # "#discarded images at beginning"
        "numberOfT2":        None,  # "#T2"
        "numberOfRepetitions":  1,  # "#repetitions"
        # ---------------------------------------------------------------------
        # Field: "Rotation of field of view", default is identity matrix
        "qSpaceTransform_xx": 1.0,
        "qSpaceTransform_xy": 0.0,
        "qSpaceTransform_xz": 0.0,
        "qSpaceTransform_yx": 0.0,
        "qSpaceTransform_yy": 1.0,
        "qSpaceTransform_yz": 0.0,
        "qSpaceTransform_zx": 0.0,
        "qSpaceTransform_zy": 0.0,
        "qSpaceTransform_zz": 1.0,
        # ---------------------------------------------------------------------
        # Field: "Q-space sampling"
        "qSpaceSamplingType": 4,  # default "spherical single-shell custom"
        "qSpaceChoice5BValueFileNames": ";".join(bvals),
        "qSpaceChoice5BValueThreshold": 50,
        "qSpaceChoice5OrientationFileNames": ";".join(bvecs),

        # Apparently Connectomist uses 2 as True, and 0 as False.
        "invertXAxis": 2 if invertX else 0,
        "invertYAxis": 2 if invertY else 0,
        "invertZAxis": 2 if invertZ else 0,

        # In this field but not used/handled parameters
        "qSpaceChoice1MaximumBValue":       1000,  # case Cartesian
        "qSpaceChoice2BValue":              1000,
        "qSpaceChoice3BValue":              1000,
        "qSpaceChoice4BValue":              1000,
        "qSpaceChoice6BValues":               "",
        "qSpaceChoice7BValues":               "",
        "qSpaceChoice8BValues":               "",
        "qSpaceChoice9BValues":               "",
        "qSpaceChoice10BValues":              "",
        "qSpaceChoice11BValues":              "",
        "qSpaceChoice1NumberOfSteps":         11,
        "qSpaceChoice2NumberOfOrientations":   6,
        "qSpaceChoice3NumberOfOrientations":   6,
        "qSpaceChoice4NumberOfOrientations":   6,
        "qSpaceChoice6NumberOfOrientations":   6,
        "qSpaceChoice7NumberOfOrientations":   6,
        "qSpaceChoice8NumberOfOrientations":   6,
        "qSpaceChoice10NumberOfOrientations": "",
        "qSpaceChoice11NumberOfOrientations": "",
        "qSpaceChoice13OrientationFileNames": "",
        # ---------------------------------------------------------------------
        # Field: micro structure config"
        "gradientCharacteristicsFileNames": "",
        # ---------------------------------------------------------------------
        # Field: "Work directory"
        "outputWorkDirectory": outdir,
        # ---------------------------------------------------------------------
        # unknown parameter
        "_subjectName": subject_id,
    }

    # Map the manufacturer name with Connectomist convention
    if manufacturer not in MANUFACTURERS:
        raise ConnectomistBadManufacturerNameError(manufacturer)
    parameters_dict["manufacturer"] = MANUFACTURERS[manufacturer]

    # Read bvals and bvecs
    bvalues, bvectors, nb_shells, nb_nodiff = read_bvals_bvecs(bvals, bvecs)

    # Update Connectomist step description
    parameters_dict["numberOfT2"] = nb_nodiff
    if nb_shells == 1:
        # Spherical single-shell custom
        parameters_dict["qSpaceSamplingType"] = 4
    else:
        warnings.warn(
            "'{0}' shell model(s) not handled yet.".format(nb_shells))
        # Arbitrary shell
        parameters_dict["qSpaceSamplingType"] = 12
        parameters_dict["qSpaceChoice13BValueFileNames"] = ";".join(bvals)
        parameters_dict["qSpaceChoice13BValueThreshold"] = 50.0
        parameters_dict["qSpaceChoice13OrientationFileNames"] = ";".join(bvecs)

    # Call with Connectomist
    process = ConnectomistWrapper(path_connectomist)
    parameter_file = ConnectomistWrapper.create_parameter_file(
        algorithm, parameters_dict, outdir)
    process(algorithm, parameter_file, outdir)

    # When there are multiple volume or when there are multiple t2 (nodif)
    # volumes, Connectomist merges them
    # rewrite bvec, bval file accordingly (remove extra T2 values)
    if nb_nodiff > 1:
        bval = os.path.join(outdir, "dwi.bval")
        dw_indexes = np.where(bvalues >= 100)[0]
        new_bvals = np.concatenate(([0], bvalues[dw_indexes]))
        np.savetxt(bval, new_bvals)
        bvec = os.path.join(outdir, "dwi.bvec")
        new_bvecs = np.concatenate(
            ([[0], [0], [0]], bvectors.T[:, dw_indexes]), axis=1)
        np.savetxt(bvec, new_bvecs)

    return outdir
