def flatten_extend(matrix):
    flat_list = []
    for row in matrix:
        flat_list.extend(row)
    return flat_list


def boolean_emojis(bool_emoji):
    emoji = '✅' if bool_emoji else '❌'
    return emoji
