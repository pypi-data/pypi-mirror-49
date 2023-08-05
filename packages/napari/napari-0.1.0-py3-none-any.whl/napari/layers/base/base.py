import warnings
from abc import ABC, abstractmethod
from contextlib import contextmanager
from xml.etree.ElementTree import Element, tostring
import numpy as np
from skimage import img_as_ubyte

from ...util.event import Event
from ...util.keybindings import KeymapMixin
from ._visual_wrapper import VisualWrapper


class Layer(VisualWrapper, KeymapMixin, ABC):
    """Base layer class.

    Parameters
    ----------
    central_node : vispy.scene.visuals.VisualNode
        Visual node that controls all others.
    name : str, optional
        Name of the layer. If not provided, is automatically generated
        from `cls._basename()`

    Notes
    -----
    Must define the following:
        * `_get_shape()`: called by `shape` property
        * `_refresh()`: called by `refresh` method
        * `data` property (setter & getter)
        * `class_keymap` class variable (dictionary)

    May define the following:
        * `_set_view_slice(indices)`: called to set currently viewed slice
        * `_basename()`: base/default name of the layer

    Attributes
    ----------
    name
    ndim
    shape
    selected
    indices
    coordinates : tuple of float
        Coordinates of the cursor in the image space of each layer. The length
        of the tuple is equal to the number of dimensions of the layer.

    Methods
    -------
    refresh()
        Refresh the current view.
    """

    def __init__(self, central_node, name=None):
        super().__init__(central_node)
        self._selected = True
        self._freeze = False
        self._status = 'Ready'
        self._help = ''
        self._cursor = 'standard'
        self._cursor_size = None
        self._interactive = True
        self._indices = (slice(None, None, None), slice(None, None, None))
        self._position = (0, 0)
        self.coordinates = (0, 0)
        self._thumbnail_shape = (32, 32, 4)
        self._thumbnail = np.zeros(self._thumbnail_shape, dtype=np.uint8)
        self._update_properties = True
        self._name = ''
        self.events.add(
            select=Event,
            deselect=Event,
            data=Event,
            name=Event,
            thumbnail=Event,
            status=Event,
            help=Event,
            interactive=Event,
            cursor=Event,
            cursor_size=Event,
        )
        self.name = name

        self.events.opacity.connect(lambda e: self._update_thumbnail())

    def __str__(self):
        """Return self.name
        """
        return self.name

    def __repr__(self):
        cls = type(self)
        return f"<{cls.__name__} layer {repr(self.name)} at {hex(id(self))}>"

    @classmethod
    def _basename(cls):
        return f'{cls.__name__}'

    @property
    def name(self):
        """str: Layer's unique name.
        """
        return self._name

    @name.setter
    def name(self, name):
        if name == self.name:
            return
        if not name:
            name = self._basename()
        self._name = name
        self.events.name()

    @property
    def indices(self):
        """Tuple of int of Slice: Used for slicing arrays on each dimension.
        """
        return self._indices

    @indices.setter
    def indices(self, indices):
        if indices == self.indices:
            return
        self._indices = indices[-self.ndim :]
        self._update_coordinates()
        self._set_view_slice()

    @property
    def position(self):
        """2-tuple of int: Cursor position in canvas ordered (x, y)."""
        return self._position

    @position.setter
    def position(self, position):
        if self._position == position:
            return
        self._position = position
        self._update_coordinates()

    def _update_coordinates(self):
        """Insert the cursor position (x, y) into the correct position in the
        tuple of indices and update the cursor coordinates.
        """
        if self._node.canvas is not None:
            transform = self._node.canvas.scene.node_transform(self._node)
            position = transform.map(list(self.position))[:2]
            coords = list(self.indices)
            coords[-2] = position[1]
            coords[-1] = position[0]
            self.coordinates = tuple(coords)

    @property
    @abstractmethod
    def data(self):
        # user writes own docstring
        raise NotImplementedError()

    @data.setter
    @abstractmethod
    def data(self, data):
        raise NotImplementedError()

    @abstractmethod
    def _get_shape(self):
        raise NotImplementedError()

    @property
    def thumbnail(self):
        """np.ndarray: Integer array of thumbnail for the layer
        """
        return self._thumbnail

    @thumbnail.setter
    def thumbnail(self, thumbnail):
        if thumbnail.dtype != np.uint8:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                thumbnail = img_as_ubyte(thumbnail)
        self._thumbnail = thumbnail
        self.events.thumbnail()

    @property
    def ndim(self):
        """int: Number of dimensions in the data.
        """
        return len(self.shape)

    @property
    def shape(self):
        """tuple of int: Shape of the data.
        """
        return self._get_shape()

    @property
    def range(self):
        """list of 3-tuple of int: ranges of data for slicing specifed by
        (min, max, step).
        """
        return tuple((0, max, 1) for max in self.shape)

    @property
    def selected(self):
        """boolean: Whether this layer is selected or not.
        """
        return self._selected

    @selected.setter
    def selected(self, selected):
        if selected == self.selected:
            return
        self._selected = selected

        if selected:
            self.events.select()
        else:
            self.events.deselect()

    @property
    def status(self):
        """string: Status string
        """
        return self._status

    @status.setter
    def status(self, status):
        if status == self.status:
            return
        self.events.status(status=status)
        self._status = status

    @property
    def help(self):
        """string: String that can be displayed to the
        user in the status bar with helpful usage tips.
        """
        return self._help

    @help.setter
    def help(self, help):
        if help == self.help:
            return
        self.events.help(help=help)
        self._help = help

    @property
    def interactive(self):
        """bool: Determines if canvas pan/zoom interactivity is enabled or not.
        """
        return self._interactive

    @interactive.setter
    def interactive(self, interactive):
        if interactive == self.interactive:
            return
        self.events.interactive(interactive=interactive)
        self._interactive = interactive

    @property
    def cursor(self):
        """string: String identifying cursor displayed over canvas.
        """
        return self._cursor

    @cursor.setter
    def cursor(self, cursor):
        if cursor == self.cursor:
            return
        self.events.cursor(cursor=cursor)
        self._cursor = cursor

    @property
    def cursor_size(self):
        """int | None: Size of cursor if custom. None is yields default size
        """
        return self._cursor_size

    @cursor_size.setter
    def cursor_size(self, cursor_size):
        if cursor_size == self.cursor_size:
            return
        self.events.cursor_size(cursor_size=cursor_size)
        self._cursor_size = cursor_size

    @property
    def scale_factor(self):
        """float: Conversion factor from canvas coordinates to image
        coordinates, which depends on the current zoom level.
        """
        if self._node.canvas is not None:
            transform = self._node.canvas.scene.node_transform(self._node)
            scale_factor = transform.map([1, 1])[0] - transform.map([0, 0])[0]
        else:
            scale_factor = 1
        return scale_factor

    @contextmanager
    def block_update_properties(self):
        self._update_properties = False
        yield
        self._update_properties = True

    def _update(self):
        """Update the underlying visual."""
        if self._need_display_update:
            self._need_display_update = False
            if hasattr(self._node, '_need_colortransform_update'):
                self._node._need_colortransform_update = True
            self._set_view_slice()

        if self._need_visual_update:
            self._need_visual_update = False
            self._node.update()

    @abstractmethod
    def _set_view_slice(self):
        raise NotImplementedError()

    @abstractmethod
    def _update_thumbnail(self):
        raise NotImplementedError()

    def refresh(self):
        """Fully refreshes the layer. If layer is frozen refresh will not occur
        """
        if self._freeze:
            return
        self._refresh()

    def _refresh(self):
        """Fully refresh the underlying visual.
        """
        self._need_display_update = True
        self._update()

    @contextmanager
    def freeze_refresh(self):
        self._freeze = True
        yield
        self._freeze = False

    def to_xml_list(self):
        """Generates a list of xml elements for the layer.

        Returns
        ----------
        xml : list of xml.etree.ElementTree.Element
            List of a single xml element specifying the currently viewed image
            as a png according to the svg specification.
        """
        return []

    def to_svg(self, file=None, canvas_shape=None):
        """Convert the current layer state to an SVG.

        Parameters
        ----------
        file : path-like object, optional
            An object representing a file system path. A path-like object is
            either a str or bytes object representing a path, or an object
            implementing the `os.PathLike` protocol. If passed the svg will be
            written to this file
        canvas_shape : 4-tuple, optional
            View box of SVG canvas to be generated specified as `min-x`,
            `min-y`, `width` and `height`. If not specified, calculated
            from the last two dimensions of the layer.

        Returns
        ----------
        svg : string
            SVG representation of the layer.
        """

        if canvas_shape is None:
            min_shape = [r[0] for r in self.range[-2:]]
            max_shape = [r[1] for r in self.range[-2:]]
            shape = np.subtract(max_shape, min_shape)
        else:
            shape = canvas_shape[2:]
            min_shape = canvas_shape[:2]

        props = {
            'xmlns': 'http://www.w3.org/2000/svg',
            'xmlns:xlink': 'http://www.w3.org/1999/xlink',
        }

        xml = Element(
            'svg',
            height=f'{shape[0]}',
            width=f'{shape[1]}',
            version='1.1',
            **props,
        )

        transform = f'translate({-min_shape[1]} {-min_shape[0]})'
        xml_transform = Element('g', transform=transform)

        xml_list = self.to_xml_list()
        for x in xml_list:
            xml_transform.append(x)
        xml.append(xml_transform)

        svg = (
            '<?xml version=\"1.0\" standalone=\"no\"?>\n'
            + '<!DOCTYPE svg PUBLIC \"-//W3C//DTD SVG 1.1//EN\"\n'
            + '\"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd\">\n'
            + tostring(xml, encoding='unicode', method='xml')
        )

        if file:
            # Save svg to file
            with open(file, 'w') as f:
                f.write(svg)

        return svg

    def on_mouse_move(self, event):
        """Called whenever mouse moves over canvas.
        """
        return

    def on_mouse_press(self, event):
        """Called whenever mouse pressed in canvas.
        """
        return

    def on_mouse_release(self, event):
        """Called whenever mouse released in canvas.
        """
        return

    def on_key_press(self, event):
        """Called whenever key pressed in canvas.
        """
        return

    def on_key_release(self, event):
        """Called whenever key released in canvas.
        """
        return

    def on_draw(self, event):
        """Called whenever the canvas is drawn.
        """
        return
