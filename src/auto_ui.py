import tkinter as tk
import re
import queue

class UI_Form:
    def __init__(self):
        self._title = ""
        self._entries = []

    def set_title(self, title):
        self._title = title

    def get_title(self):
        return self._title

    def add_description(self, description_text):
        self._entries.append({
            "type": "description",
            "payload": {
                "text": description_text
                }
            })

    def add_query(self,var_identifier, query_label, conv_func = str, default_value = None):
        # var_identifier stores the key under which the result of the query will be stored.
        # Default value will be the value returned. IT WILL NOT BE CONVERTED
        self._entries.append({
            "type": "query",
            "payload": {
                "var_identifier":var_identifier,
                "query_label":query_label,
                "conv_func":conv_func,
                "default_value":default_value
                }
            })

    def get_entries(self):
        return self._entries

class Form_Display:
    def get_correct_value(self, entry, raw_value):
        if raw_value == "":
            return entry["payload"]["default_value"]
        return entry["payload"]["conv_func"](raw_value)

       
        

class Tk_Form_Display(Form_Display):
    """
    Tkinter auto UI form. Uses GRID!
    """
    def __init__(self, frame, start_column = 1, start_row = 1):
        self._frame = frame
        self._start_column = start_column
        self._start_row = start_row
        self.reset()

    def reset(self):
        self._results_queue = queue.Queue()
        self._form_entries = {}

    def run(self, form):
        self.reset()
        column = self._start_column
        row = self._start_row

        title_label = tk.Label(self._frame, text = form.get_title())
        title_label.grid(row = row, column = column)
        row += 1

        for entry in form.get_entries():
            entry_payload = entry["payload"]
            if entry["type"] == "description":
                tk.Message(self._frame, text = entry_payload["text"])

            if entry["type"] == "query":
                query_label = tk.Label(self._frame, text = entry_payload["query_label"])
                
                tk_item = tk.Entry(self._frame)
                self._form_entries[entry_payload["var_identifier"]] = {
                    "tk_entry": tk_item,
                    "query": entry
                    }

                query_label.grid(row = row, column = column)
                tk_item.grid(row = row, column = column + 1)
            row += 1
            
        submit_button = tk.Button(self._frame, text = "Submit", command = lambda : self._results_queue.put("submit"))
        submit_button.grid(row = row, column = column)
        
    def get_results(self):
        while self._results_queue.get() != "submit":
            pass

        results = {}
        for key, value in self._form_entries.items():
            results[key] = self.get_correct_value(value["query"], value["tk_entry"].get())
            
        return results
                

class Text_Form_Display(Form_Display):
    """
    Text Auto_UI form
    """
    def __init__(self):
        self.reset()

    def reset(self):
        self._results = {}

    def run(self,form):
        self.reset()
        print("\n")
        print(form.get_title())

        max_query_length = max([0] + [(len(item["payload"]["query_label"]) if item["type"] == "query" else 0) for item in form.get_entries()])
        base_string = create_base_string(max_query_length)   #Determines maximum length of query so each query aligns neatly
        
        for entry in form.get_entries():
            if entry["type"] == "description":
                print(entry["payload"]["text"])
            elif entry["type"] == "query":
                raw_input = input(base_string.format(entry["payload"]["query_label"],">>"))
                self._results[entry["payload"]["var_identifier"]] = self.get_correct_value(entry, raw_input)

    def get_results(self):
        return self._results
        
            


def create_base_string(size):
    return "{0:"+str(size)+"} : {1}"
