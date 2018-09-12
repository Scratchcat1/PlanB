import auto_ui
import auto_ui_dialog
import tkinter 

__version__ = "0.1.0"

ui_mode = "text"

def get_ui_renderer(ui_mode):
    if ui_mode == "tk":
        root = tkinter.Tk()
        return auto_ui.Tk_Form_Display(root)
    else:
        return auto_ui.Text_Form_Display()


if __name__ == "__main__":
    renderer = get_ui_renderer(ui_mode)
    app = auto_ui_dialog.App(renderer)
    while True:
        try:
            app.main_menu_dialog()
        except Exception as e:
            print("An error occured", e)




