def str_to_dict(string):
    return {neirong.split(':')[0].strip():neirong.split(':')[1].strip() for neirong in str(string).split('\n') if neirong }