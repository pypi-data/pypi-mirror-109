import requests
import numpy as np
from napari_plugin_engine import napari_hook_implementation


@napari_hook_implementation
def napari_get_reader(path):
    """A basic implementation of the napari_get_reader hook specification.

    Parameters
    ----------
    path : str
        Url to DVID volume

    Returns
    -------
    function or None
        If the url is a not empty, return a function that accepts the url and
        returns a list of layer data tuples.
    """
    if path == "":
        return None

    return reader_function


def reader_function(path):
    """Take a url, load data, and return a list of LayerData tuples.

    Readers are expected to return data as a list of tuples, where each tuple
    is (data, [add_kwargs, [layer_type]]), "add_kwargs" and "layer_type" are
    both optional.

    Parameters
    ----------
    path : str
        Url to DVID volume

    Returns
    -------
    layer_data : list of tuples
        A list of LayerData tuples where each tuple in the list contains
        (data, metadata, layer_type), where data is a numpy array, metadata is
        a dict of keyword arguments for the corresponding viewer.add_* method
        in napari, and layer_type is a lower-case string naming the type of
        layer.

        Both "meta", and "layer_type" are optional. napari will default to
        layer_type=="image" if not provided
    """
    # TODO: handle failed requests
    r = requests.get(path)

    deserialized_bytes = np.frombuffer(r.content, dtype=np.int8)
    data = np.reshape(deserialized_bytes, newshape=(256, 256, 256))

    return [(data,)]
