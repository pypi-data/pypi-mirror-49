#! /usr/bin/env python

"""
Module with frame px resampling/rescaling functions.
"""
__author__ = 'Carlos Alberto Gomez Gonzalez, V. Christiaens, R. Farkas'
__all__ = ['frame_px_resampling',
           'cube_px_resampling',
           'cube_rescaling_wavelengths',
           'check_scal_vector']

import numpy as np
import warnings
try:
    import cv2
    no_opencv = False
except ImportError:
    warnings.warn("Opencv python bindings are missing.", ImportWarning)
    no_opencv = True

from scipy.ndimage.interpolation import geometric_transform, zoom
from ..var import frame_center, get_square
from .subsampling import cube_collapse


def cube_px_resampling(array, scale, imlib='ndimage', interpolation='bicubic',
                       verbose=True):
    """
    Resample the frames of a cube with a single scale factor.

    Wrapper of ``frame_px_resampling``. Useful when we need to upsample
    (upscaling) or downsample (pixel binning) a set of frames, e.g. an ADI cube.

    Parameters
    ----------
    array : 3d numpy ndarray
        Input cube, 3d array.
    scale : int, float or tuple
        Scale factor for upsampling or downsampling the frames in the cube. If
        a tuple it corresponds to the scale along x and y.
    imlib : str, optional
        See the documentation of the ``vip_hci.preproc.frame_px_resampling``
        function.
    interpolation : str, optional
        See the documentation of the ``vip_hci.preproc.frame_px_resampling``
        function.
    verbose : bool, optional
        Whether to print out additional info such as the new cube shape.

    Returns
    -------
    array_resc : numpy ndarray
        Output cube with resampled frames.

    """
    if array.ndim != 3:
        raise TypeError('Input array is not a cube or 3d array.')

    array_resc = []
    for i in range(array.shape[0]):
        imresc = frame_px_resampling(array[i], scale=scale, imlib=imlib,
                                     interpolation=interpolation)
        array_resc.append(imresc)

    array_resc = np.array(array_resc)

    if verbose:
        print("Cube successfully rescaled")
        print("New shape: {}".format(array_resc.shape))
    return array_resc


def frame_px_resampling(array, scale, imlib='ndimage', interpolation='bicubic',
                        verbose=False):
    """
    Resample the pixels of a frame wrt to the center, changing the frame size.

    If ``scale`` < 1 then the frame is downsampled and if ``scale`` > 1 then its
    pixels are upsampled.

    Parameters
    ----------
    array : numpy ndarray
        Input frame, 2d array.
    scale : int, float or tuple
        Scale factor for upsampling or downsampling the frame. If a tuple it
        corresponds to the scale along x and y.
    imlib : {'ndimage', 'opencv'}, optional
        Library used for image transformations.
    interpolation : str, optional
        For 'ndimage' library: 'nearneig', bilinear', 'bicuadratic', 'bicubic',
        'biquartic', 'biquintic'. The 'nearneig' interpolation is the fastest
        and the 'biquintic' the slowest. The 'nearneig' is the worst
        option for interpolation of noisy astronomical images.
        For 'opencv' library: 'nearneig', 'bilinear', 'bicubic', 'lanczos4'.
        The 'nearneig' interpolation is the fastest and the 'lanczos4' the
        slowest and accurate.
    verbose : bool, optional
        Whether to print out additional info such as the new image shape.

    Returns
    -------
    array_resc : numpy ndarray
        Output resampled frame.

    """
    if array.ndim != 2:
        raise TypeError('Input array is not a frame or 2d array')

    if isinstance(scale, tuple):
        scale_x, scale_y = scale
    elif isinstance(scale, (float, int)):
        scale_x = scale
        scale_y = scale
    else:
        raise TypeError('`scale` must be float, int or tuple')

    if imlib == 'ndimage':
        if interpolation == 'nearneig':
            order = 0
        elif interpolation == 'bilinear':
            order = 1
        elif interpolation == 'bicuadratic':
            order = 2
        elif interpolation == 'bicubic':
            order = 3
        elif interpolation == 'biquartic':
            order = 4
        elif interpolation == 'biquintic':
            order = 5
        else:
            raise TypeError('Scipy.ndimage interpolation method not recognized')

        array_resc = zoom(array, zoom=(scale_y, scale_x), order=order)

    elif imlib == 'opencv':
        if no_opencv:
            msg = 'Opencv python bindings cannot be imported. Install opencv or'
            msg += ' set imlib to ndimage'
            raise RuntimeError(msg)

        if interpolation == 'bilinear':
            intp = cv2.INTER_LINEAR
        elif interpolation == 'bicubic':
            intp = cv2.INTER_CUBIC
        elif interpolation == 'nearneig':
            intp = cv2.INTER_NEAREST
        elif interpolation == 'lanczos4':
            intp = cv2.INTER_LANCZOS4
        else:
            raise TypeError('Opencv interpolation method not recognized')

        array_resc = cv2.resize(array.astype(np.float32), (0, 0), fx=scale_x,
                                fy=scale_y, interpolation=intp)

    else:
        raise ValueError('Image transformation library not recognized')

    array_resc /= scale_y * scale_x

    if verbose:
        print("Image successfully rescaled")
        print("New shape: {}".format(array_resc.shape))

    return array_resc


