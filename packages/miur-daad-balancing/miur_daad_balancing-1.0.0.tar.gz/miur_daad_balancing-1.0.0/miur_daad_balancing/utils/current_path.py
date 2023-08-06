import os

def current_path()->str:
    """Return absolute path to the root of this package."""
    return "{script_directory}/..".format(
        script_directory=os.path.dirname(os.path.abspath(__file__))
    )