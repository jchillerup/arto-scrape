def make_payload_from_dom(dom):
    payload = {}
    
    for inputField in dom.xpath('.//input'):
        payload[inputField.name] = inputField.value

    return payload