def cube_rescaling_wavelengths(cube, scal_list, full_output=True, inverse=False,
                               y_in=None, x_in=None, imlib='opencv',
                               interpolation='lanczos4', collapse='median',
                               pad_mode='reflect'):
    """
    Scale/Descale a cube by scal_list, with padding.

    Wrapper to scale or descale a cube by factors given in scal_list,
    without any loss of information (zero-padding if scaling > 1).
    Important: in case of IFS data, the scaling factors in scal_list should be
    >= 1 (ie. provide the scaling factors as for scaling to the longest
    wavelength channel).

    Parameters
    ----------
    cube: 3D-array
       Data cube with frames to be rescaled.
    scal_list: 1D-array
       Vector of same dimension as the first dimension of datacube, containing
       the scaling factor for each frame.
    full_output: bool, optional
       Whether to output just the rescaled cube (False) or also its median,
       the new y and x shapes of the cube, and the new centers cy and cx of the
       frames (True).
    inverse: bool, optional
       Whether to inverse the scaling factors in scal_list before applying them
       or not; i.e. True is to descale the cube (typically after a first scaling
       has already been done)
    y_in, x_in: int
       Initial y and x sizes, required for ``inverse=True``. In case the cube is
       descaled, these values will be used to crop back the cubes/frames to
       their original size.
    imlib : {'opencv', 'ndimage'}, str optional
        Library used for image transformations. Opencv is faster than ndimage or
        skimage.
    interpolation : str, optional
        For 'ndimage' library: 'nearneig', bilinear', 'bicuadratic', 'bicubic',
        'biquartic', 'biquintic'. The 'nearneig' interpolation is the fastest
        and the 'biquintic' the slowest. The 'nearneig' is the poorer
        option for interpolation of noisy astronomical images.
        For 'opencv' library: 'nearneig', 'bilinear', 'bicubic', 'lanczos4'.
        The 'nearneig' interpolation is the fastest and the 'lanczos4' the
        slowest and accurate. 'lanczos4' is the default.
    collapse : {'median', 'mean', 'sum', 'trimmean'}, str optional
        Sets the way of collapsing the frames for producing a final image.
    pad_mode : str, optional
        One of the following string values:

            ``'constant'``
                pads with a constant value
            ``'edge'``
                pads with the edge values of array
            ``'linear_ramp'``
                pads with the linear ramp between end_value and the array edge
                value.
            ``'maximum'``
                pads with the maximum value of all or part of the vector along
                each axis
            ``'mean'``
                pads with the mean value of all or part of the vector along each
                axis
            ``'median'``
                pads with the median value of all or part of the vector along
                each axis
            ``'minimum'``
                pads with the minimum value of all or part of the vector along
                each axis
            ``'reflect'``
                pads with the reflection of the vector mirrored on the first and
                last values of the vector along each axis
            ``'symmetric'``
                pads with the reflection of the vector mirrored along the edge
                of the array
            ``'wrap'``
                pads with the wrap of the vector along the axis. The first
                values are used to pad the end and the end values are used to
                pad the beginning

    Returns
    -------
    frame: 2d array
        The median of the rescaled cube.
    cube : 3d array
        [full_output] rescaled cube
    frame : 2d array
        [full_output] median of the rescaled cube
    y,x,cy,cx : float
        [full_output] New y and x shapes of the cube, and the new centers cy and
        cx of the frames

    """
    n, y, x = cube.shape

    max_sc = np.amax(scal_list)

    if not inverse and max_sc > 1:
        new_y = int(np.ceil(max_sc * y))
        new_x = int(np.ceil(max_sc * x))
        if (new_y - y) % 2 != 0:
            new_y += 1
        if (new_x - x) % 2 != 0:
            new_x += 1
        pad_len_y = (new_y - y) // 2
        pad_len_x = (new_x - x) // 2
        pad_width = ((0, 0), (pad_len_y, pad_len_y), (pad_len_x, pad_len_x))
        big_cube = np.pad(cube, pad_width, pad_mode)
    else:
        big_cube = cube.copy()

    n, y, x = big_cube.shape
    cy, cx = frame_center(big_cube[0])

    if inverse:
        scal_list = 1. / scal_list
        cy, cx = frame_center(cube[0])

    # (de)scale the cube, so that a planet would now move radially
    cube = _cube_resc_wave(big_cube, scal_list, ref_xy=(cx, cy),
                           imlib=imlib, interpolation=interpolation)
    frame = cube_collapse(cube, collapse)

    if inverse and max_sc > 1:
        if y_in is None or x_in is None:
            raise ValueError("You need to provide y_in and x_in when "
                             "inverse=True!")
        siz = max(y_in, x_in)
        if frame.shape[0] > siz:
            frame = get_square(frame, siz, cy, cx)
        if full_output:
            n_z = cube.shape[0]
            array_old = cube.copy()
            cube = np.zeros([n_z, siz, siz])
            for zz in range(n_z):
                cube[zz] = get_square(array_old[zz], siz, cy, cx)

    if full_output:
        return cube, frame, y, x, cy, cx
    else:
        return frame


