from setuptools import setup

setup(
    name="Pneumonia detections",
    version="0.1",
    python_requires='==3.12.5',  # Specify the required Python version
    install_requires=[
        'tensorflow==2.18.0',
        'flask==3.0.3',
        # other dependencies
    ],
)
