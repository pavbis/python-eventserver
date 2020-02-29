from configparser import ConfigParser


class InvalidConfigSection(ValueError):
    """Throw this when section does not exist in config file."""


def config(file: str, section: str) -> {}:
    parser = ConfigParser()
    parser.read(file)

    configuration = {}

    if parser.has_section(section):
        parameters = parser.items(section)
        for parameter in parameters:
            configuration[parameter[0]] = parameter[1]

    else:
        raise InvalidConfigSection('Section {0} not found in the {1} file'.format(section, file))

    return configuration
