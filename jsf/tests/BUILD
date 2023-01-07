python_sources(name="src")

python_test_utils(
    name="test_utils",
)

files(
    name="test_data", 
    sources=["data/*.json"]
)

python_tests(
    name="pytest",
    dependencies=[":test_data"],
    interpreter_constraints=parametrize(py3=[">=3.7,<4"]),
)
