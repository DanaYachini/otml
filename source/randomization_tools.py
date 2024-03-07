
def get_weighted_list(weighted_choices):
    return [value for value, counter in weighted_choices for _ in range(counter)]
