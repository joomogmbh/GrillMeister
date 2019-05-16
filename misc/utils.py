bratwurstPreis = 1.0
schinkengrillerPreis = 1.5

def getOrderPrice(req_key, req_values):
    result = {}
    for order in req_values:
        resultV = 0.0
        # TODO Keys verwenden, nicht einfach von Reihenfolge ausgehen!!
        resultV = resultV + (order[2] * bratwurstPreis) + (order[3] * schinkengrillerPreis)
        result[order[1]] = resultV
    return result       

def getEventPrice(req_key, req_values):
    result = 0.0
    for order in req_values:
        # TODO Keys verwenden, nicht einfach von Reihenfolge ausgehen!!
        result = result + (order[2] * bratwurstPreis) + (order[3] * schinkengrillerPreis)
    return result
