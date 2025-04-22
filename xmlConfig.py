import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import xml.etree.ElementTree as ET
import Kocman as K
import removeAmpersand as rmA
from datetime import datetime
from pathlib import Path

#Globals
resultDirectory = "."
fileData = None
root = None

#getSeparator function
#serves to detect whether a given filePath should be split by / or \, depending what system we're on
#filePath parameter is teh filePath we will be splitting
def getSeparator(filePath : str) -> str:

    #check whether the forward slash is present in the filePath
    if "/" in filePath:

        #if it is, we're on a UNIX system
        #set it up as separator to be used later
        return "/"
    
    #otherwise
    #I hope windows does not allow / in fileNames
    else:

        #otherwise we must be on a Windows system
        #set \ up as a separator for later use
        return "\\"

#chooseOutputFolder function
#uses askdirectory from fd to prompt the user to choose which folder they wish to save the result of the script into
def chooseOutputFolder(label : tk.Label) -> None:

    #get resultDirectory from globals
    #we do this, since buttons are not able to return anything unfortunately
    global resultDirectory

    #try except statement to make sure if anything wrong happens, I raise an error
    try:

        #prompt the user to select a directory and catch the output in resultDirectory
        resultDirectory = fd.askdirectory()

        #lastly configure the passed label to make sure the user gets feedback on what happened
        label.config(text = f"Zvolená složka: {Path(resultDirectory).name}", fg = "green")

    #if anything wrong happened during the execution of askdirectory
    except Exception:

        #display an error letting the user know what happened
        #dunno how a user could create this error, I hope they won't
        displayError("Chyba při volbě složky pro výstup, zkuste to prosím znovu", 1)

#writeResult function to handle writing the results of XMLConfigs into files
def writeResult(result) -> int:

    global resultDirectory

    #try attempting to write the file itself, if an error occurs, will jump to except, returning false, sending parent function into an error state, generating an error dialogue
    try:

        #try attempting to write the file character by character, if working with a previously corrupted XML file, it was worked as such, thus we need to write it as such
        try:

            #creating a new file following this naming convention
            #get the organisation this was performed for (option selected from dropDown menu) + -FV- + get month-year from datetime and end with .xml extension
            file = open(resultDirectory + getSeparator(resultDirectory) + selectedOption.get() + "-FV-" + datetime.today().strftime('%m-%Y') + ".xml", "w", encoding = "utf-8")

            #join it to an empty string, just to stringify it back together, since it is a python abomination of a bajillion strings strewn together (because python does not know what a char is)
            #We'll never be modifying regular, workable xml files as raw text anyway, they were probably broken in some way, so this should be fine (will fix if it is not later on)
            result = ''.join(result)

            #write the result string into the file and close it
            file.write(result)
            file.close()

            #return 0, we successfully finished writing the result of our edit
            return 0

        #if an error was encountered while trying to write the file as raw text, input was a valid xml file we edited, meaning we can jump into except and write it via inbuilt functions
        except:

            #using xml.etrees write inbuilt function to write the file
            #naming convention follows this
            #get the organisation this was performed for (option selected from dropDown menu) + -FV- + get month-year from datetime and end with .xml extension
            #using getSeparator function to make sure the resultDirectory and fileName are separated using the correct system separator
            result.write(resultDirectory + getSeparator(resultDirectory) + selectedOption.get() + "-FV-" + datetime.today().strftime('%m-%Y') + ".xml", encoding = "utf-8")

            #writing was succesful, return 0
            return 0
    
    #if all writing failed at any point
    except:

        #return 1 and send the parent function into an error state, generating an error dialogue
        return 1


#displayError function
#taking errorMsg as an argument, so that the caller can specify message to user on error call
def displayError(errorMsg : str, errorCode : int) -> None:

    #create a new tkinter window for the error dialogue
    #title it error and set its size to smaller
    errorWindow = tk.Toplevel(app)
    errorWindow.title = "Error"
    
    #a label within the window, showing the passed error message to the user and pack this label
    label = tk.Label(errorWindow, text = errorMsg + "\nError Code: " + str(errorCode))
    label.pack()

    #errorButton with a simple function to close the error window and return to calling function
    errorButton = ttk.Button(errorWindow, text = "Ok", command = errorWindow.destroy)
    errorButton.pack()

    #finally return back to caller, error resolved
    return

#displaySuccess function
#takes no arguments, serves to give user feedback on an edit of an xml file succeeding
def displaySuccess(changed_lines) -> None:

    #create a new window to display success, se it to appear on top of the original window
    #title it success and set its size to be small
    successWindow = tk.Toplevel(app)
    successWindow.title = "Success"
    
    #a label to display a success message and pack it
    label = tk.Label(successWindow, text = "XML soubor úspěšně zpracován\nUpraveny/odstraněny byly tyto řádky:")
    label.pack()

    text_box_frame = ttk.Frame(successWindow)
    text_box_frame.pack()

    text_box = tk.Text(text_box_frame, height = 15, width = 80, wrap = "none")
    text_box.grid(row = 0, column = 0, sticky = "nsew")

    scrollbar_y = ttk.Scrollbar(text_box_frame, orient = "vertical", command = text_box.yview)
    scrollbar_y.grid(row = 0, column = 1, sticky = "ns")

    scrollbar_x = ttk.Scrollbar(text_box_frame, orient = "horizontal", command = text_box.xview)
    scrollbar_x.grid(row = 1, column = 0, sticky = "ew")

    text_box.configure(yscrollcommand = scrollbar_y.set, xscrollcommand = scrollbar_x.set)

    for i in changed_lines:

        text_box.insert(tk.END, f"{i}\n")

    text_box.config(state = "disabled")

    #successButton to simply close the window
    successButton = ttk.Button(successWindow, text = "OK", command = successWindow.destroy)
    successButton.pack()

    #return back to caller
    return

