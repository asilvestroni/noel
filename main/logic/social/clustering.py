# ----------------------------
#  Andrea Silvestroni 2019
#  Residual Noise Extraction and Smartphone Linking
#
#  Picture clustering functions
# ----------------------------

import numpy as np
from pyclustering.cluster.kmedoids import kmedoids
from typing import List

from main.logic.common import timeit, status_extracted
from main.models import Picture, PictureCluster, Session
from scipy.stats import pearsonr


@timeit
def clusterize(ses: Session, cluster_type: str) -> List[PictureCluster]:
    """
    Divides the pictures associated with the provided session and type into a main cluster and a secondary one.
    The main cluster contains the biggest group of pictures that most likely share origin (i.e. same smartphone),
    while the secondary one is comprised of all the other ones

    :param ses: Session that contains the pictures
    :param cluster_type: Type of pictures to split into clusters
    :return: A list containing two PictureCluster instances
    """
    matrix: np.ndarray

    def compute_distance_matrix() -> np.ndarray:
        """
        Computes the distance matrix between the provided pictures

        :return: The computed distance matrix
        """
        # Collect all residual noises
        rns = np.array([np.load(pic.noise_path) for pic in pictures])
        n = len(rns)

        corrs = np.zeros((n, n))

        for i, a in enumerate(rns):
            for j, b in enumerate(rns):
                if corrs[j][i] != 0:
                    corrs[i][j] = corrs[j][i]
                else:
                    # Compute correlations, first in the original orientation and then rotated by 180 degrees,
                    # to make up for missing rotation data
                    corr1 = abs(pearsonr(a.flatten(), b.flatten())[0])
                    corr2 = abs(pearsonr(np.rot90(a, 2).flatten(), b.flatten())[0])

                    if corr1 > corr2:
                        corrs[i][j] = corr1
                    else:
                        corrs[i][j] = corr2

        # Normalize matrix
        for i in range(n):
            # Set diagonal to 0
            corrs[i][i] = 0

            # Normalize row between 0 and 1
            c_min = np.min(corrs[i])
            corrs[i] -= c_min

            c_max = np.max(corrs[i])
            corrs[i] /= c_max

            # Set diagonal back to 1
            corrs[i][i] = 1

        # Return the distances
        return 1 - corrs

    pictures = Picture.objects.filter(session=ses, type=cluster_type, status=status_extracted)

    matrix_path = 'storage/{}/{}/distance_matrix.npy'.format(ses.id, cluster_type)

    # Compute distances
    matrix = compute_distance_matrix()
    np.save(matrix_path, matrix)

    # Cluster pictures based on distances
    initial_medoids = [0, np.argmax(matrix[0])]
    kmed = kmedoids(matrix, initial_medoids)
    kmed.process()
    clusters = kmed.get_clusters()

    result = []
    pics = list(pictures)

    # Create clusters and associate pictures with the respective one
    for i, c in enumerate(clusters):
        cluster = PictureCluster(label=str(i), type=cluster_type, session=ses, original=False)
        cluster.save()

        for pic_id in c:
            pics[pic_id].cluster = cluster
            pics[pic_id].save()

        result.append(cluster)

    return result
