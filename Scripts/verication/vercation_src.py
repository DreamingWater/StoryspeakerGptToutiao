# Lenovo-"Xie Yan"

def get_uuid_from_img(img_str):
    import re
    pattern = r'uuid=(.*?)&'
    re_compile = re.search(pattern, img_str)
    if re_compile is not None:
        return re_compile.group(1)
    else:
        print('A error in get uuid...')
        return None

