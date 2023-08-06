"""The file contains the SPmerge02_final function
"""

import sys
import warnings
from multiprocessing import Pool, cpu_count, shared_memory

import numpy as np

def SPmerge02_final(sm, scanOrStep, **kwargs):
    """Final alignment

    Parameters
    ----------
    sm : sMerge object
        the sMerge object contains all the data.
    scanOrStep : ndarray
        step size in refinement, in pixels.
    densityCutoff : float, optional
        density cutoff for image boundaries (norm. to 1). Default to 0.8.
    pixelsMovedThreshold : float, optional
        if number of pixels shifted (per image) is below this value,
        refinement will be halted. Default to 0.1.
    stepSizeReduce : float, optional
        when a scanline origin does not move, step size will be reduced by
        this factor. Default to 0.5.
    flagPointOrder : bool, optional
        use this flag to force origins to be ordered, i.e. disallow points
        from changing their order. Default to True.
    parallel : bool, optional
        whether to parallelise the alignment for scan lines.
        The default is True in Linux system, else False.

    Returns
    -------
    stopRefine : bool
        specifies whether furthere refinement is needed or not.

    Raises
    ------
    ValueError
        if there is a shape mismatch of scanOrStep.
    """

    # ignore unknown input arguments
    _args_list = ['densityCutoff', 'pixelsMovedThreshold', 'stepSizeReduce',
                  'flagPointOrder', 'parallel']
    for key in kwargs.keys():
        if key not in _args_list:
            msg = "The argument '{}' is not recognised, and it is ignored."
            warnings.warn(msg.format(key), RuntimeWarning)

    scanOrStep = np.asarray(scanOrStep)
    if (scanOrStep.shape[0] != sm.numImages) or (scanOrStep.shape[1] != sm.nr):
        msg = ('The shape of scanOrstep {} does not match the number of '
               'image ({}) or the number of origins ({}).')
        raise ValueError(msg.format(scanOrStep.shape, sm.numImages, sm.nr))

    # for final alignment
    densityCutoff = kwargs.get('densityCutoff', 0.8)
    pixelsMovedThreshold = kwargs.get('pixelsMovedThreshold', 0.1)
    stepSizeReduce = kwargs.get('stepSizeReduce', 1/2)
    flagPointOrder = kwargs.get('flagPointOrder', True)
    parallel = kwargs.get('parallel', True if 'linux' in sys.platform else False)

    # Reset pixels moved count
    pixelsMoved = 0

    # Refine each image in turn, against the sum of all other images
    for k in range(sm.numImages):
        # get alignment image for the current image
        imageAlign = _get_reference_image(sm, k, densityCutoff)
        imgAgn_sz = imageAlign.shape
        imageAlign = imageAlign.ravel()

        if parallel:
            # set shared memory, used by different processes
            Z = _set_shm_instance(sm, scanOrStep, imageAlign)
            shm_scanOr = Z[0]
            shm_scanLines = Z[1]
            shm_scanOrStep = Z[2]
            shm_scanDir = Z[3]
            shm_imageAlign = Z[4]

            # the tasks include all scanline in the current image
            tasks = []
            for m in range(sm.nr):
                tasks.append([k, m, sm.nr, sm.nc, sm.numImages, sm.imageSize,
                              imgAgn_sz, flagPointOrder, shm_scanOr,
                              shm_scanLines, shm_scanOrStep, shm_scanDir,
                              shm_imageAlign,
                              ])

            pixelsMoved = _parallel_align(tasks, sm, scanOrStep, stepSizeReduce,
                                          pixelsMoved)

            # clean up the shared memory blocks
            shm_scanOr.close()
            shm_scanLines.close()
            shm_scanOrStep.close()
            shm_scanDir.close()
            shm_imageAlign.close()
            shm_scanOr.unlink()
            shm_scanLines.unlink()
            shm_scanOrStep.unlink()
            shm_scanDir.unlink()
            shm_imageAlign.unlink()
        else:
            dxy = np.array([[0,1,-1,0,0], [0,0,0,1,-1]])
            # If ordering is used as a condition, determine parametric positions
            if flagPointOrder:
                # Use vector perpendicular to scan direction (negative 90 deg)
                nn = np.array([sm.scanDir[k, 1], -sm.scanDir[k, 0]])
                vParam = nn[0]*sm.scanOr[k, 0, :] + nn[1]*sm.scanOr[k, 1, :]
            else:
                nn = None
                vParam = None

            # perform serial alignmment
            pixelsMoved = _serial_align(sm, scanOrStep, k, flagPointOrder,
                                        dxy, nn, vParam, imageAlign,
                                        imgAgn_sz, stepSizeReduce, pixelsMoved)

    # If pixels moved is below threshold, halt refinement
    if (pixelsMoved/sm.numImages) < pixelsMovedThreshold:
        stopRefine = True
    else:
        stopRefine = False

    return stopRefine

