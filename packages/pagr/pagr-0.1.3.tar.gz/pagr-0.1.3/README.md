# pagr - the Python Aggregator
**THIS IS NOT INTENDED FOR ANY USE**

## Run your yaml
`python -m pagr.runner config.yaml`

## Development
### Upload to pip
1. Make sure that the version number has been updated
1. Generate dist files `python setup.py sdist bdist_wheel`
2. Upload to PyPI `twine upload dist/*`

## Docker
1. `docker build -t pagr-test:latest .`
1. `docker run pagr-test:latest`
1. `docker tag pagr-test:latest defreng-virtual-k8s:30500/pagr-test:latest`
1. `docker push defreng-virtual-k8s:30500/pagr-test:latest`
