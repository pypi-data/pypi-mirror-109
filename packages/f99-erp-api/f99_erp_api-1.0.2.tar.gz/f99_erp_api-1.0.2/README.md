
python -m grpc_tools.protoc --proto_path=. ./f99_erp_api.proto --python_out=. --grpc_python_out=.

pip install wheel
pip install twine
python setup.py sdist bdist_wheel
twine upload dist/*