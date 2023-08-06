from collections import OrderedDict
from abc import ABCMeta, abstractmethod
import cv2
import numpy as np
import copy

from ..data import DataContainer, KeyPoints
from ..constants import allowed_interpolations, allowed_paddings
from ..utils import validate_parameter, img_shape_checker
import random


class BaseTransform(metaclass=ABCMeta):
    """Transformation abstract class.

    Parameters
    ----------
    p : float or None
        Probability of executing this transform
    data_indices : tuple or None
        Indices where the transforms need to be applied
    """
    def __init__(self, p=None, data_indices=None):
        if p is None:
            p = 0.5

        self.p = p
        if data_indices is not None and not isinstance(data_indices, tuple):
            raise TypeError
        if isinstance(data_indices, tuple):
            for el in data_indices:
                if not isinstance(el, int):
                    raise TypeError
                if el < 0:
                    raise ValueError

        self._data_indices = data_indices

        self.state_dict = None
        self.reset_state()

    def reset_state(self):
        self.state_dict = {'use': False}

    def serialize(self, include_state=False):
        """Method returns an ordered dict, describing the object.

        Parameters
        ----------
        include_state : bool
            Whether to include a self.state_dict into the result. Mainly useful for debug.
        Returns
        -------
        out : OrderedDict
            OrderedDict, ready for json serialization.

        """
        if not include_state:
            d = dict(
                map(lambda item: (item[0].split('_')[-1], item[1]),
                    filter(lambda item: item[0] != 'state_dict',
                           self.__dict__.items())
                    )
            )
        else:
            d = dict(map(lambda item: (item[0].split('_')[-1], item[1]), self.__dict__.items()))

        res = {}
        for item in d.items():
            if hasattr(item[1], "serialize"):
                res[item[0]] = item[1].serialize()
            else:
                res[item[0]] = item[1]
        # the method must return the result always in the same order
        return OrderedDict(sorted(res.items()))

    def use_transform(self):
        """Method to randomly determine whether to use this transform.

        Returns
        -------
        out : bool
            Boolean flag. True if the transform is used.
        """
        if random.random() <= self.p:
            self.state_dict['use'] = True
            return True

        self.state_dict['use'] = False
        return False

    @abstractmethod
    def sample_transform(self):
        """Abstract method. Must be implemented in the child classes

        Returns
        -------
        None

        """

    def apply(self, data):
        """Applies transformation to a DataContainer items depending on the type.

        Parameters
        ----------
        data : DataContainer
            Data to be augmented

        Returns
        -------
        out : DataContainer
            Result

        """
        result = []
        types = []
        settings = {}
        if self._data_indices is None:
            self._data_indices = np.arange(0, len(data)).astype(int)
        tmp_item = None
        for i, (item, t, item_settings) in enumerate(data):
            if i in self._data_indices:
                if t == 'I':  # Image
                    tmp_item = self._apply_img(item, item_settings)
                elif t == 'M':  # Mask
                    tmp_item = self._apply_mask(item, item_settings)
                elif t == 'P':  # Points
                    tmp_item = self._apply_pts(item, item_settings)
                elif t == 'L':  # Labels
                    tmp_item = self._apply_labels(item, item_settings)
            else:
                if t == 'I' or t == 'M':
                    tmp_item = item.copy()
                elif t == 'L':
                    tmp_item = copy.copy(item)
                elif t == 'P':
                    tmp_item = copy.copy(item)

            types.append(t)
            result.append(tmp_item)
            settings[i] = item_settings

        return DataContainer(data=tuple(result), fmt=''.join(types))

    def __call__(self, data):
        """Applies the transform to a DataContainer

        Parameters
        ----------
        data : DataContainer
            Data to be augmented

        Returns
        -------
        out : DataContainer
            Result

        """
        self.reset_state()
        if self.use_transform():
            self.sample_transform()
            return self.apply(data)
        else:
            return data

    @abstractmethod
    def _apply_img(self, img: np.ndarray, settings: dict):
        """Abstract method, which determines the transform's behaviour when it is applied to images HxWxC.

        Parameters
        ----------
        img : numpy.ndarray
            Image to be augmented

        Returns
        -------
        out : numpy.ndarray

        """

    @abstractmethod
    def _apply_mask(self, mask: np.ndarray, settings: dict):
        """Abstract method, which determines the transform's behaviour when it is applied to masks HxW.

        Parameters
        ----------
        mask : numpy.ndarray
            Mask to be augmented

        Returns
        -------
        out : numpy.ndarray
            Result

        """

    @abstractmethod
    def _apply_labels(self, labels, settings: np.ndarray):
        """Abstract method, which determines the transform's behaviour when it is applied to labels (e.g. label smoothing)

        Parameters
        ----------
        labels : numpy.ndarray
            Array of labels.

        Returns
        -------
        out : numpy.ndarray
            Result

        """

    @abstractmethod
    def _apply_pts(self, pts: KeyPoints, settings: dict):
        """Abstract method, which determines the transform's behaviour when it is applied to keypoints.

        Parameters
        ----------
        pts : KeyPoints
            Keypoints object

        Returns
        -------
        out : KeyPoints
            Result

        """


