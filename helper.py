def get_configuration(f = 'config.txt'):
    f = open(f, "r")
    config_dict = {}
    for line in f:
        raw_text = line.split('=')
        config_dict.update({raw_text[0]: raw_text[1][:-1]})
    print(config_dict)
    return config_dict
