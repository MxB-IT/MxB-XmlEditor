#removeAmpersands function for Evropa Services Czech
#returns a bool to determine whether the caller goes into an error state or not
def removeAmpersands(chars):

    #since the file we're editing HAS to be corrupted, since it contains ampersands without escape sequences, we automatically go through an array of all the chars that was passed to this function
    for i in range(len(chars)):

        #with each character, set up a try except, in case anything weird happens, to that we catch all errors
        try:

            #if the character is an ampersand
            if chars[i] == "&":

                #replace it with a + sign (yes, they do not want the excape sequence ampersand, I have asked before)
                chars[i] = "+"
        
        #if anything weird happens, return false, sending the caller into an error state
        except:

            return False

    #if everything goes through fine, return True
    return True
