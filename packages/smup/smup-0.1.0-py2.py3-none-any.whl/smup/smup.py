import numpy as np
from numba import njit
from matplotlib import pyplot as plt
import logging
from pathlib import Path


@njit
def dist_2(center, points):
    """
    Parameters
    ----------
    center: :class:`~numpy.ndarray`
        2-D coordinate of the center.
    points: :class:`~numpy.ndarray`
        2-D coordinates of the points

    Returns
    -------
    :class:`~numpy.ndarray`
        Square of Euclidian distances between center and points.

    Examples
    --------

    >>> center = np.array([0, 0])
    >>> points = np.array([ [0.3, 1, 2], [0.4, 0, 1] ])
    >>> dist_2(center, points)
    array([0.25, 1.  , 5.  ])
    """
    return (points[0, :] - center[0]) ** 2 + (points[1, :] - center[1]) ** 2


@njit
def dist_1(center, points):
    """
    Parameters
    ----------
    center: :class:`~numpy.ndarray`
        2-D coordinate of the center.
    points: :class:`~numpy.ndarray`
        2-D coordinates of the points

    Returns
    -------
    :class:`~numpy.ndarray`
        Manhattan distances between center and points.

    Examples
    --------

    >>> center = np.array([0, 0])
    >>> points = np.array([ [0.3, 1, 2], [0.4, 0, 1] ])
    >>> dist_1(center, points)
    array([0.7, 1. , 3. ])
    """
    return np.abs(points[0, :] - center[0]) + np.abs(points[1, :] - center[1])


@njit
def dist_inf(center, points):
    """
    Parameters
    ----------
    center: :class:`~numpy.ndarray`
        2-D coordinate of the center.
    points: :class:`~numpy.ndarray`
        2-D coordinates of the points

    Returns
    -------
    :class:`~numpy.ndarray`
        Inf-norm distances between center and points.

    Examples
    --------

    >>> center = np.array([0, 0])
    >>> points = np.array([ [0.3, 1, 2], [0.4, 0, 1] ])
    >>> dist_inf(center, points)
    array([0.4, 1. , 2. ])
    """
    return np.maximum(np.abs(points[0, :] - center[0]), np.abs(points[1, :] - center[1]))


def ascii_display(picture, centers):
    """
    Parameters
    ----------
    picture: :class:`~numpy.ndarray`
        A xXy array populated with s distinct floats in [0, 1] that hints the area of each pixel
    centers: :class:`~numpy.ndarray`
        Coordinates of the area centers

    Returns
    -------
    :class:`str`
        ASCII display of the matching.
    """
    _, s = centers.shape
    center_set = {(int(centers[0, i]), int(centers[1, i])) for i in range(s)}

    def pixel_to_txt(x, y):
        if (x, y) in center_set:
            return "X"
        else:
            return str(picture[y, x])

    h, w = picture.shape
    return "\n".join(" ".join(pixel_to_txt(x, y) for x in range(w)) for y in range(h))


@njit
def compute(x, y, s, distance_function, seed=None):
    """
    Main function of the package. Computes the pictures.

    Parameters
    ----------
    x: :py:class:`int`
        Width of the picture (in pixels)
    y: :py:class:`int`
        Height of the picture (in pixels)
    s: :py:class:`int`
        Number of areas to display in the picture
    distance_function: callable
        Functions that computes distances between a center and points
    seed: :py:class:`int`, optional
        Random seed

    Returns
    -------
    picture: :class:`~numpy.ndarray`
        A xXy array populated with s distinct floats in [0, 1] that hints the area of each pixel
    centers: :class:`~numpy.ndarray`
        Coordinates of the area centers
    """
    xy = x * y
    # pixel quota for each area
    bb = round(xy / s)
    # Draw s centers
    if seed is not None:
        np.random.seed(seed)
    centers = np.random.rand(2, s)  # np.random.rand(2,s) #% Coordonnées des sites, penser à la déformation
    centers[0, :] *= x
    centers[1, :] *= y
    # Compute coordinates of all pixels
    points = np.zeros((2, xy))
    for xi in range(x):
        points[0, (xi * y):((xi + 1) * (y))] = xi + 0.5
    for yi in range(y):
        points[1, yi:xy:y] = yi + 0.5
    # Compute distances between all centers and all pixels
    dist = np.zeros(s * xy)
    for si in range(s):
        dist[si * xy:(si + 1) * xy] = distance_function(centers[:, si], points)
    # Sort the indexes by increasing distance
    edges = np.argsort(dist)
    # Prepare main loop
    quotas = bb * np.ones(s, dtype=np.int32)
    results = s * np.ones((y, x), dtype=np.int32)
    pixels = xy
    # Main allocation loop
    for e in edges:
        # edge center
        si = e // xy
        # Check center needs to expand
        if quotas[si] != 0:
            # Pixel
            xyi = e % xy
            xi = xyi // y
            yi = xyi % y
            # Check pixel is free
            if results[yi, xi] == s:
                results[yi, xi] = si
                quotas[si] -= 1
                pixels -= 1
                if pixels == 0:
                    break
    return results, centers


