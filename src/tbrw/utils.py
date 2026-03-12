def validate_probability(p: float | list[float]) -> float | list[float]:
    """Validate and normalize the growth probability parameter."""
    if isinstance(p, (float, int)):
        if not (0 <= p <= 1):
            raise ValueError(f"When a number, p must be between 0 and 1. Provided p={p}")
        return float(p)

    if isinstance(p, list):
        if not p:
            raise ValueError("p cannot be an empty list.")

        values: list[float] = []
        for value in p:
            if not isinstance(value, (float, int)) or not (0 <= float(value) <= 1):
                raise ValueError(
                    "each value in p must be a number between 0 and 1. "
                    f"Found {value!r}"
                )
            values.append(float(value))
        return values

    raise TypeError("p must be either a float or a list of float between 0 and 1")