import numpy as np
import tkinter.filedialog
import copy, sys
import tqdm
import ctpros as ct


def imgchecker(imgs, transformfiles):
    """
    Checks that the referenced images in all given transformations is
    provided.

    Assumes default naming convention:
    IMG:
        [*]FILENAME.*
        or
        FILENAME.*

    Transform:
        [*]FILE1-FILE2.tfm
        or
        FILE1-FILE2.tfm
        or
        FILE1.tfm

    """
    indexmatrix = indexfileinfo(imgs, transformfiles)
    unpairedtransform = np.nonzero(np.sum(indexmatrix != -1, 1) < 2)[0]
    overpairedtransform = np.nonzero(np.sum(indexmatrix != -1, 0) > 3)[0]

    return unpairedtransform.size == 0 or overpairedtransform.size < 2


def indexfileinfo(imgs, transformfiles):
    """
    Generates img and transform relationship index matrix.

    """
    imgnames = [myimg.filename for myimg in imgs]
    tnames = [
        gen.methods.sys_splitfullfilename(transformfile)[-2]
        for transformfile in transformfiles
    ]
    indexmatrix = np.array(
        [[tname.find(imgname) for imgname in imgnames] for tname in tnames]
    )

    return indexmatrix


def reorienter(imgs, transformfiles):
    """
    Re-orients transformations to set all images to be (1) relative to the
    frame of the unmatched transformation matrix OR (2) relative to an
    average orientation of all of the matches transformations.

    Ex:
        Given:
            Img1-Img2.tfm
            Img2-Img3.tfm
        Yields: Imgs1-3 are oriented to the average orientation of all of
        the images.

        Given:
            Img1.tfm
            Img1-Img2.tfm
            Img2-Img3.tfm
        Yields: Imgs1-3 are oriented to the orientation set by Img1.tfm.

        Given:
            Img1-Img2.tfm
            Img2.tfm
            Img2-Img3.tfm
        Yields: Imgs1-3 are oriented to the orientation set by Img2.tfm
    """
    transforms = [
        gen.Orientation(3).read(fullfilename=tname) for tname in transformfiles
    ]

    indexmatrix = indexfileinfo(imgs, transformfiles).astype(np.single)
    indexmatrix[indexmatrix == -1] = np.nan
    indexmatrix[np.arange(indexmatrix.shape[0]), np.nanargmin(indexmatrix, 1)] = 1
    indexmatrix[np.arange(indexmatrix.shape[0]), np.nanargmax(indexmatrix, 1)] = 2

    spareind = np.nonzero(np.sum(np.logical_not(np.isnan(indexmatrix)), 1) == 1)[0]
    if spareind.size == 0:
        spareinfo = None
    else:
        spareinfo = indexmatrix[spareind[0]]
        sparetransform = transforms[spareind[0]]
        transforms.pop(spareind[0])
        indexmatrix = np.delete(indexmatrix, spareind, axis=0)

    # combine transforms to be relative to last timepoint
    for i, row in enumerate(indexmatrix):
        minind = np.nanargmin(row)
        maxind = np.nanargmax(row)
        if minind > maxind:
            row[[minind, maxind]] = row[[maxind, minind]]
            transforms[i] = transforms[i].inv()
    for j, col in enumerate(indexmatrix.transpose()[:-1]):
        start = np.nonzero(col == 1)[0][0]
        end = np.nonzero(col == 2)[0]
        for ind in end:
            col[ind] = np.nan
            indexmatrix[ind, np.nonzero(indexmatrix[start] == 2)[0][0]] = 2
            transforms[ind].update(transforms[start])

    # define order of transforms
    transforminds = []
    for col in indexmatrix.transpose()[:-1]:
        transforminds.append(np.nonzero(col == 1)[0][0])
    transforms = [transforms[i] for i in transforminds]
    transforms.append(gen.Orientation(3))

    # change relativity of transforms to spare or otherwise average
    if spareinfo is None:
        avgorientation = gen.Orientation(imgs[0].ndim).average(*transforms)

        for img, transform in zip(imgs, transforms):
            transform.update(avgorientation.inv())
            img.orientation.update(transform)

    else:
        relind = np.nonzero(spareinfo == 2)[0][0]
        reltransform = transforms[relind].inv().update(sparetransform)

        for img, transform in zip(imgs, transforms):
            transform.update(reltransform)
            img.orientation.update(transform)

    return None


def calc_bounds(*imgs):
    """
    Calculates the physical bounds of the images at their orientation.

    """

    boundpoints = np.array(
        [
            [
                myimg.orientation.orient(array)
                for array in np.flip(
                    gen.methods.np_cubevertices(myimg.header["dim"])[0]
                )
            ]
            for myimg in imgs
        ]
    ).reshape((-1, 3))

    minbounds = np.min(boundpoints, axis=0)
    maxbounds = np.max(boundpoints, axis=0)

    return minbounds, maxbounds


