from json import loads
from tiramisu_api import Config


def test_list_option():
    filename = 'tests/data/boolean1.json'
    with open(filename, 'r') as fh:
        json = loads(fh.read())
    #
    config = Config(json)
    opts = []
    for option in config.option.list():
        opts.append(option.option.name())
    assert opts == []
    #
    opts = []
    for option in config.option('options').list():
        opts.append(option.option.name())
    assert opts == ['boolean']


def test_list_optiondescription():
    filename = 'tests/data/boolean1.json'
    with open(filename, 'r') as fh:
        json = loads(fh.read())
    #
    config = Config(json)
    opts = []
    for option in config.option.list('optiondescription'):
        opts.append(option.option.name())
    assert opts == ['options']
    #
    opts = []
    for option in config.option('options').list('optiondescription'):
        opts.append(option.option.name())
    assert opts == []


def test_list_all():
    filename = 'tests/data/boolean1.json'
    with open(filename, 'r') as fh:
        json = loads(fh.read())
    #
    config = Config(json)
    opts = []
    for option in config.option.list('all'):
        opts.append(option.option.name())
    assert opts == ['options']
    #
    opts = []
    for option in config.option('options').list('all'):
        opts.append(option.option.name())
    assert opts == ['boolean']
