import os

# Variables are handled as a mapping from name to value. In addition to
# the basic mapping, it is possible to supplement variable definitions from
# a variety of places:
#
#   - The environment, in the form PREFIX_NAME
#       The prefix can be specified, environment variables should be all
#       uppercase, and the resulting name will be lowercase
#   - An ini-style configuration file
#       The name of the section to be used can be specified
#   - Prompting the user
#       In this case, a list of (name, prompt, default) values should be
#       provided

# Usage:
#   varspec = [...]
#   variables = {...}
#   cp = ConfigParser()
#   cp.read("myinifile.ini")
#   variables = ChainMap(variables, env_values("GEN"), cp["varsection"])
#   prompt_for_missing(variables, varspec)

def env_values(prefix):
    """A dictionary of values from the environment.
    
    Only environment variables starting with PREFIX_ are selected, where
    PREFIX is forced to uppercase. The keys are formed from the rest of the
    environment variable name, converted to lowercase.
    """
    prefix = prefix.upper() + '_'
    l = len(prefix)
    result = {}
    for name, value in os.environ:
        if name.startswith(prefix):
            name = name[l:].lower()
            result[name] = value
    return result

def prompt_for_missing(dictionary, variables, promptfn):
    """Prompt for any variables missing from DICTIONARY.

    The VARIABLES should be a list of (name, prompt, default) tuples.
    The user will be prompted for a value for any names that are not already
    present in the DICTIONARY.

    PROMPTFN is the function to use to prompt for a value. Typically this
    will be click.prompt, but by factoring it out, we can avoid a dependency
    on click in this file.
    """
    for name, prompt, default in variables:
        if name not in dictionary:
        dictionary[name] = promptfn(prompt, default=default)
