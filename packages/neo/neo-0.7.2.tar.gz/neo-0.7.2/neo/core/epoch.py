# -*- coding: utf-8 -*-
'''
This module defines :class:`Epoch`, an array of epochs.

:class:`Epoch` derives from :class:`BaseNeo`, from
:module:`neo.core.baseneo`.
'''

# needed for python 3 compatibility
from __future__ import absolute_import, division, print_function

import sys
from copy import deepcopy

import numpy as np
import quantities as pq

from neo.core.baseneo import BaseNeo, merge_annotations
from neo.core.dataobject import DataObject, ArrayDict

PY_VER = sys.version_info[0]


def _new_epoch(cls, times=None, durations=None, labels=None, units=None, name=None,
               description=None, file_origin=None, array_annotations=None, annotations=None,
               segment=None):
    '''
    A function to map epoch.__new__ to function that
    does not do the unit checking. This is needed for pickle to work.
    '''
    e = Epoch(times=times, durations=durations, labels=labels, units=units, name=name,
              file_origin=file_origin, description=description,
              array_annotations=array_annotations, **annotations)
    e.segment = segment
    return e


class Epoch(DataObject):
    '''
    Array of epochs.

    *Usage*::

        >>> from neo.core import Epoch
        >>> from quantities import s, ms
        >>> import numpy as np
        >>>
        >>> epc = Epoch(times=np.arange(0, 30, 10)*s,
        ...             durations=[10, 5, 7]*ms,
        ...             labels=np.array(['btn0', 'btn1', 'btn2'], dtype='S'))
        >>>
        >>> epc.times
        array([  0.,  10.,  20.]) * s
        >>> epc.durations
        array([ 10.,   5.,   7.]) * ms
        >>> epc.labels
        array(['btn0', 'btn1', 'btn2'],
              dtype='|S4')

    *Required attributes/properties*:
        :times: (quantity array 1D) The start times of each time period.
        :durations: (quantity array 1D or quantity scalar) The length(s) of each time period.
           If a scalar, the same value is used for all time periods.
        :labels: (numpy.array 1D dtype='S') Names or labels for the time periods.

    *Recommended attributes/properties*:
        :name: (str) A label for the dataset,
        :description: (str) Text description,
        :file_origin: (str) Filesystem path or URL of the original data file.

    *Optional attributes/properties*:
        :array_annotations: (dict) Dict mapping strings to numpy arrays containing annotations \
                                   for all data points

    Note: Any other additional arguments are assumed to be user-specific
    metadata and stored in :attr:`annotations`,

    '''

    _single_parent_objects = ('Segment',)
    _quantity_attr = 'times'
    _necessary_attrs = (('times', pq.Quantity, 1), ('durations', pq.Quantity, 1),
                        ('labels', np.ndarray, 1, np.dtype('S')))

    def __new__(cls, times=None, durations=None, labels=None, units=None, name=None,
                description=None, file_origin=None, array_annotations=None, **annotations):
        if times is None:
            times = np.array([]) * pq.s
        if durations is None:
            durations = np.array([]) * pq.s
        elif durations.size != times.size:
            if durations.size == 1:
                durations = durations * np.ones_like(times.magnitude)
            else:
                raise ValueError("Durations array has different length to times")
        if labels is None:
            labels = np.array([], dtype='S')
        elif len(labels) != times.size:
            raise ValueError("Labels array has different length to times")
        if units is None:
            # No keyword units, so get from `times`
            try:
                units = times.units
                dim = units.dimensionality
            except AttributeError:
                raise ValueError('you must specify units')
        else:
            if hasattr(units, 'dimensionality'):
                dim = units.dimensionality
            else:
                dim = pq.quantity.validate_dimensionality(units)
        # check to make sure the units are time
        # this approach is much faster than comparing the
        # reference dimensionality
        if (len(dim) != 1 or list(dim.values())[0] != 1 or not isinstance(list(dim.keys())[0],
                                                                          pq.UnitTime)):
            ValueError("Unit %s has dimensions %s, not [time]" % (units, dim.simplified))

        obj = pq.Quantity.__new__(cls, times, units=dim)
        obj.labels = labels
        obj.durations = durations
        obj.segment = None
        return obj

    def __init__(self, times=None, durations=None, labels=None, units=None, name=None,
                 description=None, file_origin=None, array_annotations=None, **annotations):
        '''
        Initialize a new :class:`Epoch` instance.
        '''
        DataObject.__init__(self, name=name, file_origin=file_origin, description=description,
                            array_annotations=array_annotations, **annotations)

    def __reduce__(self):
        '''
        Map the __new__ function onto _new_epoch, so that pickle
        works
        '''
        return _new_epoch, (self.__class__, self.times, self.durations, self.labels, self.units,
                            self.name, self.file_origin, self.description, self.array_annotations,
                            self.annotations, self.segment)

    def __array_finalize__(self, obj):
        super(Epoch, self).__array_finalize__(obj)
        self.annotations = getattr(obj, 'annotations', None)
        self.name = getattr(obj, 'name', None)
        self.file_origin = getattr(obj, 'file_origin', None)
        self.description = getattr(obj, 'description', None)
        self.segment = getattr(obj, 'segment', None)
        # Add empty array annotations, because they cannot always be copied,
        # but do not overwrite existing ones from slicing etc.
        # This ensures the attribute exists
        if not hasattr(self, 'array_annotations'):
            self.array_annotations = ArrayDict(self._get_arr_ann_length())

    def __repr__(self):
        '''
        Returns a string representing the :class:`Epoch`.
        '''
        # need to convert labels to unicode for python 3 or repr is messed up
        if PY_VER == 3:
            labels = self.labels.astype('U')
        else:
            labels = self.labels

        objs = ['%s@%s for %s' % (label, time, dur) for label, time, dur in
                zip(labels, self.times, self.durations)]
        return '<Epoch: %s>' % ', '.join(objs)

    def _repr_pretty_(self, pp, cycle):
        super(Epoch, self)._repr_pretty_(pp, cycle)

    def rescale(self, units):
        '''
        Return a copy of the :class:`Epoch` converted to the specified
        units
        '''

        obj = super(Epoch, self).rescale(units)
        obj.segment = self.segment

        return obj

    def __getitem__(self, i):
        '''
        Get the item or slice :attr:`i`.
        '''
        obj = Epoch(times=super(Epoch, self).__getitem__(i))
        obj._copy_data_complement(self)
        try:
            # Array annotations need to be sliced accordingly
            obj.array_annotate(**deepcopy(self.array_annotations_at_index(i)))
        except AttributeError:  # If Quantity was returned, not Epoch
            pass
        return obj

    def __getslice__(self, i, j):
        '''
        Get a slice from :attr:`i` to :attr:`j`.attr[0]

        Doesn't get called in Python 3, :meth:`__getitem__` is called instead
        '''
        return self.__getitem__(slice(i, j))

    @property
    def times(self):
        return pq.Quantity(self)

    def merge(self, other):
        '''
        Merge the another :class:`Epoch` into this one.

        The :class:`Epoch` objects are concatenated horizontally
        (column-wise), :func:`np.hstack`).

        If the attributes of the two :class:`Epoch` are not
        compatible, and Exception is raised.
        '''
        othertimes = other.times.rescale(self.times.units)
        times = np.hstack([self.times, othertimes]) * self.times.units
        kwargs = {}
        for name in ("name", "description", "file_origin"):
            attr_self = getattr(self, name)
            attr_other = getattr(other, name)
            if attr_self == attr_other:
                kwargs[name] = attr_self
            else:
                kwargs[name] = "merge(%s, %s)" % (attr_self, attr_other)

        merged_annotations = merge_annotations(self.annotations, other.annotations)
        kwargs.update(merged_annotations)

        kwargs['array_annotations'] = self._merge_array_annotations(other)
        labels = kwargs['array_annotations']['labels']
        durations = kwargs['array_annotations']['durations']

        return Epoch(times=times, durations=durations, labels=labels, **kwargs)

    def _copy_data_complement(self, other):
        '''
        Copy the metadata from another :class:`Epoch`.
        Note: Array annotations can not be copied here because length of data can change
        '''
        # Note: Array annotations cannot be copied because length of data could be changed
        # here which would cause inconsistencies. This is instead done locally.
        for attr in ("name", "file_origin", "description", "annotations"):
            setattr(self, attr, getattr(other, attr, None))

    def __deepcopy__(self, memo):
        cls = self.__class__
        new_ep = cls(times=self.times, durations=self.durations, labels=self.labels,
                     units=self.units, name=self.name, description=self.description,
                     file_origin=self.file_origin)
        new_ep.__dict__.update(self.__dict__)
        memo[id(self)] = new_ep
        for k, v in self.__dict__.items():
            try:
                setattr(new_ep, k, deepcopy(v, memo))
            except TypeError:
                setattr(new_ep, k, v)
        return new_ep

    def duplicate_with_new_data(self, signal, units=None):
        '''
        Create a new :class:`Epoch` with the same metadata
        but different data (times, durations)

        Note: Array annotations can not be copied here because length of data can change
        '''

        if units is None:
            units = self.units
        else:
            units = pq.quantity.validate_dimensionality(units)

        new = self.__class__(times=signal, units=units)
        new._copy_data_complement(self)
        # Note: Array annotations can not be copied here because length of data can change
        return new

    def time_slice(self, t_start, t_stop):
        '''
        Creates a new :class:`Epoch` corresponding to the time slice of
        the original :class:`Epoch` between (and including) times
        :attr:`t_start` and :attr:`t_stop`. Either parameter can also be None
        to use infinite endpoints for the time interval.
        '''
        _t_start = t_start
        _t_stop = t_stop
        if t_start is None:
            _t_start = -np.inf
        if t_stop is None:
            _t_stop = np.inf

        indices = (self >= _t_start) & (self <= _t_stop)
        new_epc = self[indices]

        return new_epc

    def set_labels(self, labels):
        self.array_annotate(labels=labels)

    def get_labels(self):
        return self.array_annotations['labels']

    labels = property(get_labels, set_labels)

    def set_durations(self, durations):
        self.array_annotate(durations=durations)

    def get_durations(self):
        return self.array_annotations['durations']

    durations = property(get_durations, set_durations)
