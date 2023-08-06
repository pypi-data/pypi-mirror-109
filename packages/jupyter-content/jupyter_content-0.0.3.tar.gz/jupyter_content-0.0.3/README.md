[![Datalayer](https://raw.githubusercontent.com/datalayer/datalayer/main/res/logo/datalayer-25.svg?sanitize=true)](https://datalayer.io)

# Jupyter Content

## Jupyter Content GCP

```bash
# Install dependencies.
make install
# Get a key.
PROJECT_ID=<YOUR_PROJECT_ID> \
  SERVICE_ACCOUNT=<YOUR_SERVICE_ACCOUNT> \
  make key
# Run the tests.
make test
```

```bash
# Start a jupyterlab example configured with a content bucket.
make jupyterlab-example
```

Initial source code for the Jupyter Content Manager taken from https://github.com/src-d/jgscm under [MIT License](https://github.com/datalayer-externals/jgscm/blob/65ee2fe74d2db05b0873ee9e39af42925fc0ea83/LICENSE.md).

Using Google Storage python library.

- https://googleapis.dev/python/storage/latest/index.html
- https://github.com/googleapis/python-storage

- https://googleapis.dev/python/google-resumable-media/latest/index.html
- https://github.com/googleapis/google-resumable-media-python/latest/index.html
