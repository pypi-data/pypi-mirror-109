from setuptools import setup, find_packages
setup(
    name='nlp_nn',
    version='0.0.11.0',
    description='NLP NN Framework',
    long_description='NLP NN Framework',
    long_description_content_type="text/markdown",
    author='fubo',
    author_email='fb_linux@163.com',
    url='https://gitee.com/fubo_linux/nlp_nn',
    packages=find_packages(where='.', exclude=(), include=('*',)),
    package_data={
        "nlp_nn": [
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'rouge',
        'seqeval',
        'sklearn',
        'torch>=1.6',
        'fastapi>=0.55.1',
        'pydantic>=1.5.1',
        'tensorboard>=2.2.1',
        'transformers==4.5.1',
        'jieba>=0.39',
        'uvicorn>=0.13.4',
        'fastapi>=0.63.0',
        'typing'
    ],
    python_requires='>=3.6'
)