class ImageTransform(BaseTransform):
    """Abstract class, allowing the application of a transform only to an image

    """
    def __init__(self, p=None, data_indices=None):
        super(ImageTransform, self).__init__(p=p, data_indices=data_indices)

    def _apply_mask(self, mask, settings: dict):
        return mask

    def _apply_pts(self, pts: KeyPoints, settings: dict):
        return pts

    def _apply_labels(self, labels, settings: dict):
        return labels

    @abstractmethod
    def _apply_img(self, img: np.ndarray, settings: dict):
        """Abstract method, which determines the transform's behaviour when it is applied to images HxWxC.

        Parameters
        ----------
        img : numpy.ndarray
            Image to be augmented

        Returns
        -------
        out : numpy.ndarray

        """


class DataDependentSamplingTransform(BaseTransform):
    def __init__(self, p=0.5, data_indices=None):
        """A class, which indicates that we sample its parameters based on data.

        Such transforms are Crops, Elastic deformations etc, where the data is needed to make sampling.

        """
        super(DataDependentSamplingTransform, self).__init__(p=p, data_indices=data_indices)

    def sample_transform(self):
        raise NotImplementedError

    def sample_transform_from_data(self, data: DataContainer):
        """Samples transform parameters based on data.

        Parameters
        ----------
        data : DataContainer
            Data container to be used for sampling.

        Returns
        -------
        out : tuple
            Coordinate frame (h, w).
        """
        prev_h = None
        prev_w = None
        # Let's make sure that all the objects have the same coordinate frame
        for obj, t, settings in data:
            if t == 'M' or t == 'I':
                h = obj.shape[0]
                w = obj.shape[1]
            elif t == 'P':
                h = obj.H
                w = obj.W
            elif t == 'L':
                continue

            if prev_h is None:
                prev_h = h
            else:
                if prev_h != h:
                    raise ValueError

            if prev_w is None:
                prev_w = w
            else:
                if prev_w != w:
                    raise ValueError
        return prev_h, prev_w

    def __call__(self, data: DataContainer):
        """Applies the transform to a DataContainer

        Parameters
        ----------
        data : DataContainer
            Data to be augmented

        Returns
        -------
        out : DataContainer
            Result

        """
        if self.use_transform():
            self.sample_transform_from_data(data)
            return self.apply(data)
        else:
            return data

    @abstractmethod
    def _apply_img(self, img: np.ndarray, settings: dict):
        """Abstract method, which determines the transform's behaviour when it is applied to images HxWxC.

        Parameters
        ----------
        img : numpy.ndarray
            Image to be augmented

        Returns
        -------
        out : numpy.ndarray

        """

    @abstractmethod
    def _apply_mask(self, mask: np.ndarray, settings: dict):
        """Abstract method, which determines the transform's behaviour when it is applied to masks HxW.

        Parameters
        ----------
        mask : numpy.ndarray
            Mask to be augmented

        Returns
        -------
        out : ndarray
            Result

        """

    @abstractmethod
    def _apply_labels(self, labels, settings: dict):
        """Abstract method, which determines the transform's behaviour when it is applied to labels (e.g. label smoothing)

        Parameters
        ----------
        labels : numpy.ndarray
            Array of labels.

        Returns
        -------
        out : numpy.ndarray
            Result

        """

    @abstractmethod
    def _apply_pts(self, pts: KeyPoints, settings: dict):
        """Abstract method, which determines the transform's behaviour when it is applied to keypoints.

        Parameters
        ----------
        pts : KeyPoints
            Keypoints object

        Returns
        -------
        out : KeyPoints
            Result

        """


class PaddingPropertyHolder(object):
    """PaddingPropertyHolder

    Adds padding property to a class and validates it using the allowed paddings from constants.

    Parameters
    ----------
    padding : None or str
        Padding mode.

    """
    def __init__(self, padding=None):
        super(PaddingPropertyHolder, self).__init__()
        self._padding = validate_parameter(padding, allowed_paddings, 'z')

    @property
    def padding(self):
        return self._padding

    @padding.setter
    def padding(self, value):
        self._padding = validate_parameter(value, allowed_paddings, 'z')