def resampler(imgs, resolution=None, verbose=True):
    """
    Resamples the images within their physical bounds with a given image resolution.

    """
    minbounds, maxbounds = calc_bounds(*imgs)
    translation = -np.floor(minbounds)
    maxbounds += translation
    [myimg.orientation.update("translating", translation) for myimg in imgs]

    if resolution is None:
        resolution = np.flip(imgs[0].header["elsize"])
    elif not issubclass(np.ndarray, type(resolution)):
        resolution = np.array([resolution, resolution, resolution])
    stitchedsize = np.ceil(maxbounds / resolution).astype(np.int)

    stitchedimg = img.NDImg(imgs[0], shape=stitchedsize, dtype=np.single)
    stitchedimg[:] = 0
    coeffimg = img.NDImg(imgs[0], shape=stitchedsize, dtype=np.half)
    coeffimg[:] = 0

    samplespace = copy.deepcopy(maxbounds)
    samplespace[0] = resolution[0]
    step = np.array([resolution[0], 0, 0])
    for myimg in imgs:
        myimg.load(verbose=verbose)
        mymin, mymax = calc_bounds(myimg)
        myrange = range(
            int(np.floor(mymin[0] / resolution[0])),
            int(np.ceil(mymax[0] / resolution[0])),
        )
        myones = img.NDImg(myimg, shape=myimg.shape, dtype=np.single)
        myones[:] = 1.0

        def run(i):
            coeffimg[i] += myones.transform_affine(
                affine=gen.Orientation(3).update("translating", -step * i),
                ndspace=samplespace,
                elsizes=resolution,
                interpolation="linear",
                outofbounds="constant",
            )[0]

            stitchedimg[i] += myimg.transform_affine(
                affine=gen.Orientation(3).update("translating", -step * i),
                ndspace=samplespace,
                elsizes=resolution,
                interpolation="linear",
                outofbounds="constant",
            )[0]

        if verbose:
            for i in tqdm.tqdm(myrange, ascii=True, desc=myimg.filename):
                run(i)
        else:
            for i in myrange:
                run(i)

        myimg.orientation.update("translating", step * stitchedimg.shape[0])
        myimg.resize(0, refcheck=False)

    stitchedimg[coeffimg > 1] /= coeffimg[coeffimg > 1]
    stitchedimg = img.AIM(np.round(stitchedimg).astype(np.int16), view=True)
    return stitchedimg
    #     def sampleimg(i):
    #         stitchedimg[i]+=myimg.transform_affine(
    #             affine=gen.Orientation(3).update("translating",-step*i),
    #             ndspace=samplespace,
    #             elsizes=resolution,
    #             interpolation="linear",
    #             outofbounds="constant",)[0]
    #     if verbose:
    #         for i in tqdm.tqdm(myrange, ascii=True, desc=myimg.filename):
    #             sampleimg(i)
    #     else:
    #         for i in myrange:
    #             sampleimg(i)

    #     myimg.orientation.update("translating",step*stitchedimg.shape[0])
    #     myimg.resize(0,refcheck=False)

    # coeffimg = img.NDImg(ndimg=imgs[0],shape=stitchedimg[i].shape,dtype=np.single)
    # myones =
    # def normalizeimg(i):
    #     coeffimg[:] = 0
    #     for myimg in imgs:
    #         myones =
    #         coeffimg+=myones.transform_affine(
    #             affine=gen.Orientation(3).update("translating",-step*i),
    #             ndspace=samplespace,
    #             elsizes=resolution,
    #             interpolation="linear",
    #             outofbounds="constant",)[0]

    # if verbose:
    #     for i in tqdm.tqdm(myrange,ascii=True,desc="Normalizing"):
    #         normalizeimg(i)
    # else:
    #     for i in myrange:
    #         normalizeimg(i)

    # stitchedimg[coeffimg > 1] /= coeffimg[coeffimg > 1]
    # stitchedimg = stitchedimg.astype(np.int16)
    # return stitchedimg


def stitcher(imgfiles=None, transformfiles=None):
    """
    Stitches a set of images

    """
    if imgfiles is None or transformfiles is None:
        return None

    imgs = [img.NDImg(imgfile).read() for imgfile in imgfiles]
    datachecked = imgchecker(imgs, transformfiles)
    if not datachecked:
        print("Not enough information. Missing or redundant .AIM or .tfm files.")
        return None

    reorienter(imgs, transformfiles)
    stitchedimg = resampler(imgs)

    newfilename = (
        imgs[0].filelocation + imgs[0].filename + "_STITCHED" + imgs[0].fileext
    )
    stitchedimg.save(filename=newfilename, verbose=True)
    return None


def main(*argv):
    imgfiles = gen.methods.sys_fileselector(
        "AIM*", title="Select the images to be stitched."
    )
    transformfiles = gen.methods.sys_fileselector(
        "tfm", title="Select the transforms to be used."
    )
    stitcher(imgfiles=imgfiles, transformfiles=transformfiles)


if __name__ == "__main__":
    main(*sys.argv)
