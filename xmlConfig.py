import os
import threading
from datetime import *

from pywin.Demos import progressbar

from Widgets.ComboBoxBase import *
from Utils.ErrorHandler import *
from Utils.SuccessHandler import *
from xml.etree import ElementTree
from Scripts.Kocman import *
from Scripts.removeAmpersand import *
from Widgets.ProgressBar import *

class XmlConfig(CTk):
    def __init__(self):
        super().__init__()

        org_options = ["Evropa services Czech",
                       "Radomír Kocman"]

        self.file_data = None
        self.output_directory = os.getcwd()

        self.title("XML Config")
        self.frame = FrameBase(master=self)

        self.widgets = list()

        self.load_xml = (ButtonBase(master=self.frame,
                                    command=self.open_xml,
                                    text="Načíst XML"),
                         LabelBase(master=self.frame,
                                   text ="Nebyl načten žádný xml soubor",
                                   text_color ="red"))
        self.widgets.append(self.load_xml)
        self.drop_down = (ComboBoxBase(master=self.frame,
                                       values=org_options),
                          LabelBase(master=self.frame,
                                    text=""))
        self.drop_down[0].configure(width=self.drop_down[0].cget('font').measure(self.get_longest(org_options)) + 45)
        self.widgets.append(self.drop_down)
        self.output_directory_widgets = (ButtonBase(master=self.frame,
                                                    command=self.choose_output_folder,
                                                    text="Zvolit složku pro uložení výsledného souboru"),
                                         LabelBase(master=self.frame,
                                                   text=f"Složka pro uložení výsledného souboru: {str(self.output_directory.split(self.get_separator(self.output_directory))[-1])}",
                                                   text_color ="green"))
        self.widgets.append(self.output_directory_widgets)
        self.invoker = (ButtonBase(master=self.frame,
                                   command=self.threaded_invocation,
                                   text="Zpracovat XML"),
                        LabelBase(master=self.frame,
                                  text=""))
        self.widgets.append(self.invoker)

        self.frame_setup()

        self.arrange_widgets(self.frame, self.widgets)

        self.progressbar = ProgressBarBase(master=self.frame,
                                           mode="indeterminate")

    @staticmethod
    def get_longest(arr : Iterable) -> Any:
        """
        looks through the provided array and returns the item with the longest length
        :param arr: iterable to look through
        :return: item from iterable
        """
        max_len=max(len(item) for item in arr)
        for item in arr:
            if len(item) == max_len:
                return item
        return 'm'

    def frame_setup(self):
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    @staticmethod
    def arrange_widgets(master : CTkFrame, widgets : List[Tuple[Widget, Widget]]) -> None:
        """
        arranges widgets into a grid layout within the master parameter
        :param master: the master widget within which to arrange all the child widgets
        :param widgets: list of all child widgets, expected to be arranged into a list of tuples, where each list item
                        represents a row and each tuple item represents a column within the grid
        :return: None
        """
        for i, row in enumerate(widgets):
            for j, widget in enumerate(row):
                widget.grid(row=i,
                            column=j,
                            padx = 10,
                            pady = 10)
                master.columnconfigure(j, weight=1)
            master.rowconfigure(i, weight=1)

    def open_xml(self) -> None:
        """
        handles the user choice of input, letting the user open a xml file they wish to edit
        :return: None
        """
        file_types = [("XML soubor", "*.xml")]
        file_path = filedialog.askopenfilename(filetypes=file_types,
                                               initialdir=os.getcwd())
        if file_path == ():
            return

        try:
            try:
                self.file_data = ElementTree.parse(file_path)

            except:

                file = open(file_path,
                            "r",
                            encoding="utf-8")

                lines = [line for line in file]
                self.file_data = [char for char in lines]
                file.close()

        except FileNotFoundError:
            ErrorHandler(error_message="Chyba při načítání vstupního souboru",
                         error_code=3).lift()
            return

        self.load_xml[1].configure(text = f"Soubor {str(file_path.split(self.get_separator(file_path))[-1])} úspěšně načten",
                                   text_color="green")

    @staticmethod
    def get_separator(file_path: str) -> str:
        """
        gets the file separator valid for the OS ('/' for unix or '\' for Windows)
        :param file_path: filepath to be analyzed
        :return: str representing the file separator present within the filepath
        """
        if "/" in file_path:
            return "/"
        else:
            return "\\"

    def choose_output_folder(self):
        """
        handles the output folder selection
        :return: None
        """
        try:
            output_directory = filedialog.askdirectory(initialdir=os.getcwd())

            if output_directory == "":
                return

            self.output_directory = output_directory
            self.output_directory_widgets[1].configure(text=f"Složka pro uložení výsledného souboru: {str(self.output_directory.split(self.get_separator(self.output_directory))[-1])}",
                                                       text_color="green")

        except FileNotFoundError:
            ErrorHandler(error_message="Chyba při načítání výstupní složky",
                         error_code=2).lift()
            self.output_directory_widgets[1].configure(text=f"Chyba při načítání výstupní složky",
                                                       text_color="red")
            return

    def threaded_invocation(self):
        if self.output_directory is None:
            ErrorHandler(error_message="Nebyla zvolena složka pro výstup",
                         error_code=3).lift()
            return

        self.invoker[1].configure(text="")
        self.update_idletasks()
        self.progressbar.grid(row=self.invoker[1].grid_info()['row'],
                         column=self.invoker[1].grid_info()['column'])
        progressbar_thread = threading.Thread(target=CTkProgressBar.start,
                                              args=(self.progressbar,))
        progressbar_thread.start()

        script_thread=threading.Thread(target=self.invoke_script)
        script_thread.start()

    def invoke_script(self):
        match self.drop_down[0].get():
            case "Radomír Kocman":
                if type(self.file_data) is not ElementTree.ElementTree:
                    ErrorHandler(master=self,
                                 error_message="Chyba při provádění skriptu, zkontrolujte, že jste načetli správný soubor a zvolili správnou organizaci",
                                 error_code=4).lift()
                    self.invoker[1].configure(text="Chyba při provádění skriptu",
                                              text_color="red")
                    self.progressbar.stop()
                    self.progressbar.grid_forget()
                    return
                result = kocman_script(self.file_data.getroot())
                if result[0] == 0:
                    if self.write_result(self.file_data) == 0:
                        SuccessHandler(result[1]).lift()
                        self.invoker[1].configure(text="Změny úspěšně provedeny",
                                                  text_color = "green")
                else:
                    ErrorHandler(master=self,
                                 error_message="Chyba při zápisu souboru",
                                 error_code=22).lift()
                    self.invoker[1].configure(text="Chyba při zápisu souboru",
                                              text_color="red")
            case "Evropa services Czech":
                if type(self.file_data) is not list:
                    ErrorHandler(master=self,
                                 error_message="Chyba při provádění skriptu, zkontrolujte, že jste načetli správný soubor a zvolili správnou organizaci",
                                 error_code=4).lift()
                    self.invoker[1].configure(text="Chyba při provádění skriptu",
                                              text_color="red")
                    self.progressbar.stop()
                    self.progressbar.grid_forget()
                    return
                result=remove_ampersands(self.file_data)
                if result[0] == 0:
                    if self.write_result(self.file_data) == 0:
                        SuccessHandler(result[1]).lift()
                        self.invoker[1].configure(text="Změny úspěšně provedeny",
                                                  text_color="green")
                    else:
                        ErrorHandler(master=self,
                                     error_message="Chyba při zápisu souboru",
                                     error_code=22).lift()
                        self.invoker[1].configure(text="Chyba při provádění skriptu",
                                                  text_color="red")
            case _:
                ErrorHandler(master=self,
                             error_message="Nebyla zvolena žádná organizace!",
                             error_code=2).lift()
                self.progressbar.stop()
                self.progressbar.grid_forget()

        self.progressbar.stop()
        self.progressbar.grid_forget()

    def write_result(self, result : any) -> int:
        """
        handles the output file writing
        :param result: taken as any since it could either be a tree or a string
        :return: int signifying success or failure
        """
        try:
            try:
                file = open(f"{self.output_directory}{self.get_separator(self.output_directory)}{self.drop_down[0].get()}-FV-{datetime.today().strftime('%m-%Y')}.xml", "w", encoding="utf-8")
                result = ''.join(result)
                file.write(result)
                file.close()
                return 0
            except:
                result.write(f"{self.output_directory}{self.get_separator(self.output_directory)}{self.drop_down[0].get()}-FV-{datetime.today().strftime('%m-%Y')}.xml", encoding="utf-8")
                return 0
        except:
            return 1

if __name__ == '__main__':
    app = XmlConfig()
    app.mainloop()