def _set_shm_instance(sm, scanOrStep, imageAlign):
    """set shared memory block for different arrays that used by all processes
    """

    # scanOr
    shm_scanOr = shared_memory.SharedMemory(create=True,
                                            size=sm.scanOr.nbytes)
    tmp = np.ndarray(sm.scanOr.shape, dtype=sm.scanOr.dtype,
                     buffer=shm_scanOr.buf)
    tmp[:] = sm.scanOr[:]

    # scanLines
    shm_scanLines = shared_memory.SharedMemory(create=True,
                                               size=sm.scanLines.nbytes)
    tmp = np.ndarray(sm.scanLines.shape, dtype=sm.scanLines.dtype,
                     buffer=shm_scanLines.buf)
    tmp[:] = sm.scanLines[:]

    # scanOrStep
    shm_scanOrStep = shared_memory.SharedMemory(create=True,
                                                size=scanOrStep.nbytes)
    tmp = np.ndarray(scanOrStep.shape, dtype=scanOrStep.dtype,
                     buffer=shm_scanOrStep.buf)
    tmp[:] = scanOrStep[:]

    # scanDir
    shm_scanDir = shared_memory.SharedMemory(create=True,
                                             size=sm.scanDir.nbytes)
    tmp = np.ndarray(sm.scanDir.shape, dtype=sm.scanDir.dtype,
                     buffer=shm_scanDir.buf)
    tmp[:] = sm.scanDir[:]

    # imageAlign
    shm_imageAlign = shared_memory.SharedMemory(create=True,
                                                size=imageAlign.nbytes)
    tmp = np.ndarray(imageAlign.shape, dtype=imageAlign.dtype,
                     buffer=shm_imageAlign.buf)
    tmp[:] = imageAlign[:]

    return (shm_scanOr, shm_scanLines, shm_scanOrStep, shm_scanDir,
            shm_imageAlign)

