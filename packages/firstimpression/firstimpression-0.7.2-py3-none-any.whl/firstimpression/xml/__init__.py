
def get_text_from_element(element, tag_name):
    return element.find(tag_name).text


def get_items_from_element(element, tag_name):
    return element.findall(tag_name)


def get_attrib_from_element(element, tag_name, attrib_name):
    return element.find(tag_name).attrib[attrib_name]
