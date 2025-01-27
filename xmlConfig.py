import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import xml.etree.ElementTree as ET
import Kocman as K
import removeAmpersand as rmA
from datetime import datetime

#writeResult function to handle writing the results of XMLConfigs into files
def writeResult(result):

    #try attempting to write the file itself, if an error occurs, will jump to except, returning false, sending parent function into an error state, generating an error dialogue
    try:

        #try attempting to write the file character by character, if working with a previously corrupted XML file, it was worked as such, thus we need to write it as such
        try:

            #creating a new file following this naming convention
            #get the organisation this was performed for (option selected from dropDown menu) + -FV- + get month-year from datetime and end with .xml extension
            file = open(selectedOption.get() + "-FV-" + datetime.today().strftime('%m-%Y') + ".xml", "w", encoding = "utf-8")

            #join it to an empty string, just to stringify it back together, since it is a python abomination of a bajillion strings strewn together (because python does not know what a char is)
            #We'll never be modifying regular, workable xml files as raw text anyway, they were probably broken in some way, so this should be fine (will fix it it is not later on)
            result = ''.join(result)

            #write the result string into the file and close it
            file.write(result)
            file.close()

            #return True, we succesfully finished writing the result of our edit
            return True

        #if an error was encountered while trying to write the file as raw text, input was a valid xml file we edited, meaning we can jump into except and write it via inbuilt functions
        except:

            #using xml.etrees write inbuilt function to write the file
            #naming convention follows this
            #get the organisation this was performed for (option selected from dropDown menu) + -FV- + get month-year from datetime and end with .xml extension
            result.write(selectedOption.get() + "-FV-" + datetime.today().strftime('%m-%Y') + ".xml", encoding = 'utf-8')

            #writing was succesful, return True
            return True
    
    #if all writing failed at any point
    except:

        #return False and send the parent function into an error state, generating an error dialogue
        return False


#displayError function
#taking errorMsg as an argument, so that the caller can specify message to user on error call
def displayError(errorMsg):

    #create a new tkinter window for the error dialogue
    #title it error and set its size to smaller
    errorWindow = tk.Toplevel(app)
    errorWindow.title = "Error"
    errorWindow.geometry("200x200")
    
    #a label within the window, showing the passed error message to the user and pack this label
    label = tk.Label(errorWindow, text = errorMsg)
    label.pack()

    #errorButton with a simple function to close the error window and return to calling function
    errorButton = ttk.Button(errorWindow, text = "Ok", command = errorWindow.destroy)
    errorButton.pack()

    #finally return back to caller, error resolved
    return

#displaySuccess function
#takes no arguments, serves to give user feedback on an edit of an xml file succeeding
def displaySuccess():

    #create a new window to display success, se it to appear on top of the original window
    #title it success and set its size to be small
    successWindow = tk.Toplevel(app)
    successWindow.title = "Success"
    successWindow.geometry("200x200")
    
    #a label to display a success message and pack it
    label = tk.Label(successWindow, text = "XML soubor úspěšně zpracován")
    label.pack()

    #successButton to simply close the window
    successButton = ttk.Button(successWindow, text = "Hurá", command = successWindow.destroy)
    successButton.pack()

    #return back to caller
    return

#invokeScript function
#serves to invoke a certain script depending on which option was selected from the dropDown menu
#so far each organisation has only 1 operation to perform, so we essentially only need to get that org's name and invoke the script belonging to that organisation
def invokeScript():

    #simple switch case to recognise which option was selected
    #currently works on comparing strings a dict could be more efficient
    match selectedOption.get():
        
        #if it's a valid org, get that org's script from imports (different files as modules, so there's no gigaMain)
        #and select which script from the org's file to use (for the future, if we ever need operation selections within orgs, we add another match case)
        case "Radomír Kocman":

            #each script within the org file returns a bool to determine whether it was performed successfully
            if K.KocmanScript(root) == True:

                #if the script went through fine, we attempt a write
                if writeResult(eTree) == True:
                    
                    #if the write was successful we display a success window
                    displaySuccess()

                #if the write was unsuccessfull, we display an error with the error message telling the user what happened
                else:

                    displayError("ERROR pri zapisu souboru")

            #if the script was unsuccessfull, we display an error message telling the user what happened
            else:

                displayError("ERROR pri provadeni skriptu")

        #if it's a valid org, get that org's script from imports (different files as modules, so there's no gigaMain)
        #and select which script from the org's file to use (for the future, if we ever need operation selections within orgs, we add another match case)
        case "Evropa services Czech":

            #each script within the org file returns a bool to determine whether it was performed successfully
            if rmA.removeAmpersands(chars) == True:

                #if the script went through fine, we attempt a write
                if writeResult(chars) == True:

                    #if the write was successful we display a success window
                    displaySuccess()

                #if the write was unsuccessfull, we display an error with the error message telling the user what happened
                else:

                    displayError("ERROR pri zapisu souboru")

            #if the script was unsuccessfull, we display an error message telling the user what happened
            else:

                displayError("ERROR pri provadeni skriptu")

        #if we get an org name not within the orgs we know (using the throwaway '_' for that), we tell the user they didn't select an organisation
        case _:

            displayError("Nebyla zvolena žádná organizace!")

    #after all of that is done, return to caller (probably main)
    return
            
