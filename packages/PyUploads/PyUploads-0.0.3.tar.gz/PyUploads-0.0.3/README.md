# PyUploads
A python wrapper for uploading information to websites such as `throwbin.io`

## Installation
You can either install the module via PyPi or directly from the GitHub Repository. If you want to download via `pip` / `PyPi` execute the following command:
```bash
pip[3] install PyUploads
```

## Example Usage
```python
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
```