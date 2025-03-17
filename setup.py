from setuptools import setup, find_packages

setup(
    name="matrix-term",
    version="1.0.0",
    description="A terminal-based Matrix-style digital rain animation",
    author="Juan Villada",
    author_email="YOUR_EMAIL",
    url="https://github.com/juanvillada/matrix-term",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "matrix-term=matrix_rain:main_wrapper",
        ],
    },
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console :: Curses",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Artistic Software",
    ],
)
