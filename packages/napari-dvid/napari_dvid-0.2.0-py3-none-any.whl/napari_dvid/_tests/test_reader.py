from napari_dvid import napari_get_reader


def test_get_reader_pass():
    reader = napari_get_reader("")
    assert reader is None
