def string_to_list(s: str, sep: str = ",") -> list:
    if not s:
        return []

    return [s.strip() for s in (s.strip()).split(sep)]


def get_queryset_filters(data: dict) -> dict:
    return {k: v for k, v in data.items() if v}