def _cube_resc_wave(array, scaling_list, ref_xy=None, imlib='opencv',
                    interpolation='lanczos4', scaling_y=None, scaling_x=None):
    """
    Rescale a cube by factors from ``scaling_list`` wrt a position.

    Parameters
    ----------
    array : numpy ndarray
        Input 3d array, cube.
    scaling_list : 1D-array
        Scale corresponding to each frame in the cube.
    ref_xy : float, optional
        Coordinates X,Y of the point with respect to which the rescaling will be
        performed. By default the rescaling is done with respect to the center
        of the frames; central pixel if the frames have odd size.
    imlib : str optional
        See the documentation of ``vip_hci.preproc.cube_rescaling_wavelengths``.
    interpolation : str, optional
        See the documentation of ``vip_hci.preproc.cube_rescaling_wavelengths``.
    scaling_y : 1D-array or list
        Scaling factor only for y axis. If provided, it takes priority on
        scaling_list.
    scaling_x : 1D-array or list
        Scaling factor only for x axis. If provided, it takes priority on
        scaling_list.

    Returns
    -------
    array_sc : numpy ndarray
        Resulting cube with rescaled frames.

    """
    def _scale_func(output_coords, ref_xy=0, scaling=1.0, scale_y=None,
                    scale_x=None):
        """
        For each coordinate point in a new scaled image (output_coords),
        coordinates in the image before the scaling are returned. This scaling
        function is used within geometric_transform which, for each point in the
        output image, will compute the (spline) interpolated value at the
        corresponding frame coordinates before the scaling.
        """
        ref_x, ref_y = ref_xy
        if scale_y is None:
            scale_y = scaling
        if scale_x is None:
            scale_x = scaling
        return (ref_y + (output_coords[0] - ref_y) / scale_y,
                ref_x + (output_coords[1] - ref_x) / scale_x)

    def _frame_rescaling(array, ref_xy=None, scale=1.0, imlib='opencv',
                         interpolation='lanczos4', scale_y=None, scale_x=None):
        """
        Rescale a frame by a factor wrt a reference point.

        The reference point is by default the center of the frame (typically the
        exact location of the star). However, it keeps the same dimensions.

        Parameters
        ----------
        array : numpy ndarray
            Input frame, 2d array.
        ref_xy : float, optional
            Coordinates X,Y  of the point wrt which the rescaling will be
            applied. By default the rescaling is done with respect to the center
            of the frame.
        scale : float
            Scaling factor. If > 1, it will upsample the input array equally
            along y and x by this factor.
        scale_y : float
            Scaling factor only for y axis. If provided, it takes priority on
            scale parameter.
        scale_x : float
            Scaling factor only for x axis. If provided, it takes priority on
            scale parameter.

        Returns
        -------
        array_out : numpy ndarray
            Resulting frame.

        """
        if array.ndim != 2:
            raise TypeError('Input array is not a frame or 2d array.')

        if scale_y is None:
            scale_y = scale
        if scale_x is None:
            scale_x = scale

        outshape = array.shape
        if ref_xy is None:
            ref_xy = frame_center(array)

        if imlib == 'ndimage':
            if interpolation == 'nearneig':
                order = 0
            elif interpolation == 'bilinear':
                order = 1
            elif interpolation == 'bicuadratic':
                order = 2
            elif interpolation == 'bicubic':
                order = 3
            elif interpolation == 'biquartic':
                order = 4
            elif interpolation == 'biquintic':
                order = 5
            else:
                raise TypeError(
                    'Scipy.ndimage interpolation method not recognized')

            array_out = geometric_transform(array, _scale_func, order=order,
                                            output_shape=outshape,
                                            extra_keywords={'ref_xy': ref_xy,
                                                            'scaling': scale,
                                                            'scale_y': scale_y,
                                                            'scale_x': scale_x})

        elif imlib == 'opencv':
            if no_opencv:
                msg = 'Opencv python bindings cannot be imported. Install '
                msg += ' opencv or set imlib to skimage'
                raise RuntimeError(msg)

            if interpolation == 'bilinear':
                intp = cv2.INTER_LINEAR
            elif interpolation == 'bicubic':
                intp = cv2.INTER_CUBIC
            elif interpolation == 'nearneig':
                intp = cv2.INTER_NEAREST
            elif interpolation == 'lanczos4':
                intp = cv2.INTER_LANCZOS4
            else:
                raise TypeError('Opencv interpolation method not recognized')

            M = np.array([[scale_x, 0, (1. - scale_x) * ref_xy[0]],
                          [0, scale_y, (1. - scale_y) * ref_xy[1]]])
            array_out = cv2.warpAffine(array.astype(np.float32), M, outshape,
                                       flags=intp)

        else:
            raise ValueError('Image transformation library not recognized')

        array_out /= scale_y * scale_x
        return array_out

    ############################################################################
    if array.ndim != 3:
        raise TypeError('Input array is not a cube or 3d array')

    array_sc = []
    for i in range(array.shape[0]):
        array_sc.append(_frame_rescaling(array[i], ref_xy=ref_xy,
                                         scale=scaling_list[i], imlib=imlib,
                                         interpolation=interpolation,
                                         scale_y=scaling_y, scale_x=scaling_x))
    return np.array(array_sc)


