# conftest.py — put core/tools on sys.path and register the network marker for video tests
import sys, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "network: hits real network/models; excluded from verify:fast")
