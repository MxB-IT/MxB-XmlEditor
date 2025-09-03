def remove_ampersands(chars : list) -> int or (int, list):
    """
    removes all raw ampersands within the xml file
    :param chars: file contents in a list containing each char as a single string
    :return: (int, list) tuple, int representing success and the list containing all the changed lines
    """

    invoice_counter = 0
    try:
        text = ''.join(chars)

        lines = text.splitlines(keepends = True)

        for i, line in enumerate(lines):

            if '<inv:invoice version="2.0">' in line:
                invoice_counter += 1
                print(line)

            if "&" in line:

                lines[i] = line.replace("&", "+")

        updated_text = ''.join(lines)
        chars.clear()
        chars.extend(updated_text)

        #if everything goes through fine, return True
        return 0, invoice_counter

    #if anything weird happens, return false, sending the caller into an error state
    except Exception:

        return 1, invoice_counter
