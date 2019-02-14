import itertools
import numpy as np

from PIL import Image
from pyclustering.cluster import kmedoids
from skimage import img_as_float

from main.models import Picture
from skimage.restoration import denoise_wavelet
from scipy.signal import wiener
from scipy.stats import pearsonr

size = 1024


def run():
    all_pics = Picture.objects.filter(session__id='9e45t6g0kh44hrqdve359yizbne9mood')
    original = all_pics.filter(type='original')[0:2]
    other = all_pics.filter(type='facebook')
    other = other[len(other) - 2:len(other)]
    pics = list(itertools.chain(original, other))
    noises = []

    for p in pics:
        with Image.open(p.pic_path) as pic:
            pic: Image
            width, height = pic.size
            if width > height:
                pic = pic.transpose(Image.ROTATE_90)
            width, height = pic.size

            pic = pic.crop((width / 2 - size / 2, height / 2 - size / 2, width / 2 + size / 2, height / 2 + size / 2))
            _, pic, _ = pic.split()
            pic_float = img_as_float(pic)
            denoised = denoise_wavelet(pic_float)
            noise = pic_float - denoised
            noise = (noise - noise.mean(axis=0)) / noise.std(axis=0)
            noise = wiener(noise)
            noises.append(noise)

    corrs = [[1 - abs(pearsonr(a.flatten(), b.flatten())[0]) for b in noises] for a in noises]
    for i, row in enumerate(corrs):
        corrs[i][i] = 1
        corrs[i] = row - np.min(row)
        corrs[i][i] = 0
        corrs[i] = corrs[i] / np.max(corrs[i])
    print(corrs)
