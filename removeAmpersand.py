#removeAmpersands function for Evropa Services Czech
#returns a bool to determine whether the caller goes into an error state or not
def removeAmpersands(chars):

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
