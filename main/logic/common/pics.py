# ----------------------------
#  Andrea Silvestroni 2019
#  Residual Noise Extraction and Smartphone Linking
#
#  Provides functions used by the session processing task, in order to make it more readable and easy to understand
# ----------------------------

from typing import List
from time import sleep
from celery import group, shared_task

import numpy as np
from celery.result import allow_join_result, GroupResult
from django.db.models.query import QuerySet

from main.logic.common import thumbnail_sizes
from main.models import Picture, Session, PictureCluster
from .funcs import timeit

from os import path
from PIL import Image
from urllib import request, error


def download_pic(pic: Picture, url: str) -> bool:
    """
    Downloads a picture from the provided url and associates it to the provided model

    :param pic: Picture model to associate the downloaded file with
    :param url: Url from which the picture is being downwloaded
    :return: True if the file was successfully downloaded, False otherwise.
    """
    pic_path = pic.pic_path
    thumb_path = pic.thumb_path

    if path.isfile(pic_path):
        return True

    while True:

        try:
            # Download and store image
            # TODO: consider using django file managing tools (and serving it separately)
            req = request.urlopen(url, timeout=10)
            with open(pic_path, 'wb') as f:
                f.write(req.read())
            print("Saving " + pic_path)

            # Create thumbnail
            with Image.open(pic_path) as i:
                # TODO: leverage Django's file managing for access and storage of the thumbnails
                i.thumbnail(thumbnail_sizes, Image.ANTIALIAS)
                i.save(thumb_path)
                print("Saving " + thumb_path)

            return True
        except error.URLError:
            print("Could not download " + url)
        except Exception as e:
            print(e)
            return False


def generate_thumbnails(ses: Session, type: str = 'original'):
    """
    Generates thumbnails for all the pictures of the specified type that belong to the provided session

    :param ses: Session to which pictures belong
    :param type: The type of pictures for which thumbnails are being generated
    """
    pics: QuerySet = Picture.objects.filter(session=ses, type=type)

    # Needed to document the type
    pic: Picture
    for pic in pics:
        # TODO: leverage Django's file managing for access and storage of the thumbnails
        with Image.open(pic.pic_path) as i:
            i.thumbnail(thumbnail_sizes, Image.ANTIALIAS)
            i.save(pic.thumb_path)


@timeit
def pics_preprocess(pics: QuerySet) -> List[Picture]:
    """
    Preprocess all the pics contained in the QuerySet, and return a list of preprocessed pictures.
    Preprocessing simply consists in calling the `preprocessed()` method on each picture instance, and checking if the
    picture was valid or not: if it was, it is added to the result

    :param pics: Pics that need to be preprocessed
    :return: A list of preprocessed pictures that were found to be valid
    """
    valid_pics = []

    pic: Picture
    for pic in pics:
        if pic.preprocessed():
            valid_pics.append(pic)

    return valid_pics


@timeit
def pics_residual_noise(ses: Session, type: str = "original"):
    """
    Preprocesses all the pictures of the specified type that belong to the provided session, and then extracts the
    residual noise from each of them. This is achieved by launching a separate task for each picture, which is then
    processed by a Celery worker. Waits for all children tasks to be completed before returning.

    :param ses: Session to which pictures belong
    :param type: The type of pictures for which thumbnails are being generated
    """
    pics = Picture.objects.filter(session=ses, type=type)

    # Preprocess the provided pictures
    preprocessed = pics_preprocess(pics)

    # Generate a list of children task to be launched
    tasks = []
    for pic in preprocessed:
        tasks.append(extract_from_pic.s(pic.id, type))

    # Call all the children tasks and wait for them to return
    result: GroupResult
    result = group(tasks).apply_async()
    with allow_join_result():
        while not result.completed_count() == len(pics):
            sleep(5)


@shared_task
def extract_from_pic(pic_id: int, type: str):
    """
    Task that extracts residual noise from a picture

    :param pic_id: Id of the picture
    """
    from main.logic.common import const

    pic = Picture.objects.get(id=pic_id)
    pic.extract()

    total = pic.session.picture_set.exclude(status=const.status_invalid_size).filter(type=pic.type).count()

    pic.session.update_and_log_status(type, 1/total)


@timeit
def cluster_pattern_noise(cluster: PictureCluster) -> np.ndarray:
    """
    Computes Pattern Noise for a PictureCluster by averaging pictures' Residual Noises.

    :param cluster: PictureCluster for which the Pattern Noise is being computed
    :return: The computed Pattern Noise
    """
    from main.logic.common.const import sizes
    cluster_pics = cluster.picture_set
    rns = np.array([np.load(p.noise_path).flatten() for p in cluster_pics.all()])

    pn = rns.mean(axis=0)
    pn = pn.reshape(sizes['height'], sizes['width'])

    # TODO: leverage Django's file managing to store it
    np.save(cluster.pattern_noise_path, pn)

    return pn
