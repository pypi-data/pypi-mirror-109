import setuptools

setuptools.setup(
    name="easy_detection",
    version="1.0.2",
    author="samonsix",
    author_email="samonsix@163.com",
    description="face detection with out AI framework",
    url="https://github.com/Samonsix",
    packages=setuptools.find_packages(),
    install_requires=["opencv-python>=4.1.1.26", "numpy>=1.19.0", "scikit-image>=0.17.2", "tensorrt==6.0.1.5",
                      "torch2trt-unofficial==0.0.3", "onnx==1.7.0"],
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.onnx', '*.jpg'],
    },
    keywords=('face detection', 'centerface'),
    include_package_data=True,
)
