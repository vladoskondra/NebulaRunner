import heapq


def dijkstra(graph, start, end):
    # print(f'Start: {start}\nEnd: {end}')
    distances = {vertex: float('infinity') for vertex in graph}
    distances[start] = 0
    previous_vertices = {vertex: None for vertex in graph}
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        if current_distance > distances[current_vertex]:
            continue

        for direction, neighbor in graph[current_vertex].items():
            if neighbor is None:
                continue

            distance = current_distance + 1
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_vertices[neighbor] = current_vertex
                heapq.heappush(priority_queue, (distance, neighbor))

    path = []
    current_vertex = end
    while previous_vertices[current_vertex] is not None:
        previous_vertex = previous_vertices[current_vertex]
        for direction, neighbor in graph[previous_vertex].items():
            if neighbor == current_vertex:
                path.append(direction)
                break
        current_vertex = previous_vertex
    path.reverse()

    path_dirs = []
    for p in path:
        if p == 'NW':
            path_dirs.append('↖️')
        elif p == 'N':
            path_dirs.append('⬆️')
        elif p == 'NE':
            path_dirs.append('↗️')
        elif p == 'W':
            path_dirs.append('⬅️')
        elif p == 'E':
            path_dirs.append('➡️')
        elif p == 'SW':
            path_dirs.append('↙️')
        elif p == 'S':
            path_dirs.append('⬇️')
        elif p == 'SE':
            path_dirs.append('↘️')

    return path_dirs