from utils.retention import calculate_retention
from utils.linkgenerate import generate_link


class TestRetention:
    def test_max_filesize(self):
        assert calculate_retention(file_size=256, min_age=30, max_age=90,
                                   max_size=256) == 30

    def test_min_filesize(self):
        assert calculate_retention(file_size=0, min_age=30, max_age=90,
                                   max_size=256) == 90

    def test_too_big_filesize(self):
        assert calculate_retention(file_size=1000, min_age=30, max_age=90,
                                   max_size=256) == -1
