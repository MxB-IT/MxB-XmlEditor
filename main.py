"""Main module used as an entrypoint for the app."""

from src.xml_editor import XmlEditor

if __name__ == "__main__":
    app: XmlEditor = XmlEditor()
    app.mainloop()