#invokeScript function
#serves to invoke a certain script depending on which option was selected from the dropDown menu
#so far each organisation has only 1 operation to perform, so we essentially only need to get that org's name and invoke the script belonging to that organisation
def invokeScript(label : tk.Label) -> None:

    #simple switch case to recognise which option was selected
    #currently works on comparing strings a dict could be more efficient
    match selectedOption.get():
        
        #if it's a valid org, get that org's script from imports (different files as modules, so there's no gigaMain)
        #and select which script from the org's file to use (for the future, if we ever need operation selections within orgs, we add another match case)
        case "Radomír Kocman":

            #check whether fileData is an etree
            #if not, this is the incorrect file format
            if type(fileData) is not ET.ElementTree:

                #display an error, letting the user know what happened
                displayError("ERROR při provádění skriptu, zkontrolujte, že jste načetli správný soubor a zvolili odpovídající organizaci prosím", 11)

                #configure the label to let the user know something wrong happened
                label.config(text = "Chyba při provádění skriptu", fg = "red")

                #and return to prevent any errors
                return

            result = K.KocmanScript(root)

            #each script within the org file returns a bool to determine whether it was performed successfully
            if result[0] == 0:

                #if the script went through fine, we attempt a write
                if writeResult(fileData) == 0:
                    
                    #if the write was successful we display a success window
                    displaySuccess(result[1])

                    #configure the passed label to notify the user about the script successfully exiting
                    label.config(text = "Změny úspěšně provedeny", fg = "green")

                #if the write was unsuccessfull, we display an error with the error message telling the user what happened
                else:

                    #display an error, letting the user know something wrong happened
                    displayError("ERROR při zápisu souboru", 21)

                    #configure the passed label to notify the user about the fileWrite erroring out
                    label.config(text = "Chyba při zápisu výsledného souboru", fg = "red")

            #if the script was unsuccessful, we display an error message telling the user what happened
            else:

                #display an error, letting the user know something wrong happened
                displayError("ERROR při provádění skriptu", 31)

                #configure the passed label to notify the user about the script erroring out
                label.config(text = "Chyba při provádění skriptu", fg = "red")

        #if it's a valid org, get that org's script from imports (different files as modules, so there's no gigaMain)
        #and select which script from the org's file to use (for the future, if we ever need operation selections within orgs, we add another match case)
        case "Evropa services Czech":

            #check whether chars is None
            #if it is, do not run the script as there is nothing to be used
            if type(fileData) is not list:

                #display an error, letting the user know what happened
                displayError("ERROR při provádění skriptu, zkontrolujte, že jste načetli správný soubor a zvolili odpovídající organizaci prosím", 12)

                #configure the label to let the user know something wrong happened
                label.config(text = "Chyba při provádění skriptu", fg = "red")

                #return in order to not run anything else and avoid doing anything in the script, since the data are not correctly formatted
                return

            #the function returns a tuple of (success value, changedLines)
            result = rmA.removeAmpersands(fileData)

            #each script within the org file returns an int to determine whether it was performed successfully, 0 for success, other values for errors
            if result[0] == 0:

                #if the script went through fine, we attempt a write
                #write function returns an int to determine success as well, 0 for success, other for errors
                if writeResult(fileData) == 0:

                    #if the write was successful we display a success window
                    #takes changed_lines as an argument to display them as feedback to the user
                    displaySuccess(result[1])

                    #configure the passed label to notify the user about the script successfully exiting
                    label.config(text = "Změny úspěšně provedeny", fg = "green")

                #if the write was unsuccessful, we display an error with the error message telling the user what happened
                else:

                    displayError("ERROR při zápisu souboru", 22)

                    #configure the passed label to notify the user about the fileWrite erroring out
                    label.config(text = "Chyba při zápisu výsledného souboru", fg = "red")

            #if the script was unsuccessful, we display an error message telling the user what happened
            else:

                displayError("ERROR při provádění skriptu", 32)

                #configure the passed label to notify the user about the script erroring out
                label.config(text = "Chyba při provádění skriptu", fg = "red")

        #if we get an org name not within the orgs we know (using the throwaway '_' for that), we tell the user they didn't select an organisation
        case _:

            displayError("Nebyla zvolena žádná organizace!", 2)

    #after all of that is done, return to caller (probably main)
    return
            