class Smup:
    """
    Main interface with two main methods:
    :py:meth:`~smup.smup.Smup.compute`
    and
    :py:meth:`~smup.smup.Smup.display`.
    """

    def __init__(self):
        self.s = None
        self.picture = None
        self.centers = None

    def compute(self, x=1024, y=720, s=20, norm=2, seed=None):
        """
        Parameters
        ----------
        x: :py:class:`int`
            Width of the picture (in pixels)
        y: :py:class:`int`
            Height of the picture (in pixels)
        s: :py:class:`int`
            Number of areas to display in the picture
        norm: :py:class:`int` or :py:class:`str`
            Distance to use. Can be 1, 2, or 'inf'
        seed: :py:class:`int`, optional
            Random seed

        Returns
        -------
        None

        Examples
        --------

        >>> matcher = Smup()
        >>> matcher.compute(x=30, y=20, s=3, norm=2, seed=42)
        >>> txt = ascii_display(matcher.picture, matcher.centers)
        >>> print(txt) # doctest: +SKIP
        1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 X 2 2 2 1 1 1 X 1
        1 1 1 1 1 2 2 2 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 0 0 0 0 0 0 0 0 X 0 0 0 0 0 0 0 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 1 1 1 0 0 0 0 0 0 1 1 1 1 1 2 2 2 2 2 1 1 1 1 1 1

        >>> matcher.compute(x=30, y=20, s=3, norm=1, seed=42)
        >>> txt = ascii_display(matcher.picture, matcher.centers)
        >>> print(txt) # doctest: +SKIP
        1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 2 2 2 2 2 2 2 2 0 2 2 2 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 2 2 2 2 2 2 0 0 0 0 2 2 2 2 2 2 2 2 X 2 2 2 1 1 1 X 1
        1 1 1 2 2 2 2 2 2 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 2 2 2 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 1 1 1 1 1
        1 0 0 0 0 0 0 0 0 0 0 X 0 0 0 0 0 0 0 0 0 2 2 2 2 1 1 1 1 1
        1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 1 1 1 1 1
        1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 1 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 1 1 1 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 1 1 1 1 0 0 0 0 0 1 1 1 1 1 2 2 2 2 2 2 1 1 1 1 1

        >>> matcher.compute(x=30, y=20, s=3, norm="inf", seed=42)
        >>> txt = ascii_display(matcher.picture, matcher.centers)
        >>> print(txt) # doctest: +SKIP
        1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 X 2 2 2 1 1 1 X 1
        1 1 2 2 2 2 0 2 2 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 2 2 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 2 2 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 1 1 1 1 1 1
        1 1 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 1 1 1 1 1 1 1
        1 1 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 1 1 1 1 1 1 1 1
        1 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 1 1 1 1 1 1 1 1 1
        1 2 2 2 0 0 0 0 0 0 0 X 0 0 0 0 0 0 0 2 1 1 1 1 1 1 1 1 1 1
        1 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1
        1 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1
        1 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1
        1 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1
        1 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1
        1 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1
        1 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1
        1 2 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1

        Unclear norm defaults to Euclidian norm (and a warning is issued).

        >>> matcher.compute(x=30, y=20, s=3, norm="??", seed=42)
        >>> txt = ascii_display(matcher.picture, matcher.centers)
        >>> print(txt) # doctest: +SKIP
        1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 X 2 2 2 1 1 1 X 1
        1 1 1 1 1 2 2 2 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 0 0 0 0 0 0 0 0 X 0 0 0 0 0 0 0 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 1 1 1 1 1
        1 1 1 1 1 1 1 1 0 0 0 0 0 0 1 1 1 1 1 2 2 2 2 2 1 1 1 1 1 1
        """
        self.s = s
        if str(norm) == 'inf':
            dist = dist_inf
        elif str(norm) == '1':
            dist = dist_1
        elif str(norm) == '2':
            dist = dist_2
        else:
            logging.warning(f"Norm {norm} unknown, defaulting to 2-norm.")
            dist = dist_2
        self.picture, self.centers = compute(x, y, s, dist, seed)

    def display(self, cmap='jet', draw_centers=True, center_size=20, save=None):
        """

        Parameters
        ----------
        cmap: :class:`str`
            Matplotlib colormap to use. Defaults to 'jet'
        draw_centers: :class:`bool`
            Draw centers of areas. Defaults to True.
        center_size: :class:`int`
            Size of centers, if drawn. Defaults to 20.
        save: :class:`str` ot :class:`~pathlib.Path`, optional
            Filename for saving picture.

        Returns
        -------
        None

        Examples
        --------

        See :doc:`/use` for graphical examples. Here we just show the file saving feature.

        >>> from pathlib import Path
        >>> import tempfile
        >>> matcher = Smup()
        >>> matcher.compute(x=30, y=20, s=3, norm=2, seed=42)
        >>> with tempfile.TemporaryDirectory() as tmpdirname:
        ...     fn = tmpdirname/Path("picture.png")
        ...     matcher.display(save=fn)
        ...     size=fn.stat().st_size
        >>> size
        55984
        """
        plt.figure(figsize=(40, 30))
        img = plt.imshow(self.picture / self.s)
        plt.contour(self.picture, levels=2 * self.s, colors='black')
        img.set_cmap(cmap)
        if draw_centers:
            plt.plot(self.centers[0, :], self.centers[1, :], 'k.', markersize=center_size)
        plt.xticks([], [])
        plt.yticks([], [])
        if save and (isinstance(save, str) or isinstance(save, Path)):
            plt.savefig(save, bbox_inches='tight')