def _do_align(task):
    """perform alginment for a specific scan m in image k
    """

    # unpack variables in the provided order
    k = task[0]
    m = task[1]
    nr = task[2]
    nc = task[3]
    numImage = task[4]
    imageSize = task[5]
    imgAgn_sz = task[6]
    flagPointOrder = task[7]
    shm_scanOr = task[8]
    shm_scanLines = task[9]
    shm_scanOrStep = task[10]
    shm_scanDir = task[11]
    shm_imageAlign = task[12]

    # create numpy array from the shared memory blocks
    scanOr = np.ndarray((numImage, 2, nr), dtype=float, buffer=shm_scanOr.buf)
    scanLines = np.ndarray((numImage, nr, nc), dtype=float,
                           buffer=shm_scanLines.buf)
    scanOrStep = np.ndarray((numImage, nr), dtype=float,
                            buffer=shm_scanOrStep.buf)
    scanDir = np.ndarray((numImage, 2), dtype=float, buffer=shm_scanDir.buf)
    imageAlign = np.ndarray((imgAgn_sz[0]*imgAgn_sz[1],), dtype=float,
                            buffer=shm_imageAlign.buf)

    dxy = np.array([[0,1,-1,0,0], [0,0,0,1,-1]])
    # If ordering is used as a condition, determine parametric positions
    if flagPointOrder:
        # Use vector perpendicular to scan direction (negative 90 deg)
        nn = np.array([scanDir[k, 1], -scanDir[k, 0]])
        vParam = nn[0]*scanOr[k, 0, :] + nn[1]*scanOr[k, 1, :]
    else:
        nn = None
        vParam = None

    # Refine score by moving the origin (by dxy*step) of this scanline
    # If required, force ordering of points
    origin = scanOr[k, :, m]
    step = scanOrStep[k, m]
    orTest = _origin_ordering(nr, origin, m, dxy, step, nn, vParam,
                              flagPointOrder)

    # Loop through the test origins
    # score each of them against the reference image (imageAlign)
    raw_scanline = scanLines[k, m, :]
    ind, norigin = _test_origins(nc, scanDir, imageSize, orTest, k,
                                 dxy, imageAlign,
                                 imgAgn_sz, raw_scanline)

    return ind, norigin, k, m

def _parallel_align(tasks, sm, scanOrStep, stepSizeReduce, pixelsMoved):
    """parallelise the alignment of each scan lines by creating workers
    """

    chsz = sm.nr // cpu_count() + 1
    with Pool(cpu_count()) as pool:
        for ret in pool.imap_unordered(_do_align, tasks, chunksize=chsz):
            ind, norigin, k, m = ret

            # record the pixel shift
            pixelsMoved = _move_origin(sm, k, m, scanOrStep, stepSizeReduce,
                                       ind, norigin, pixelsMoved)

    return pixelsMoved

def _serial_align(sm, scanOrStep, k, flagPointOrder, dxy, nn, vParam,
                  imageAlign, imgAgn_sz, stepSizeReduce, pixelsMoved):
    """serial alginment of each scan lines
    """

    # Loop through each scanline and perform alignment
    for m in range(sm.nr):
        # Refine score by moving the origin (by dxy*step) of this scanline
        # If required, force ordering of points
        origin = sm.scanOr[k, :, m]
        step = scanOrStep[k, m]
        orTest = _origin_ordering(sm.nr, origin, m, dxy, step, nn, vParam,
                                  flagPointOrder)

        # Loop through the test origins
        # score each of them against the reference image (imageAlign)
        raw_scanline = sm.scanLines[k, m, :]
        ind, norigin = _test_origins(sm.nc, sm.scanDir, sm.imageSize, orTest,
                                     k, dxy, imageAlign, imgAgn_sz,
                                     raw_scanline)

        # record the pixel shift
        pixelsMoved = _move_origin(sm, k, m, scanOrStep, stepSizeReduce,
                                   ind, norigin, pixelsMoved)

    return pixelsMoved

def _get_reference_image(sm, k, densityCutoff):
    """Generate alignment image, mean of all other scanline datasets,
    unless user has specified a reference image.
    """

    if sm.imageRef is None:
        indsAlign = np.arange(sm.numImages, dtype=int)
        indsAlign = indsAlign[indsAlign != k]

        dens_cut = sm.imageDensity[indsAlign, ...] > densityCutoff
        imageAlign = (sm.imageTransform[indsAlign, ...] * dens_cut).sum(axis=0)
        dens = dens_cut.sum(axis=0)
        sub = dens > 0
        imageAlign[sub] = imageAlign[sub] / dens[sub]
        imageAlign[~sub] = np.mean(imageAlign[sub])
    else:
        imageAlign = sm.imageRef

    return imageAlign

