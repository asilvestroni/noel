# ----------------------------
#  Andrea Silvestroni 2019
#  Residual Noise Extraction and Smartphone Linking
#
# ----------------------------

import os

import numpy as np
from django.db import models

from . import PictureCluster, Session


class Picture(models.Model):
    """
    Model representing a picture on the system. It may come from different sources (e.g. Facebook, smartphone, ...) and
    belongs to a Session.
    The typical lifecycle of a Picture is the following:
        - Created on the system (either after being uploaded from a smartphone or by being fetched from a SN)
        - Preprocessed by calling the `preprocess()` method on the instance
        - Extracted by caling the `extract()` method on the instance. This produces a Residual Noise file
        - Clustered based on its extracted Residual Noise
    """
    # TODO: consider leveraging django's file managing instead of direct path access to files
    # TODO: consider allowing the user to identify pictures through the front end (e.g. detect badly clustered pictures,
    #  declaring a trusted picture for clustering, ...)

    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, default='original')
    status = models.CharField(max_length=40, blank=True, null=True, default='waiting to be processed')
    cluster = models.ForeignKey(PictureCluster, blank=True, null=True, default=None, on_delete=models.SET_NULL)
    ext = models.CharField(max_length=10, default='.jpg')

    # Computed properties
    @property
    def base_path(self) -> str:
        """
        :return: Base path of the picture (session directory, type and id)
        """
        return "{}/{}/{}".format(self.session.session_dir, self.type, self.id)

    @property
    def pic_path(self) -> str:
        """
        :return: Path to the original picture file
        """
        return "{}/{}/{}{}".format(self.session.session_dir, self.type, self.id, self.ext)

    @property
    def thumb_path(self) -> str:
        """
        :return: Path to the picture's thumbnail
        """
        return "{}-thumb{}".format(self.base_path, self.ext)

    @property
    def prep_path(self) -> str:
        """
        :return: Path to the picture's preprocessed version
        """
        return "{}/{}/preps/{}.mat".format(self.session.session_dir, self.type, self.id)

    @property
    def mat_noise_path(self) -> str:
        """
        :return: Path to the picture's noise .mat file
        """
        return "{}/{}/noises/{}.mat".format(self.session.session_dir, self.type, self.id)

    @property
    def noise_path(self):
        """
        :return: Path to the picture's noise .npy file
        """
        return "{}/{}/noises/{}.npy".format(self.session.session_dir, self.type, self.id)

    def delete(self, using=None, keep_parents=False):
        """
        Deletes a Picture instance and all of its related files.
        :param using:
        :param keep_parents:
        """
        import contextlib

        with contextlib.suppress(FileNotFoundError):
            os.remove(self.mat_noise_path)
            os.remove(self.noise_path)
            os.remove(self.prep_path)
            os.remove(self.pic_path)
            os.remove(self.thumb_path)
        super().delete(using, keep_parents)

    def preprocessed(self) -> bool:
        """
        Preprocesses the picture or returns its preprocessed version if it was already computed.
        Preprocessing consists of:
            - Conversion to grayscale
            - Rotation of landscape pictures (width > height) to portrait
            - Saving as .mat file for the extraction script

        :return: A boolean value indicating if the picture was valid or not (e.g. too small to be processed)
        """
        from PIL import Image
        from scipy.io import savemat
        from main.logic.common import const

        prep_path = self.prep_path

        if not os.path.isfile(prep_path):
            with Image.open(self.pic_path) as img:
                self.update_and_log_status(const.status_preprocessing)
                width, height = img.size

                # If picture size is smaller than the minimum one specified set the picture as invalid
                if width < const.sizes['width'] or height < const.sizes['height']:
                    self.update_and_log_status(const.status_invalid_size)
                    return False

                # Keep only Y channel
                img = img.convert('L')

                # Rotate landscape pictures
                if width > height:
                    img = img.transpose(Image.ROTATE_270)

                # Save preprocessed picture
                prep = np.array(img)
                savemat(prep_path, {"pic": prep})

                # Update status
                self.update_and_log_status(const.status_preprocessed)
                return True
        else:
            return True

    def extract(self):
        """
        Extracts residual noise from the picture or returns its already computed one.
        Calls an external script called 'run_BM3D.sh' which requires Matlab Runtime to be executed.
        Source code for the executable is found under the `matlab_bm3d directory`, which can be used to compile an
        executable for a different target system, but requires Matlab Compiler to do so
        """
        from PIL import Image
        from subprocess import Popen
        from subprocess import PIPE
        from scipy.io import loadmat
        from main.logic.common import const

        # Acquire paths of preprocessed picture and matlab noise
        prep_path = self.prep_path
        mat_noise_path = self.mat_noise_path

        # If noise was not extracted before, do it
        if not os.path.isfile(mat_noise_path):
            self.update_and_log_status(const.status_extracting)

            # Call the external script (BM3D_DIRECTORY will be added to the environment
            # since it's a child process)
            subproc = Popen('$BM3D_DIRECTORY/application/run_BM3D.sh $BM3D_DIRECTORY/v95 "{}" "{}"'
                            .format(prep_path,
                                    mat_noise_path),
                            shell=True,
                            stdout=open(os.devnull, 'wb'), stderr=PIPE)
            subproc.wait()

            # Load the .mat version of the noise and resize it, then save it aas .npy
            residual_noise = loadmat(mat_noise_path)['rn']
            noise = np.array(Image.fromarray(residual_noise).resize((1024, 1024), Image.BICUBIC))

            # TODO: leverage Django's file managing to store and access the noise file
            np.save(self.noise_path, noise)
            self.update_and_log_status(const.status_extracted)

    def update_and_log_status(self, new_status: str):
        """
        Updates session status and prints it on the console.

        :param new_status: The new status to be set.
        """
        self.status = new_status
        self.save()
        print("[{}]: {}".format(self.id, new_status))