#openXML function
#takes no arguments, used to invoke a dialogue window, letting the user choose the location in their computer from which to open the xml file they wish to edit
def openXML(label : tk.Label) -> None:

    #define which file types we use
    #first var of the tuple defines the description of the file
    #second var of the tuple defines the file extensions we accept
    fileTypes = [("XML soubor", ".xml")]

    #generate a dialogue window, which defaults to the location of the script (current working directory)
    #filePath then saves the path to the file to user picked
    filePath = fd.askopenfilename(filetypes = fileTypes, initialdir = os.getcwd())

    #check if filePath is an empty tuple
    #if it is, the user has cancelled the operation above
    if filePath == ():

        #meaning we should return in order to avoid erroring
        return

    #create a global fileData variable
    #since python is not typed, I can do wild things with this and let it be whatever it wants to
    #I do this to make sure the script always keeps only 1 file loaded
    global fileData

    #next, try to open the file with xml.etree since it should be a valid xml file, which we should be able to generate a tree from
    try:

        #set fileData as the parsed file located at filePath picked by the user
        fileData = ET.parse(filePath)

        #create another global variable, root, to contain the root of the generated eTree
        global root

        #eTree.getroot() to get the fileData's root
        root = fileData.getroot()

    #if parsing the file as an xml file fails, we're working with a corrupted xml file and our job is to probably fix it
    except:

        #open the file in readMode
        file = open(filePath, "r", encoding = "utf-8")

        #set chars as an empty field
        fileData = []

        #now read the file line by line
        for line in file:

            #reading each character within that line (don't get fooled, python still does not know what a char is)
            #not sure about variable type of char here, probably still string or a list, if you want to do anything with it treat it as such
            for char in line:

                #append the char to chars
                #what this does is instead of giving us a string which we can't exactly sift through as easily, it gives us an array of individual characters to scan, allowing us to make any changes we wish
                fileData.append(char)

        #after we're done with all that, close the file
        file.close()

    #configure the passed label to make sure the user is notified of the file being loaded successfully
    #it splits the filePath using using getSeparator to find which separator to use and takes the last item from that list, making sure I only show the fileName, not the entire path
    label.config(text = "Soubor " + str(filePath.split(getSeparator(filePath))[-1]) + " úspěšně načten", fg = "green")

#main function for all of this, check if it really is main here
if __name__ == "__main__":

    #padding var serves to define how much padding there should be
    padding = 5

    #create the tk app
    app = tk.Tk()

    loadXMLLabel = tk.Label(text = "Nebyl načten žádný xml soubor", fg = "red")
    loadXMLLabel.grid(row = 0, column = 1, padx = padding, pady = padding, sticky = "E")

    #create the loadXML button, which calls openXML to parse or work with the file
    #since buttons in Tkinter cannot return anything, everything done by openXML is put into global variables (bad solution, need to find a better one)
    loadXMLButton = ttk.Button(text = "Načíst XML", command = lambda: openXML(loadXMLLabel))
    loadXMLButton.grid(row = 0, column = 0, padx = padding, pady = padding, sticky = "W")

    #this is the options list, comprised of strings representing the organisation names
    options = ["Radomír Kocman", "Evropa services Czech"]

    #selectedOption var, used for determining which option was selected (simple as that)
    #default value set to "Vyberte organizace" so the user knows what to do with this
    selectedOption = tk.StringVar()
    selectedOption.set("Vyberte organizaci")

    #now we create the dropdown menu, the way we do this is by providing the selectedOption as the variable to hold info on which option was selected and a pointer to all the options
    dropDown = tk.OptionMenu(app, selectedOption, *options)
    dropDown.grid(row = 1, column = 0, padx = padding, pady = padding, sticky = "W")

    #doneLable represents the label next to the run button
    #it displays whether the xml has been successfuly processed or whether an error occured
    #default value is blank, since there is nothing to display yet
    doneLabel = tk.Label(text = "")
    doneLabel.grid(row = 3, column = 1, padx = padding, pady = padding, sticky = "E")

    #next we create the run button, which calls invoke script and lets the individual organisation scripts work their magic
    doneButton = ttk.Button(text = "Zpracovat XML", command = lambda: invokeScript(doneLabel))
    doneButton.grid(row = 3, column = 0, padx = padding, pady = padding, sticky = "W")

    #saveDirectoryLabel
    #serves to show the user output on whether they have an outputDirectory selected
    #default text tells the user no directory has been selected yet and is red, to make sure the user understands somethin is off
    saveDicrectoryLabel = tk.Label(text = "Nebyla zvolena složka pro výsledek", fg = "red")
    saveDicrectoryLabel.grid(row = 2, column = 1, padx = padding, pady = padding, sticky = "E")

    #saveDirectoryButton
    #lets the user pick a directory into which they wish to write the result of the script
    saveDicrectoryButton = ttk.Button(text = "Zvolte složku pro uložení výsledného souboru", command = lambda: chooseOutputFolder(saveDicrectoryLabel))
    saveDicrectoryButton.grid(row = 2, column = 0, padx = padding, pady = padding, sticky = "W")

    #run the app mainloop
    app.mainloop()