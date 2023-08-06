python3 setup.py bdist_wheel
python3 setup.py sdist
sudo rm -r dist/*
python3 setup.py bdist_wheel sdist
pytest tests.py
