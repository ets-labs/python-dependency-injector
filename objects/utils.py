"""Utils module."""


def is_provider(instance):
    """Check if instance is provider instance."""
    return hasattr(instance, '__IS_OBJECTS_PROVIDER__')


def is_injection(instance):
    """Check if instance is injection instance."""
    return hasattr(instance, '__IS_OBJECTS_INJECTION__')


def is_init_arg_injection(instance):
    """Check if instance is init arg injection instance."""
    return hasattr(instance, '__IS_OBJECTS_INIT_ARG_INJECTION__')


def is_attribute_injection(instance):
    """Check if instance is attribute injection instance."""
    return hasattr(instance, '__IS_OBJECTS_ATTRIBUTE_INJECTION__')


def is_method_injection(instance):
    """Check if instance is method injection instance."""
    return hasattr(instance, '__IS_OBJECTS_METHOD_INJECTION__')
