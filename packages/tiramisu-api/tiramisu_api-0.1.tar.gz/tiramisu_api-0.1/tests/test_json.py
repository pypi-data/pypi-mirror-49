# -*- coding: utf-8 -*-
from json import loads
from os import listdir
from os.path import dirname, abspath, join, normpath, splitext
import pytest
# import warnings

# from tiramisu.error import ValueWarning
from tiramisu_api import Config
from tiramisu_api.error import PropertiesOptionError
from tiramisu_api.setting import undefined


# warnings.simplefilter("always", ValueWarning)


def list_data(ext='.json'):
    datadir = join(normpath(dirname(abspath(__file__))), 'data')
    filenames = listdir(datadir)
    filenames.sort()
    ret = []
    for filename in filenames:
        if filename.endswith(ext) and not filename.startswith('__'):
            ret.append(join(datadir, filename))
    return ret


LISTDATA = list_data()


LISTDATA_MOD = []
idx = 0
while True:
    idx += 1
    list_files = list_data('.mod{}'.format(idx))
    if not list_files:
        break
    LISTDATA_MOD.extend(list_files)


@pytest.fixture(params=LISTDATA)
def filename(request):
    return request.param



@pytest.fixture(params=LISTDATA_MOD)
def filename_mod(request):
    return request.param


def error_to_str(dico):
    for key, value in dico.items():
        if isinstance(value, list):
            for idx, val in enumerate(value):
                if (isinstance(val, str) and (val.startswith('cannot access to') or val.startswith('ne peut accéder'))) or isinstance(val, PropertiesOptionError):
                    dico[key][idx] = "PropertiesOptionError"
    return dico


# config.option().value.dict()
def test_dict(filename):
    debug = False
    # debug = True
    if debug:
        print('test_jsons', filename)
    with open(filename, 'r') as fh:
        json = loads(fh.read())
    #
    config = Config(json)
    with open(filename[:-4] + 'dict', 'r') as fh:
        dico = loads(fh.read())

    if debug:
        from pprint import pprint
        pprint(dico)
        print('-----')
        pprint(config.value.dict())
    assert error_to_str(dico) == error_to_str(config.value.dict())


# config.option().value.get()
def test_get(filename):
    debug = False
    # debug = True
    if debug:
        print(filename)
    with open(filename, 'r') as fh:
        json = loads(fh.read())
    config = Config(json)
    with open(filename[:-4] + 'dict', 'r') as fh:
        dico = error_to_str(loads(fh.read()))
        for key, value in dico.items():
            if config.option(key).option.isleader():
                leader_len = len(value)
            if config.option(key).option.isfollower():
                values = []
                for index in range(leader_len):
                    if debug:
                        print('  ', key, index, value)
                    try:
                        val = config.option(key, index).value.get()
                    except PropertiesOptionError:
                        val = "PropertiesOptionError"
                    values.append(val)
                assert value == values
            else:
                assert value == config.option(key).value.get()


# config.option().owner.get()
def test_owner(filename):
    debug = False
    # debug = True
    if debug:
        print(filename)
    with open(filename, 'r') as fh:
        json = loads(fh.read())
    config = Config(json)
    with open(filename[:-4] + 'owner', 'r') as fh:
        dico = loads(fh.read())
        for key, value in dico.items():
            if debug:
                print('key', key)
            if config.option(key).option.isleader():
                leader_len = len(config.option(key).value.get())
            if config.option(key).option.isfollower():
                values = {}
                for index in range(leader_len):
                    try:
                        values[str(index)] = config.option(key, index).owner.get()
                    except PropertiesOptionError:
                        pass
                if debug:
                    print(value)
                    print('------------------')
                    print(values)
                assert value == values
            else:
                if debug:
                    print(value)
                    print('------------------')
                    print({'null': config.option(key).owner.get()})
                assert value == {'null': config.option(key).owner.get()}


