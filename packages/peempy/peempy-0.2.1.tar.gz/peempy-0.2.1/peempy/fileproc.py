"""
Module for file processing
"""

import os
import logging
from multiprocessing import cpu_count
from multiprocessing.pool import Pool
from threadpoolctl import threadpool_limits

import skimage.io as io
import numpy as np

import peempy.imageproc as imageproc
from .utils import mkdir, normalize_uint8, compute_edge
from peempy.imageproc import load_image_set, XMCDImageSeries, xmcd4_from_stack, ImageSeries
import warnings

logger = logging.getLogger(__name__)
pjoin = os.path.join


# Base directory
def get_normalisation(fdname, save=False):
    """
    Get normalisation data
    Try to use the file with name but if fails just us
    """
    name = 'norm.tif'
    fname = str(fdname / name)
    if os.path.isfile(fname):
        data = io.imread(fname)
    else:
        logger.warn('Using all images in {}'.format(fdname.name))
        data = load_image_set(str(fdname))
        data = data.mean(axis=0)
        if save:
            io.imsave(fname, data.astype(np.float32))
    return data


class FolderProcesser:
    """Class for processing folders"""

    DATASUFFIX = "PCOImage"  # Suffix for data/save folders
    SAVESUFFIX = "UViewImage"
    SAVE_DTYPE = np.float32
    DRIFT_MODE = 'one-pass'

    def __init__(self, fids, norm_img, peempath, mask_ratio=0.93):
        self.fids = fids
        self.norm_img = norm_img
        self.mask_ratio = mask_ratio
        self.crop_setting = None
        self._no_warn = True
        self.alt_savedir = None
        self.save_drifted = True
        self.save_edge = None
        self.save_xmcd = False
        self.nprocs = None
        self.nthreads = None
        self.drift_sigma = None
        self.review_first_frame = False
        self.ppath = peempath

    def get_save_folder(self, fid):
        return pjoin(self.ppath.driftdir, "{}_{}".format(fid, self.SAVESUFFIX))

    def get_data_folder(self, fid):
        dfolder = pjoin(self.ppath.basedir,
                        "{}_{}".format(fid, self.DATASUFFIX))
        return dfolder

    def warning_off(self):
        """Turn off warnings"""
        self._no_warn = True

    def adjust_crop(self):
        """Adjust crop region by reading first and last images from all folders"""
        fdnames = [self.get_data_folder(fid) for fid in self.fids]
        frame_tmp = []
        frame_names = []
        logger.info("Reading data from folders")
        for folder in fdnames:
            tifs = [fn for fn in os.listdir(folder)
                    if ".tif" in fn]  # list of tifs
            tifs.sort()
            frame_tmp.append(io.imread(os.path.join(folder, tifs[0])))
            frame_tmp.append(io.imread(os.path.join(folder, tifs[-1])))
            frame_names.append(os.path.split(folder)[1] + '_first')
            frame_names.append(os.path.split(folder)[1] + '_last')
            logger.info("{} image files found "
                        "in folder {}".format(len(tifs),
                                              os.path.split(folder)[1]))
        im_tmp = ImageSeries(frame_tmp)
        # Not sure why -> This is taken from the Igor routine
        im_tmp.frames -= 100
        im_tmp.normalise(self.norm_img)
        im_tmp.apply_circle_mask(self.mask_ratio, 0)

        # Adjust crop
        crop_ok = False
        while crop_ok is False:
            im_tmp.manual_crop(frame_names=frame_names)
            #im_tmp.update_crop()
            im_tmp.view_drift_region(frame_names=frame_names)
            respond = input("Is the feature in region?(y/n)\n")
            print(respond)
            crop_ok = respond.lower() == "y"
        logger.info("Cropping region accepted")
        self.crop_setting = im_tmp.crop_setting
        del im_tmp

    def correct_and_save(self, fid, review=False):
        """Process a single folder.
        Parameters
        ----------

        fid: int
            index of the folder to be processed

        review: bool
            Review the result if True is passed

        Wether saving drift corrected frames and XMCD images is defined
        by self.save_drift and self.save_xmcd
        """

        # Turn off warnings if desired
        if self._no_warn is True:
            import warnings
            warnings.filterwarnings("ignore")

        logger.info("Processing folder {}".format(fid))

        with threadpool_limits(self.nthreads):
            data = load_image_set(self.get_data_folder(fid))
            ims = XMCDImageSeries(data)

            # Substrate the backgroup away
            ims.substract_counts(100)

            # Normalise using the normlisation image
            ims.normalise(self.norm_img)
            ims.apply_circle_mask(self.mask_ratio, 0)

            # Set region for drift correction
            ims.crop_setting = self.crop_setting

            # Do drift correction
            ims.drift_correct(mode=self.DRIFT_MODE, sigma=self.drift_sigma)

            # import IPython; IPython.embed()
            if review is True:
                logger.info("Please review the drift correction")
                print("Showing pre-drift image")
                ims.res_dc.view_cropped(ignore_drift=True)
                print("Showing drift-corrected image")
                ims.res_dc.view_cropped(use_corrected=True)
                print("Showing pre-drift image")
                ims.off_dc.view_cropped(ignore_drift=True)
                print("Showing drift-corrected image")
                ims.off_dc.view_cropped(use_corrected=True)

            if self.save_drifted is True:
                savefolder = self.get_save_folder(fid)
                logger.info("Saving results in folder: {}".format(savefolder))
                mkdir(self.ppath.driftdir)
                # Check if the folder for saving this set exists
                mkdir(savefolder)

                # Construct the mapping to the original order
                for i, frame in zip(ims.orig_index, ims.corrected_frames):
                    # Check if the master save folder exists
                    fname = "pco_{:05d}.tif".format(i + 1)
                    fname = os.path.join(savefolder, fname)
                    io.imsave(fname, frame.astype(np.uint16))

            if self.save_xmcd is True:
                # Check if the master save folder exists
                xmcddir = self.ppath.xmcddir
                mkdir(xmcddir)
                logger.info('Saving XMCD results for {}'.format(fid))
                # Save I and D images
                D, I, _ = xmcd4_from_stack(ims.corrected_frames)
                io.imsave(pjoin(xmcddir, "I_{}.tif".format(fid)),
                          I.astype(self.SAVE_DTYPE))
                io.imsave(pjoin(xmcddir, "D_{}.tif".format(fid)),
                          D.astype(self.SAVE_DTYPE))

                # Save I and D previews
                preview_dir = xmcddir.parent / (xmcddir.name + '_preview')
                mkdir(preview_dir)
                I_preview = normalize_uint8(I)
                D_preview = normalize_uint8(D)
                io.imsave(pjoin(preview_dir, "I_{}.png".format(fid)),
                          I_preview)
                io.imsave(pjoin(preview_dir, "D_{}.png".format(fid)),
                          D_preview)

                # SAVE EDGE_XAS image to check the alignment
                # A more memory efficient routine should be written for this
                if self.save_edge is True:
                    io.imsave(
                        pjoin(preview_dir, "RES_EDGE_{}.png".format(fid)),
                        normalize_uint8(compute_edge(ims.res_imgs_corr)))
                    io.imsave(
                        pjoin(preview_dir, "OFFRES_EDGE_{}.png".format(fid)),
                        normalize_uint8(compute_edge(ims.offres_imgs_corr)))

            if self._no_warn is True:
                warnings.resetwarnings()

            # Delete the frame to saving memory
            ims._clear_data()

    def process_all(self):
        """
        Start batch option to process all folders specified

        This method will process the first image and review the outcome.
        Then rest sets will be processed either in parallel or in series.
        """
        from tqdm import tqdm

        # Correct the first image
        logger.info("Processing the first image")
        self.correct_and_save(self.fids[0], review=self.review_first_frame)
        rest = self.fids[1:]
        if self.nprocs < 1:

            cpus = cpu_count()
            procs = int(cpus / 2)
        else:
            procs = self.nprocs

        if len(rest) > 1 and procs > 1:
            # Disable logging
            imageproc.set_logging(logging.WARNING)
            p = Pool(procs)
            print("Drifting {} images in {} way parallel".format(
                len(rest), procs))

            for _ in tqdm(p.imap_unordered(self.correct_and_save, rest),
                          total=len(rest)):
                pass
        elif len(rest) > 0:
            print("Drifting {} images in series".format(len(rest)))
            for i in tqdm(rest):
                self.correct_and_save(i)

        print("Processing finished")


