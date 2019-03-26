def descendingBy(columns, data, sortColumn):
    for index in range(1, len(data)):
        currentRow = data[index]
        position = index
        while position > 0 and int(data[position - 1][columns[sortColumn]]) < int(currentRow[columns[sortColumn]]):
            data[position] = data[position-1]
            position -= 1
        data[position] = currentRow
    return data

def ascendingBy(columns, data, sortColumn):
    for index in range(1, len(data)):
        currentRow = data[index]
        position = index
        while position > 0 and int(data[position - 1][columns[sortColumn]]) > int(currentRow[columns[sortColumn]]):
            data[position] = data[position-1]
            position -= 1
        data[position] = currentRow
    return data

def isMismatched(val1, val2, asc):
    return (not(val1 > val2) and asc) or ((val1 > val2) and not asc)