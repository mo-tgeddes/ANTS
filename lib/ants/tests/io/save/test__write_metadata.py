# (C) Crown Copyright, Met Office. All rights reserved.
#
# This file is part of ANTS and is released under the BSD 3-Clause license.
# See LICENSE.txt in the root of the repository for full licensing details.
import ants.tests.stock as stock
from ants.io.save import _write_metadata
import pytest
from unittest import mock
import os

@pytest.mark.filterwarnings("ignore:license has been written to sidecar file /var/tmp/:UserWarning")
def test_license_attribute_written(tmp_path):
    """Tests that a cube with a license is written out."""
    cube = stock.geodetic(shape=(2,2))
    license = "This is a cube's license. "
    cube.attributes["license"] = license
    cube.rename("license test cube")
    filename = tmp_path / "test_cube"
    _write_metadata([cube], filename)
    expected_filename = str(filename) + ".license"
    with open(expected_filename, 'r') as file:
        actual_license = file.read()
    assert actual_license == license

@pytest.mark.filterwarnings("ignore:license has been written to sidecar file /var/tmp/:UserWarning")
def test_loaded_license_written(tmp_path):
    """Tests that a cube with a license that resembles the format of a longer license
    written in, is written out correctly."""
    loaded_license = [
        "This is the license of the cube.\n",
        "\n",
        "    It should be preserved and added to the cube when loaded.\n",
        "    ",
    ]
    cube = stock.geodetic(shape=(2,2))
    cube.attributes["license"] = loaded_license
    cube.rename("loaded license test cube")
    filename = tmp_path / "test_cube"
    _write_metadata([cube], filename)
    expected_filename = str(filename) + ".license"
    with open(expected_filename, 'r') as file:
        actual_license = file.readlines()
    assert actual_license == loaded_license

def test_warning_given():
    """Tests that a warning is given when file is written out."""
    cube = stock.geodetic(shape=(2,2))
    attribution = "This date came from an institution. "
    cube.attributes["attribution"] = attribution
    expected_message="attribution has been written to sidecar file filename.attribution"
    # mocks out the opening of files, so no file is created
    with mock.patch("builtins.open"):
        with pytest.raises(UserWarning, match=expected_message):
            _write_metadata([cube], "filename")

@pytest.mark.filterwarnings("ignore:license has been written to sidecar file /var/tmp/:UserWarning")
def test_multiple_cubes(tmp_path):
    """Test that multiple_cubes with attributes is written out correctly."""
    #creating three cubes with different license attributes
    cube1 = stock.geodetic(shape=(2,2))
    license1 = "This is a cube's license. "
    cube1.attributes["license"] = license1
    cube1.rename("the first cube")
    cube2 = stock.geodetic(shape=(2,2))
    license2 = "This is another cube's license. "
    cube2.attributes["license"] = license2
    cube2.rename("the second cube")
    cube3 = stock.geodetic(shape=(2,2))
    license3 = "This is a third cube's license. "
    cube3.attributes["license"] = license3
    cube3.rename("the third cube")
    cubelist = [cube1, cube2, cube3]
    filename = tmp_path / "multiple_cube_test"
    # The actual test
    _write_metadata(cubelist, filename)
    expected_filename = str(filename) + ".license"
    with open(expected_filename, 'r') as file:
        actual_license = file.read()
    expected_license = "the first cube = This is a cube's license. the second cube = This is another cube's license. the third cube = This is a third cube's license. "
    assert actual_license == expected_license

@pytest.mark.filterwarnings("ignore:license has been written to sidecar file /var/tmp/:UserWarning")
@pytest.mark.filterwarnings("ignore:attribution has been written to sidecar file /var/tmp/:UserWarning")
@pytest.mark.filterwarnings("ignore:restrictions has been written to sidecar file /var/tmp/:UserWarning")
def test_all_different_attributes_written_out(tmp_path):
    """Tests that a cube with a multiple different attributes writes
    out all metadata files."""
    cube = stock.geodetic(shape=(2,2))
    attribution = "This date came from an institution. "
    cube.attributes["attribution"] = attribution
    cube.attributes["restrictions"] = "This data is restricted to be used for testing purposes only."
    cube.attributes["license"] = "This is a license for the data"
    filename = tmp_path / "test_multiple_attributes"
    _write_metadata([cube], filename)
    assert os.path.exists(str(filename)+".attribution")
    assert os.path.exists(str(filename)+".restrictions")
    assert os.path.exists(str(filename)+".license")
