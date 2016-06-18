import xone


def create_instance(c_instance):
    reload(xone)
    return xone.XoneK2(c_instance)
