"""Tests for the retention calculation function."""

from utils.retention import calculate
import config


def test_retention_max_filesize():
    """Test the retention calculation function with the highest filesize."""
    assert calculate(file_size=config.UPLOAD_MAX_SIZE) == config.UPLOAD_MIN_AGE


def test_retention_min_filesize():
    """Test the retention calculation function with the lowest filesize."""
    assert calculate(file_size=0) == config.UPLOAD_MAX_AGE


def test_retention_big_filesize():
    """Test the retention calculation function with a bigger filesize."""
    assert calculate(file_size=config.UPLOAD_MAX_SIZE * 2) == -1
