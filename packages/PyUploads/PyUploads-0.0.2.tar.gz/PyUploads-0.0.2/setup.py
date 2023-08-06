from setuptools import setup, find_packages


longdesc = '''
# PyUploads
A python wrapper for uploading information to websites such as `throwbin.io`

## Installation
You can either install the module via PyPi or directly from the GitHub Repository. If you want to download via `pip` / `PyPi` execute the following command:
```bash
pip[3] install PyUploads
```

## Example Usage
```bash
import PyUploads

try:
    print(
        PyUploads.Throwbin.Create(
            'Paste Title', 
            'Paste Content'
        )
    )
except PyUploads.CreationError:
    print('Failed to Upload')
```'''

VERSION = '0.0.2' 

# Setting up
setup(
        name="PyUploads", 
        version=VERSION,
        author="Gowixx",
        author_email="<notgowixxmen@protonmail.ch>",
        description='Wrapper for websites such as throwbinio',
        long_description=longdesc,
        long_description_content_type = 'text/markdown',
        packages=find_packages(),
        install_requires=['requests'],
        
        keywords=[
            'python', 
            'throwbin', 
            'pythrowbin', 
            'python throwbin',
            'throwbin.io',
            'python uploads',
            'pyuploads'
        ],
        classifiers=[
        ]
)