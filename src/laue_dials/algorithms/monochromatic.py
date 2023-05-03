"""
This file contains functions for monochromatic processing
"""
import reciprocalspaceship as rs
import gemmi
import numpy as np
from cctbx.sgtbx import space_group
from cctbx.uctbx import unit_cell
from dials.array_family import flex
from dxtbx.model import ExperimentList
from tqdm import trange


def import_images(args=None, *, phil):
    """
    Read a set of images into an ExperimentList object

    Parameters
    ----------
    args : string
        File name(s) for image files. Can include wildcards to represent several files

    phil : libtbx.phil.scope
        A phil scope containing the parameters for the DIALS import code

    Returns
    -------
    expts : ExperimentList
        An ExperimentList with information from headers in image files
    """
    from dials.command_line.dials_import import do_import

    expts = do_import(args, phil=phil)
    return expts


def find_spots(phil, expts):
    """
    Find strong reflections on images given a set of experiments

    Parameters
    ----------
    phil : libtbx.phil.scope
        A phil scope containing the parameters for the DIALS spotfinding code

    Returns
    -------
    refls : reflection_table
        A reflection table containing the found strong reflections
    """
    from dials.command_line.find_spots import do_spotfinding

    refls = do_spotfinding(expts, phil, configure_logging=True)
    return refls


def initial_index(params, expts, refls):
    """
    Indexes a dataset at a single wavelength using FFT3D

    Parameters
    ----------
    phil : libtbx.phil.scope_extract
        A phil scope extract containing the parameters for the DIALS indexing code

    Returns
    -------
    expts_indexed : ExperimentList
        An ExperimentList containing the indexing solution geometry
    refls_indexed : reflection_table
        A reflection table containing reflections with indexing data
    """
    from dials.command_line.index import index

    expts_indexed, refls_indexed = index(expts, [refls], params)
    return expts_indexed, refls_indexed


def scan_varying_refine(params, expts, refls):
    """
    Performs scan-varying geometric refinement over a sequence of images

    Parameters
    ----------
    params : phil
        A phil scope containing the needed input for dials.refine

    Returns
    -------
    expts_refined : ExperimentList
        An ExperimentList containing the refined geometric solution
    refls_refined : reflection_table
        A reflection table containing reflections with refined data
    """
    from dials.command_line.refine import run_dials_refine

    expts_refined, refls_refined, _, _ = run_dials_refine(expts, refls, params)
    return expts_refined, refls_refined


def split_sequence(params, expts, refls):
    """
    Splits a sequence of images into stills

    Parameters
    ----------
    params : phil
        A phil scope containing the needed input for dials.sequence_to_stills

    Returns
    -------
    expts_stills : ExperimentList
        An ExperimentList containing stills of the input dataset
    refls_stills : reflection_table
        A reflection table containing stills of the input dataset
    """
    return expts_stills, refls_stills