# config.option().property.get()
def test_prop(filename):
    debug = False
    # debug = True
    if debug:
        print(filename)
    with open(filename, 'r') as fh:
        json = loads(fh.read())
    config = Config(json)
    with open(filename[:-4] + 'prop', 'r') as fh:
        dico = loads(fh.read())
        for key, value in dico.items():
            if debug:
                print('key', key)
            for key_, val in value.items():
                value[key_] = set(val)
            if config.option(key).option.isleader():
                leader_len = len(config.option(key).value.get())
            if config.option(key).option.isfollower():
                props = {}
                for index in range(leader_len):
                    try:
                        props[str(index)] = set(config.option(key, index).property.get())
                    except PropertiesOptionError:
                        pass
                    if 'clearable' in props[str(index)]: 
                        props[str(index)].remove('clearable') 
            else:
                props = {'null': set(config.option(key).property.get())}
                if 'clearable' in props['null']: 
                    props['null'].remove('clearable') 
            assert value == props


# config.option().property.get(True)
def test_prop2(filename):
    debug = False
    # debug = True
    if debug:
        print(filename)
    with open(filename, 'r') as fh:
        json = loads(fh.read())
    config = Config(json)
    with open(filename[:-4] + 'prop2', 'r') as fh:
        dico = loads(fh.read())
        for key, value in dico.items():
            if debug:
                print('key', key)
            for key_, val in value.items():
                value[key_] = set(val)
            if config.option(key).option.isleader():
                leader_len = len(config.option(key).value.get())
            if config.option(key).option.isfollower():
                props = {}
                for index in range(leader_len):
                    try:
                        props[str(index)] = set(config.option(key, index).property.get(True))
                    except PropertiesOptionError:
                        pass
                    if 'clearable' in props[str(index)]: 
                        props[str(index)].remove('clearable') 
            else:
                props = {'null': set(config.option(key).property.get(True))}
                if 'clearable' in props['null']: 
                    props['null'].remove('clearable') 
            assert value == props


def test_info(filename):
    debug = False
    # debug = True
    with open(filename, 'r') as fh:
        json = loads(fh.read())
    config = Config(json)
    with open(filename[:-4] + 'info', 'r') as fh:
        dico = loads(fh.read())
        if debug:
            from pprint import pprint
            pprint(json)
            print('-------------------')
            pprint(dico)

        for key, values in dico.items():
            for info, value in values.items():
                assert getattr(config.option(key).option, info)() == value, 'error for {} info {} in {}'.format(key, info, filename)


def test_mod(filename_mod):
    debug = False
    # debug = True
    i = int(filename_mod[-1])
    if debug:
        print('test_mod', filename_mod)
    with open(filename_mod[:-4] + 'json', 'r') as fh:
        json = loads(fh.read())
    #
    if debug:
        from pprint import pprint
        pprint(json)
    config = Config(json)
    with open(filename_mod) as fh:
        mod = loads(fh.read())
    if debug:
        print(mod['cmd'])
    if isinstance(mod['cmd'], list):
        for cmd in mod['cmd']:
            eval(cmd)
    else:
        eval(mod['cmd'])
    #
    if debug:
        from pprint import pprint
        pprint(config.updates)
        print('----------------')
        pprint(mod['body']['updates'])
    assert config.updates == mod['body']['updates']
    
    with open(filename_mod[:-4] + 'dict{}'.format(i), 'r') as fh:
        dico1 = loads(fh.read())
    if debug:
        from pprint import pprint
        pprint(dico1)
        print('----------------')
        pprint(config.value.dict())
    assert dico1 == config.value.dict()


def test_mod2(filename_mod):
    debug = False
    # debug = True
    i = int(filename_mod[-1])
    if debug:
        print('test_mod', filename_mod)
    with open(filename_mod[:-4] + 'json', 'r') as fh:
        json = loads(fh.read())
    #
    config = Config(json)
    #
    with open(filename_mod[:-4] + 'updates{}'.format(i), 'r') as fh:
        data = loads(fh.read())
        config.updates_data(data)
    with open(filename_mod[:-4] + 'dict{}'.format(i), 'r') as fh:
        dico1 = loads(fh.read())
    if debug:
        from pprint import pprint
        pprint(dico1)
        print('----------------')
        pprint(config.value.dict())
    assert dico1 == config.value.dict()
