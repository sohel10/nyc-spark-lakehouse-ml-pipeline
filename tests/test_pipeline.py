import os

def test_output_exists():

    assert os.path.exists("outputs"), "Output folder does not exist"


def test_logs_exist():

    assert os.path.exists("logs/pipeline.log"), "Log file missing"