def check_scal_vector(scal_vec):
    """
    Turn wavelengths (IFS data) into a scaling factor list.

    It checks that it has the right format: all scaling factors should be >= 1
    (i.e. the scaling should be done wrt the longest wavelength of the cube).

    Parameters
    ----------
    scal_vec: 1d array or list
        Vector with the wavelengths.

    Returns
    -------
    scal_vec: numpy ndarray, 1d
        Vector containing the scaling factors (after correction to comply with
        the condition >= 1).

    """
    if not isinstance(scal_vec, (list, np.ndarray)):
        raise TypeError('`Scal_vec` is neither a list or an np.ndarray')

    scal_vec = np.array(scal_vec)

    # checking if min factor is 1:
    if scal_vec.min() != 1:
        scal_vec = 1 / scal_vec
        scal_vec /= scal_vec.min()

    return scal_vec


def _find_indices_sdi(wl, dist, index_ref, fwhm, delta_sep=1, nframes=None,
                      debug=False):
    """
    Find optimal wavelengths which minimize self-subtraction in model PSF
    subtraction.

    Parameters
    ----------
    wl : numpy ndarray or list
        Vector with the scaling factors.
    dist : float
        Separation or distance (in pixels) from the center of the array.
    index_ref : int
        The `wl` index for which we are finding the pairs.
    fwhm : float
        Mean FWHM of all the wavelengths (in pixels).
    delta_sep : float, optional
        The threshold separation in terms of the mean FWHM.
    nframes : None or int, optional
        Must be an even value. In not None, then between 2 and adjacent
        ``nframes`` are kept.
    debug : bool, optional
        It True it prints out debug information.

    Returns
    -------
    indices : numpy ndarray
        List of good indices.

    """
    wl = np.asarray(wl)
    wl_ref = wl[index_ref]
    sep_lft = (wl_ref - wl) / wl_ref * ((dist + fwhm * delta_sep) / fwhm)
    sep_rgt = (wl - wl_ref) / wl_ref * ((dist - fwhm * delta_sep) / fwhm)
    map_lft = sep_lft >= delta_sep
    map_rgt = sep_rgt >= delta_sep
    indices = np.nonzero(map_lft | map_rgt)[0]

    if debug:
        print("dist: {}, index_ref: {}".format(dist, index_ref))
        print("sep_lft:", "  ".join(["{:+.2f}".format(x) for x in sep_lft]))
        print("sep_rgt:", "  ".join(["{:+.2f}".format(x) for x in sep_rgt]))
        print("indices:", indices)
        print("indices size: {}".format(indices.size))

    if indices.size == 0:
        raise RuntimeError("No frames left after radial motion threshold. Try "
                           "decreasing the value of `delta_sep`")

    if nframes is not None:
        i1 = map_lft.sum()
        window = nframes // 2
        if i1 - window < 0 or i1 + window > indices[-1]:
            window = nframes
        ind1 = max(0, i1 - window)
        ind2 = min(wl.size, i1 + window)
        indices = indices[ind1: ind2]

        if indices.size < 2:
            raise RuntimeError("No frames left after radial motion threshold. "
                               "Try decreasing the value of `delta_sep` or "
                               "`nframes`")

    if debug:
        print("indices (nframes):", indices)

    return indices