class XMCDAlign(object):
    """Align XMCD images"""
    I_PREFIX = 'I'
    D_PREFIX = 'D'
    DRIFT_MODE = 'one-pass'
    SAVE_DTYPE = np.float32

    def __init__(self, fids, peempath):
        """Initialise the instance"""
        self.fids = fids
        self.actual_fnames = []
        self.ppath = peempath

        self.iseries = None
        self.dseries = None

    def load_images(self):
        """Load the images"""
        xdir = self.ppath.xmcddir
        i_frames = []
        d_frames = []
        for fid in self.fids:
            frames = []
            for prefix in [self.I_PREFIX, self.D_PREFIX]:
                imag_path = xdir.glob("{}_{}.tif*".format(prefix, fid))
                imag_path = list(imag_path)
                if len(imag_path) > 1:
                    raise RuntimeError(
                        'Expect 1 files, found: {}'.format(imag_path))
                elif len(imag_path) == 0:
                    warnings.warn('File not find for {}'.format(fid))
                    continue
                imag_path = imag_path[0]
                if 'I' in imag_path.name:
                    self.actual_fnames.append(imag_path.name)
                frames.append(io.imread(str(imag_path.resolve())))
            if frames:
                i_frames.append(frames[0])
                d_frames.append(frames[1])

        self.iseries = ImageSeries(i_frames)
        self.dseries = ImageSeries(d_frames)

    def select_region(self, vmax=5):
        # Adjust crop
        crop_ok = False
        while crop_ok is False:
            self.iseries.manual_crop(vmin=0,
                                     vmax=vmax,
                                     frame_names=self.actual_fnames)
            #im_tmp.update_crop()
            # View the region and select, use a fixed range
            self.iseries.view_drift_region(vmin=0,
                                           vmax=vmax,
                                           frame_names=self.actual_fnames)
            respond = input("Is the feature in region?(y/n)\n")
            print(respond)
            crop_ok = respond.lower() == "y"
        logger.info("Cropping region accepted")
        self.crop_setting = self.iseries.crop_setting

    def correct_and_save(self, threshold=None):
        """Do correction and save"""

        # Carry out drift correction
        self.iseries.drift_correct(mode=self.DRIFT_MODE, sigma=None)
        # Apply the drifts to the d series
        self.dseries.apply_drift(self.iseries.drifts)

        # Get the save directory, create if needed
        savefolder = self.ppath.xmcdavgdir
        savefolder.mkdir(exist_ok=True)

        idmin = min(self.fids)
        idmax = max(self.fids)
        dname = '{}_{}-{}.tif'.format(self.D_PREFIX, idmin, idmax)
        iname = '{}_{}-{}.tif'.format(self.I_PREFIX, idmin, idmax)

        i_average = self.iseries.corrected_frames.mean(axis=0).astype(
            self.SAVE_DTYPE)
        d_average = self.dseries.corrected_frames.mean(axis=0).astype(
            self.SAVE_DTYPE)

        if threshold:
            mask = np.all(self.iseries.corrected_frames < threshold, axis=0)
            d_average[mask] = 0

        # Save the date
        io.imsave(str(savefolder / iname),
                  i_average,
                  metadata={'averaged_from': self.actual_fnames})
        io.imsave(str(savefolder / dname),
                  d_average,
                  metadata={'averaged_from': self.actual_fnames})

        # Save the previews
        i_preview = normalize_uint8(i_average)
        d_preview = normalize_uint8(d_average)
        preview_dir = savefolder.parent / (savefolder.name + '_preview')
        preview_dir.mkdir(exist_ok=True)
        io.imsave(str(preview_dir / dname.replace('tif', 'png')), d_preview)
        io.imsave(str(preview_dir / iname.replace('tif', 'png')), i_preview)
        io.imsave(str(preview_dir / ("EDGE_" + iname.replace('tif', 'png'))),
                  normalize_uint8(compute_edge(self.iseries.corrected_frames)))
