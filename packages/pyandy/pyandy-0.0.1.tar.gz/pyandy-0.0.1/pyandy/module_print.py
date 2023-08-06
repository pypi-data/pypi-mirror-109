def fprint(text, total_chars=40, fill_chars = "-"):
    total_dashes = (total_chars - len(text))

    if total_dashes % 2 == 0:
        dashes_left = int(total_dashes / 2)
        dashes_right = int(dashes_left)

    else:
        dashes_left = int(total_dashes / 2)
        dashes_right = int(dashes_left + 1)

    print(f'{fill_chars * dashes_left}{text}{fill_chars * dashes_right}')