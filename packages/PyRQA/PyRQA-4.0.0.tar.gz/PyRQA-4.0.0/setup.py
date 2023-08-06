from distutils.core import setup
from io import open


with open("README",
          "r",
          encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="PyRQA",
    packages=[
        "pyrqa",
        "pyrqa.operators",
        "pyrqa.operators.create_matrix",
        "pyrqa.operators.create_matrix.radius",
        "pyrqa.operators.detect_diagonal_lines",
        "pyrqa.operators.detect_diagonal_lines.radius",
        "pyrqa.operators.detect_vertical_lines",
        "pyrqa.operators.detect_vertical_lines.radius",
        "pyrqa.variants",
        "pyrqa.variants.rp",
        "pyrqa.variants.rp.radius",
        "pyrqa.variants.rqa",
        "pyrqa.variants.rqa.radius",
    ],
    package_data={
        "pyrqa": [
            "config.ini",
            "kernels/clear_buffer/*.cl",
            "kernels/create_matrix/radius/euclidean_metric/*.cl.mako",
            "kernels/create_matrix/radius/maximum_metric/*.cl.mako",
            "kernels/create_matrix/radius/taxicab_metric/*.cl.mako",
            "kernels/detect_diagonal_lines/*.cl.mako",
            "kernels/detect_diagonal_lines/radius/euclidean_metric/*.cl.mako",
            "kernels/detect_diagonal_lines/radius/maximum_metric/*.cl.mako",
            "kernels/detect_diagonal_lines/radius/taxicab_metric/*.cl.mako",
            "kernels/detect_vertical_lines/*.cl.mako",
            "kernels/detect_vertical_lines/radius/euclidean_metric/*.cl.mako",
            "kernels/detect_vertical_lines/radius/maximum_metric/*.cl.mako",
            "kernels/detect_vertical_lines/radius/taxicab_metric/*.cl.mako",
        ],
    },
    version="4.0.0",
    description="A tool to conduct recurrence analysis in a massively parallel manner using the OpenCL framework.",
    long_description=long_description,
    author="Tobias Rawald",
    author_email="pyrqa@gmx.net",
    keywords=[
        "time series analysis", 
        "recurrence quantification analysis", 
        "RQA",
        "cross recurrence quantification analysis",
        "CRQA",
        "recurrence plot",
        "RP",
        "cross recurrence plot",
        "CRP"
    ],
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    install_requires=[
        'Mako',
        'numpy', 
        'Pillow', 
        'pyopencl', 
        'scipy'
    ],
)