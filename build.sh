rm -r dist build

python3 -m build && \
python3 setup.py install && \
python3 -m twine upload  dist/*
