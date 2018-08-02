import pydash as _


def zip_by_keys(dicts, default_value=None):
    all_keys = _.chain(dicts).flat_map(lambda d: list(d.keys())).uniq().value()
    # ^ это эквивалентно вот этому:
    # all_keys = _.flat_map(dicts, lambda d: list(d.keys()))
    # all_keys = _.uniq(all_keys)

    values = _.map_(all_keys, lambda key: _.invoke_map(dicts, 'get', key, default_value))
    return _.zip_object(all_keys, values)