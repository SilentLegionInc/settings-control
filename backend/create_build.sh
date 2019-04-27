source venv/bin/activate
rm -rf build toolbelt.egg-info deploy
python3 setup.py bdist_wheel -d deploy
rm -rf build toolbelt.egg-info
