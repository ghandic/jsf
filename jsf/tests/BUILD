python_test_utils(
    name="test_utils",
)

files(name="tests", sources=["data/*.json", "*.py"])

python_tests(
    name="pytest",
    dependencies=[":tests"],
    interpreter_constraints=parametrize(py3=[">=3.8,<4"]),
)