#openXML function
#takes no arguments, used to invoke a dialogue window, letting the user choose the location in their computer from which to open the xml file they wish to edit
def openXML():

    #define which file types we use
    #first var of the tuple defines the description of the file
    #second var of the tuple defines the file extensions we accept
    fileTypes = [("XML soubor", ".xml")]

    #generate a dialogue window, which defaults to the location of the script (current working directory)
    #filePath then saves the path to the file to user picked
    filePath = fd.askopenfilename(filetypes = fileTypes, initialdir = os.getcwd())

    #next, try to open the file with xml.etree since it should be a valid xml file, which we should be able to generate a tree from
    try:
        
        #eTree is global, since it's a bit harder to return values from button presses in Tkinter, will change this in the future
        global eTree

        #set eTree as the parsed file located at filePath picked by the user
        eTree = ET.parse(filePath)

        #create another global variable, root, to contain the root of the generated eTree
        global root
        
        #eTree.getroot() to get the eTree's root
        root = eTree.getroot()

    #if parsing the file as an xml file fails, we're working with a corrupted xml file and our job is to probably fix it
    except:

        #open the file in readMode
        file = open(filePath, "r", encoding = "utf-8")

        #define chars (yes, ironic, since python doesn't know what a char is)
        #chars if global, since button presses in Tkinter cannot return anything
        global chars

        #set chars as an empty field
        chars = []

        #now read the file line by line
        for line in file:

            #reading each character within that line (don't get fooled, python still does not know what a char is)
            #not sure about variable type of char here, probably still string or a list, if you want to do anything with it treat it as such
            for char in line:

                #append the char to chars
                #what this does is instead of giving us a string which we can't exactly sift through as easily, it gives us an array of individual characters to scan, allowing us to make any changes we wish
                chars.append(char)

        #after we're done with all that, close the file
        file.close()

    #display a success message to the user, so they know something actually happened
    fileLoaded = tk.Label(app, text = "Soubor uspesne nacten :)")
    fileLoaded.pack()

#main function for all of this, check if it really is main here
if __name__ == "__main__":

    #create the tk app
    app = tk.Tk()

    #set its geometry to something relatively regular
    app.geometry("300x500")

    #create the loadXML button, which calls openXML to parse or work with the file
    #since buttons in Tkinter cannot return anything, everything done by openXML is put into global variables (bad solution, need to find a better one)
    loadXMLButton = ttk.Button(text = "Načíst XML", command = openXML)
    loadXMLButton.pack()

    #this is the options list, comprised of strings representing the organisation names
    options = ["Radomír Kocman", "Evropa services Czech"]

    #selectedOption var, used for determining which option was selected (simple as that)
    #default value set to "Vyberte organizace" so the user knows what to do with this
    selectedOption = tk.StringVar()
    selectedOption.set("Vyberte organizaci")

    #now we create the dropdown menu, the way we do this is by providing the selectedOption as the variable to hold info on which option was selected and a pointer to all the options
    dropDown = tk.OptionMenu(app, selectedOption, *options)
    dropDown.pack()

    #next we create the run button, which calls invoke script and lets the individual organisation scripts work their magic
    doneButton = ttk.Button(text = "Zpracovat XML", command = invokeScript)
    doneButton.pack()

    app.mainloop()