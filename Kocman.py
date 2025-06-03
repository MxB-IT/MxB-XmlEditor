import xml.etree.ElementTree as ET

def kocman_script(e_tree : ET.ElementTree) -> int or (int, list):
    """
    removes the elements needed to be removed for the Kocman org specifically
    :param e_tree: element tree representation of the input xml file
    :return: int, representing either success or failure
    :return: (int, list) tuple, int representing success and the list containing all the changed elements
    """

    removed_elements = []

    #since we are removing certain elements in this function from an xml we know is alright, we automatically use the etree extension
    #we iterate through all the eTree elements
    for element in e_tree.iter():

        #for each child of an element
        for child in element:

            #we check whether its tag corresponds to the ones we need to get rid of
            if child.tag == "SklPolozka" or child.tag == "Stredisko":

                #if it does, we set up a try except, to detect error states
                try:

                    removed_xml = ET.tostring(child, encoding="unicode").strip()
                    removed_elements.append((element.tag, child.tag, removed_xml))

                    #clear and remove the child
                    child.clear()
                    element.remove(child)

                #if an error occurs during child deletion, return false, sending the caller into an error state
                except Exception:

                    return 1

    #if everything went through ok, return True, let the caller move on
    return 0, removed_elements