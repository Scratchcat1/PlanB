import auto_ui
import auto_ui_dialog
import tkinter 
import auto_ui_dialog
import configuration_store

__version__ = "0.1.0"

ui_mode = "text"

def get_ui_renderer(ui_mode):
    if ui_mode == "tk":
        root = tkinter.Tk()
        return auto_ui.Tk_Form_Display(root)
    else:
        return auto_ui.Text_Form_Display()


if __name__ == "__main__":
    not_exit = True
    renderer = get_ui_renderer(ui_mode)
    unknown = auto_ui_dialog.Unknown(renderer)
    while True:
        unknown.main_menu_dialog()




