def make_edge(conversion_graph,labels,values):
    if labels[0] in conversion_graph.keys():
        conversion_graph[labels[0]][labels[1]] = values[1] / values[0] 
    else:
        conversion_graph[labels[0]] = {labels[1]: values[1] / values[0]}
    if labels[1] in conversion_graph.keys():        
        conversion_graph[labels[1]][labels[0]] = values[0] / values[1]
    else:
        conversion_graph[labels[1]] = {labels[0]: values[0] / values[1]}
    return conversion_graph


def load_conversion_graph(conversion_data):
    conversion_graph = {}
    for line in conversion_data.splitlines():
        labels = []
        values = []
        for item in line.strip().split():
            for t in item.split():
                try:
                    values.append(float(t))
                except ValueError:
                    if t != '=':
                        labels.append(t)
        conversion_graph = make_edge(conversion_graph,labels,values)
    return conversion_graph


def bfs(graph, start, end):
    queue = []
    visited = []
    queue.append([start])
    while queue:
        path = queue.pop(0)
        node = path[-1]
        if node == end:
            return path
        for adjacent in graph.get(node, []):
            new_path = list(path)
            if adjacent not in visited:
                visited.append(adjacent)
                new_path.append(adjacent)
                queue.append(new_path)
    print('ERROR: Conversion from',start,'to',end,'is unknown.')
    exit()


def calc_conversion_factor(conversion_graph,path):
    conversion_factor = 1.0
    for i,item in enumerate(path):
        conversion_factor = conversion_factor * conversion_graph[path[i]][path[i+1]]
        if i == len(path) - 2:
            break
    return conversion_factor

def strip_units(s):
    units = s.strip('1234567890./ ').strip().lower()
    amount = s[:len(s) - len(units)].strip()
    if '/' in amount:
        numerator,denominator = amount.split('/')
        amount = float(numerator) / float(denominator)
    else:
        amount = float(amount)
    return amount, units

def explicit_unit_string(amount,units):
    if amount != 1.0:
        units = units + 's'
    if amount.is_integer():
        str_amount = str(int(amount))
    else:
        str_amount = str(amount)
    explicit_value = str_amount + ' ' + units
    return explicit_value

def convert_units(value_w_explicit_units,target_units,conversion_data):
    origin_amount, origin_units = strip_units(value_w_explicit_units)
    
    if target_units[-1] == 's':
        target_units = target_units[:len(target_units) -1]
    if origin_units[-1] == 's':
        origin_units = origin_units[:len(origin_units) -1]

    conversion_graph = load_conversion_graph(conversion_data)
    bfs_path = bfs(conversion_graph,origin_units,target_units)
    conversion_factor = calc_conversion_factor(conversion_graph,bfs_path)
    converted_amount = origin_amount * conversion_factor
    return explicit_unit_string(converted_amount,target_units)


conversion_data = """1 tsp = 1 teaspoon
3 teaspoon = 1 tablespoon
16 tablespoon = 1 cup
2 cup = 1 pint
2 pint = 1 quart
1 cup = 8 fluid_ounce
32 fluid_ounce = 1 quart
4 quart = 1 gallon
1 day = 24 hour
1 hour = 60 min
1 min = 60 second
2.2 lb = 1 kg
1000 g = 1 kg
"""

if __name__ == "__main__":
    origin_values = ['1/64 cups','1 gallon','0.397 lb','1 day']
    target_units = ['tablespoons','tsp','g','seconds']
    for i,origin_value in enumerate(origin_values):
        results = convert_units(origin_value,target_units[i],conversion_data)
        sentence = 'are equal to' if origin_value[-1] == 's' else 'is equal to'
        print(origin_value,sentence,results)
 
