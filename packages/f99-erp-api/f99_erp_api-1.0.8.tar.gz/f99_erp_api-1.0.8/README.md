Hello world

python -m grpc_tools.protoc --proto_path=. ./f99_erp_api.proto --java_out=.
python -m grpc_tools.protoc --proto_path=. ./f99_erp_api.proto --python_out=. --grpc_python_out=.
pip install twine
python setup.py sdist
twine upload dist/*