CATEGORICAL_ATTR = 'c'
NUMERICAL_ATTR = 'n'
BINARY_ATTR = 'b'

TYPE_MAP = {
    CATEGORICAL_ATTR: lambda x: x,
    NUMERICAL_ATTR: lambda x: float(x),
    BINARY_ATTR: lambda x: True if x == '1' or x == 1.0 else False
}
