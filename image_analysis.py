import scipy
from sklearn.cluster import MiniBatchKMeans
import numpy as np
from PIL import Image


class Reducer:
    def __init__(self, image: Image):
        self.arr = np.asarray(image, dtype=np.float16)
        self.arr = self.arr.reshape(-1, self.arr.shape[-1])

    def identify_dominant_colors(self, num_colors: int) -> list[tuple]:
        """
        Return N dominant colors of image, since average color of an image is usually brown.
        :param num_colors: Number of dominant colors to find.
        :return: Sorted list of colors, first element is most dominant color in image.
        """
        kmeans = MiniBatchKMeans(
            n_clusters=16,
            init="k-means++",
            n_init='auto',
            max_iter=20,
            random_state=137
        ).fit(self.arr)
        codes = kmeans.cluster_centers_

        vecs, _ = scipy.cluster.vq.vq(self.arr, codes)
        counts, _ = np.histogram(vecs, len(codes))

        colors = []
        for index in np.argsort(counts)[::-1][:num_colors]:
            colors.append(tuple([int(code) for code in codes[index]]))
        return colors

    def classify_rgb_to_color_name(self, rgb: tuple) -> str:
        # TODO: implement classification of color tuple to a string like (30, 200, 30) -> 'green'
        return 'black'

    def identify_brightness(self) -> float:
        """
        Identify the relative luminance of the image (a proxy for human perceived brightness: https://en.wikipedia.org/wiki/Relative_luminance)
        :return: float, perceived brightness of image
        """
        avg = np.mean(self.arr, axis=0)
        return 0.2126 * avg[0] + 0.7152 * avg[1] + 0.0722 * avg[2]

