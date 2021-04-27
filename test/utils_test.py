"""Tests for utility functions."""
from utils.retention import calculate_retention


class TestRetention:
    """Tests for the retention time of files."""
    def test_max_filesize(self):
        """Test retention time with the largest size of file."""
        assert calculate_retention(file_size=256, min_age=30, max_age=90,
                                   max_size=256) == 30

    def test_min_filesize(self):
        """Test retention time with the smallest size of file."""
        assert calculate_retention(file_size=0, min_age=30, max_age=90,
                                   max_size=256) == 90

    def test_too_big_filesize(self):
        """Test retention time with a file that is too large."""
        assert calculate_retention(file_size=1000, min_age=30, max_age=90,
                                   max_size=256) == -1
