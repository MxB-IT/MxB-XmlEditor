def remove_ampersands(chars : list) -> int or (int, list):
    """
    removes all raw ampersands within the xml file
    :param chars: file contents in a list containing each char as a single string
    :return: int representing success or failure
    :return: (int, list) tuple, int representing success and the list containing all the changed lines
    """

    try:
        text = ''.join(chars)

        lines = text.splitlines(keepends = True)
        changed_lines = []

        for i, line in enumerate(lines):

            if "&" in line:

                lines[i] = line.replace("&", "+")
                changed_lines.append(line)

        updated_text = ''.join(lines)
        chars.clear()
        chars.extend(updated_text)

        #if everything goes through fine, return True
        return 0, changed_lines

    #if anything weird happens, return false, sending the caller into an error state
    except Exception:

        return 1