def _origin_ordering(nr, origin, IndOr, dxy, step, nn, vParam, flagPointOrder):
    """Get the moved origin from dxy and step, order them if required
    """

    if flagPointOrder:
        moved_origin = origin[:, None] + dxy*step
        vTest = nn[0]*moved_origin[0, :] + nn[1]*moved_origin[1, :]

        if IndOr == 0:
            # no lower bound?
            vBound = np.array([-np.inf, vParam[1]])
        elif IndOr == nr-1:
            # no upper bound?
            vBound = np.array([vParam[IndOr-1], np.inf])
        else:
            vBound = np.array([vParam[IndOr-1], vParam[IndOr+1]])

        # order origins
        for p in range(dxy.shape[1]):
            if vTest[p] < vBound[0]:
                moved_origin[:, p] += nn*(vBound[0]-vTest[p])
            elif vTest[p] > vBound[1]:
                moved_origin[:, p] += nn*(vBound[1]-vTest[p])
    else:
        moved_origin = origin[:, None] + dxy*step

    return moved_origin

def _test_origins(nc, scanDir, imageSize, orTest, k, dxy, imageAlign,
                  imgAgn_sz, raw_scanline):
    """Loop through the test origins, score each of them against the
    reference image (imageAlign)

    ind is the index of the lowest score, norigin is the selected test origin
    """

    score = np.zeros(dxy.shape[1])
    for p in range(dxy.shape[1]):
        torigin = orTest[:, p]
        score[p] = _get_test_origin_score(nc, scanDir, imageSize, imageAlign,
                                          imgAgn_sz, torigin, k, raw_scanline)

    # Note that if moving origin does not change score, dxy = (0,0)
    # will be selected (ind = 0).
    ind = np.argmin(score)
    norigin = orTest[:, ind]

    return ind, norigin

def _move_origin(sm, k, m, scanOrStep, stepSizeReduce, ind, norigin,
                 pixelsMoved):
    """Move the origin by norigin, record the pixel shift, accumulative,
    reduce the steps of origin moved if the origin is not moved
    """

    if ind == 0:
        # Reduce the step size for this origin
        scanOrStep[k, m] *= stepSizeReduce
    else:
        pshift = np.linalg.norm(norigin - sm.scanOr[k, :, m])
        pixelsMoved += pshift
        sm.scanOr[k, :, m] = norigin

    return pixelsMoved

def _get_test_origin_score(nc, scanDir, imageSize, imageRef, imgRef_sz,
                           torigin, IndImg, scanline):
    """Get interpolated scanline from moved origins and compare its with
    raw scanline for scoring
    """

    xInd, yInd = torigin

    t = np.arange(1, nc+1)
    xInd = xInd + t*scanDir[IndImg, 0]
    yInd = yInd + t*scanDir[IndImg, 1]

    # Prevent pixels from leaving image boundaries
    xInd = np.core.umath.clip(xInd, 0, imageSize[0]-2).ravel()
    yInd = np.core.umath.clip(yInd, 0, imageSize[1]-2).ravel()

    # Bilinear coordinates
    xF = np.floor(xInd).astype(int)
    yF = np.floor(yInd).astype(int)
    dx = xInd - xF
    dy = yInd - yF

    # score for the p test origin for this scanline
    score = _calcScore(imageRef, imgRef_sz, xF, yF, dx, dy, scanline)

    return score

def _calcScore(image_ravel, imgsz, xF, yF, dx, dy, intMeas):
    """Calculate score between a reference and interpolated line
    """

    # same as ravel_multi_index but quicker, why?
    rind1 = yF + xF*imgsz[-1]
    rind2 = yF + (xF+1)*imgsz[-1]
    rind3 = (yF+1) + xF*imgsz[-1]
    rind4 = (yF+1) + (xF+1)*imgsz[-1]

    dx1 = 1 - dx
    dy1 = 1 - dy
    imageSample = image_ravel[rind1]*dx1*dy1 + image_ravel[rind2]*dx*dy1 +\
                  image_ravel[rind3]*dx1*dy + image_ravel[rind4]*dx*dy

    score = np.abs(imageSample - intMeas).sum()

    return score
