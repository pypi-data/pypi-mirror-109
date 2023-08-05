from .model_family import ModelFamily


def handle_model_family(model_family):
    """Handles model_family by either returning the ModelFamily or converting from a string

    Arguments:
        model_family (str or ModelFamily): Model type that needs to be handled

    Returns:
        ModelFamily
    """

    if isinstance(model_family, str):
        try:
            tpe = ModelFamily[model_family.upper()]
            return tpe
        except KeyError:
            raise KeyError('Model family \'{}\' does not exist'.format(model_family))
    if isinstance(model_family, ModelFamily):
        return model_family
    raise ValueError('`handle_model_family` was not passed a str or ModelFamily object')