class InterpolationPropertyHolder(object):
    """InterpolationPropertyHolder

    Adds interpolation property to a class and validates it using the allowed interpolations from constants.

    Parameters
    ----------
    interpolation : None or str
        Padding mode.

    """
    def __init__(self, interpolation=None):
        super(InterpolationPropertyHolder, self).__init__()
        self._interpolation = validate_parameter(interpolation, allowed_interpolations, 'bilinear')

    @property
    def interpolation(self):
        return self._interpolation

    @interpolation.setter
    def interpolation(self, value):
        self._interpolation = validate_parameter(value, allowed_interpolations, 'bilinear')


class MatrixTransform(BaseTransform, InterpolationPropertyHolder, PaddingPropertyHolder):
    """Matrix Transform abstract class. (Affine and Homography).
    Does all the transforms around the image /  center.

    Parameters
    ----------
    interpolation : str
        Interpolation mode.
    padding : str
        Padding Mode.
    p : float
        Probability of transform's execution.
    ignore_state : bool
        Whether to ignore the pre-calculated transformation or not. If False,
        then it will lead to an incorrect behavior when the objects are of different sizes.
        Should be used only when it is assumed that the image, mask and keypoints are of
        the same size.

    """
    def __init__(self, interpolation='bilinear', padding='z', p=0.5, ignore_state=True):
        BaseTransform.__init__(self, p=p, data_indices=None)
        InterpolationPropertyHolder.__init__(self, interpolation=interpolation)
        PaddingPropertyHolder.__init__(self, padding=padding)
        self._ignore_state = ignore_state
        self.reset_state()

    def reset_state(self):
        BaseTransform.reset_state(self)
        self.state_dict['transform_matrix'] = np.eye(3)

    def fuse_with(self, trf):
        """
        Takes a transform an performs a matrix fusion. This is useful to optimize the computations

        Parameters
        ----------
        trf : MatrixTransform

        """

        if trf.padding is not None:
            self.padding = trf.padding
        self.interpolation = trf.interpolation

        self.state_dict['transform_matrix'] = trf.state_dict['transform_matrix'] @ self.state_dict['transform_matrix']

    @abstractmethod
    def sample_transform(self):
        """Abstract method. Must be implemented in the child classes

        Returns
        -------
        None

        """

    @staticmethod
    def correct_for_frame_change(M: np.ndarray, W: int, H: int):
        """Method takes a matrix transform, and modifies its origin.

        Parameters
        ----------
        M : numpy.ndarray
            Transform (3x3) matrix
        W : int
            Width of the coordinate frame
        H : int
            Height of the coordinate frame
        Returns
        -------
        out : numpy.ndarray
            Modified Transform matrix

        """
        # First we correct the transformation so that it is performed around the origin
        M = M.copy()
        origin = [(W - 1) // 2, (H - 1) // 2]
        T_origin = np.array([1, 0, -origin[0],
                             0, 1, -origin[1],
                             0, 0, 1]).reshape((3, 3))

        T_origin_back = np.array([1, 0, origin[0],
                                  0, 1, origin[1],
                                  0, 0, 1]).reshape((3, 3))
        M = T_origin_back @ M @ T_origin

        # Now, if we think of scaling, rotation and translation, the image gets increased when we
        # apply any transform.

        # This is needed to recalculate the size of the image after the transformation.
        # The core idea is to transform the coordinate grid
        # left top, left bottom, right bottom, right top
        coord_frame = np.array([[0, 0, 1], [0, H, 1], [W, H, 1], [W, 0, 1]])
        new_frame = np.dot(M, coord_frame.T).T
        new_frame[:, 0] /= new_frame[:, -1]
        new_frame[:, 1] /= new_frame[:, -1]
        new_frame = new_frame[:, :-1]
        # Computing the new coordinates

        # If during the transform, we obtained negative coordinates, we have to move to the origin
        if np.any(new_frame[:, 0] < 0):
            new_frame[:, 0] += abs(new_frame[:, 0].min())
        if np.any(new_frame[:, 1] < 0):
            new_frame[:, 1] += abs(new_frame[:, 1].min())
        # In case of scaling the coordinate_frame, we need to move back to the origin
        new_frame[:, 0] -= new_frame[:, 0].min()
        new_frame[:, 1] -= new_frame[:, 1].min()
        W_new = int(np.round(new_frame[:, 0].max()))
        H_new = int(np.round(new_frame[:, 1].max()))

        M[0, -1] += W_new // 2 - origin[0]
        M[1, -1] += H_new // 2 - origin[1]

        return M, W_new, H_new

    def _apply_img_or_mask(self, img: np.ndarray, settings: dict):
        """Applies a transform to an image or mask without controlling the shapes.

        Parameters
        ----------
        img : numpy.ndarray
            Image or mask
        settings : dict
            Item-wise settings

        Returns
        -------
        out : numpy.ndarray
            Warped image

        """
        if 'w_new' in self.state_dict and not self._ignore_state:
            w_new = self.state_dict['w_new']
            h_new = self.state_dict['h_new']

            w = self.state_dict['w']
            h = self.state_dict['h']

            if w != img.shape[1] or h != img.shape[0]:
                raise ValueError('Ignore state is False, but the items in DataContainer are of different sizes!!!')

            transform_m_corrected = self.state_dict['transform_matrix_corrected']
        else:
            transform_m = self.state_dict['transform_matrix']
            transform_m_corrected, w_new, h_new = MatrixTransform.correct_for_frame_change(transform_m,
                                                                                           img.shape[1], img.shape[0])

            self.state_dict['transform_matrix_corrected'] = transform_m_corrected

            self.state_dict['w'] = img.shape[1]
            self.state_dict['h'] = img.shape[0]

            self.state_dict['w_new'] = w_new
            self.state_dict['h_new'] = h_new

        interp = allowed_interpolations[self.interpolation[0]]
        if settings['interpolation'][1] == 'strict':
            interp = allowed_interpolations[settings['interpolation'][0]]

        padding = allowed_paddings[self.padding[0]]
        if settings['padding'][1] == 'strict':
            padding = allowed_paddings[settings['padding'][0]]

        return cv2.warpPerspective(img, transform_m_corrected, (w_new, h_new), flags=interp, borderMode=padding)

    @img_shape_checker
    def _apply_img(self, img: np.ndarray, settings: dict):
        """Applies a matrix transform to an image.
        If padding is None, the default behavior (zero padding) is expected.

        Parameters
        ----------
        img : numpy.ndarray
            Input Image
        settings : dict
            Item-wise settings

        Returns
        -------
        out : numpy.ndarray
            Output Image

        """

        return self._apply_img_or_mask(img, settings)

    def _apply_mask(self, mask: np.ndarray, settings: dict):
        """Abstract method, which defines the transform's behaviour when it is applied to masks HxW.

        If padding is None, the default behavior (zero padding) is expected.

        Parameters
        ----------
        mask : numpy.ndarray
            Mask to be augmented
        settings : dict
            Item-wise settings

        Returns
        -------
        out : numpy.ndarray
            Result

        """
        return self._apply_img_or_mask(mask, settings)

    def _apply_labels(self, labels, settings: dict):
        """Transform's application to labels. Simply returns them back without modifications.

        Parameters
        ----------
        labels : numpy.ndarray
            Array of labels.
        settings : dict
            Item-wise settings

        Returns
        -------
        out : numpy.ndarray
            Result

        """
        return labels

    def _apply_pts(self, pts: KeyPoints, settings: dict):
        """Abstract method, which defines the transform's behaviour when it is applied to keypoints.

        Parameters
        ----------
        pts : KeyPoints
            Keypoints object
        settings : dict
            Item-wise settings

        Returns
        -------
        out : KeyPoints
            Result

        """
        if self.padding[0] == 'r':
            raise ValueError('Cannot apply transform to keypoints with reflective padding!')

        pts_data = pts.data.copy()
        if 'w_new' in self.state_dict and not self._ignore_state:
            w_new = self.state_dict['w_new']
            h_new = self.state_dict['w_new']
            transform_m_corrected = self.state_dict['transform_matrix_corrected']
        else:
            transform_matrix = self.state_dict['transform_matrix']
            transform_m_corrected, w_new, h_new = MatrixTransform.correct_for_frame_change(transform_matrix,
                                                                                           pts.W, pts.H)
            self.state_dict['w'] = pts.W
            self.state_dict['h'] = pts.H

            self.state_dict['w_new'] = w_new
            self.state_dict['h_new'] = h_new

        pts_data = np.hstack((pts_data, np.ones((pts_data.shape[0], 1))))
        pts_data = np.dot(transform_m_corrected, pts_data.T).T

        pts_data[:, 0] /= pts_data[:, 2]
        pts_data[:, 1] /= pts_data[:, 2]

        return KeyPoints(pts_data[:, :-1], h_new, w_new)
