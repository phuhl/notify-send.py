from setuptools import setup
# you may need setuptools instead of distutils

setup(
    # basic stuff here
    name = "notify-send.py",
    version = "1.2.0",
    author = "Philipp Uhl",
    author_email = "git@ph-uhl.com",
    description = "Send desktop notifications.",
    license = "MIT",
    url = "https://github.com/phuhl/notify-send.py",
    scripts = [
        'scripts/notify-send.py'
    ]
)
