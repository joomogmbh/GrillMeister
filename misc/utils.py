bratwurstPreis = 1.0
schinkengrillerPreis = 1.5

def getOrderPrize():
    result = {}
    for order in req_values:
        resultV = 0.0
        resultV = resultV + (order[2] * bratwurstPreis) + (order[3] * schinkengrillerPreis)
        result[order[1]] = resultV
    return result       

def getEventPrize():
    result = 0.0
    for order in req_values:
        result = result + (order[2] * bratwurstPreis) + (order[3] * schinkengrillerPreis)
    return result
