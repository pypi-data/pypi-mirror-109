import setuptools


setuptools.setup(
    name="cajtw",
    version="0.0.1",
    author="@ajtwBot",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=[
        "pyrogram==1.2.6",
        "tgcrypto==1.2.2"
    ]
)

