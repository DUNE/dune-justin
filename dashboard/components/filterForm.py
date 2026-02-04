class Option:
    def __init__(self, label: str, value: str = None, is_selected: bool = False):
        self.label = label
        self.value = value if value else label
        self.is_selected = is_selected
    
    def render(self):
        return f"<option value='{self.value}' {'selected' if self.is_selected else ''}>{self.label}</option>"
        
class Select:
    def __init__(self, name: str, options: list[Option]):
        self.name = name
        self.options = options

    def render(self):
        select_html = f"<select name='{self.name}'>"
        default_selected_option_html = Option(label="ANY", is_selected=True).render()
        select_html += default_selected_option_html
        for option in self.options:
            select_html += option.render()
        select_html += "</select>"
        return select_html

class Label:
    def __init__(self, content: str):
        self.content = content

    def render(self):
        return f"<label>{self.content}</label>"

class FilterForm:
    def __init__(self, selects: list[Select], cgi_method, action: str = "/dashboard/", request_method: str = "GET"):
        self.selects = selects
        self.action = action
        self.cgi_method = cgi_method
        self.request_method = request_method

    @classmethod
    def create_from_dict(cls, data: dict[str, list[str]], cgi_method, action: str = "/dashboard/", request_method: str = "GET"):
        selects = []
        for column_name, values in data.items():
            options = [Option(label=value) for value in values]
            selects.append(Select(name=column_name, options=options))
        return cls(selects=selects, cgi_method=cgi_method, action=action, request_method=request_method)

    def render(self):
        form_html = f"<form action='{self.action}' method='{self.request_method}'>"
        form_html += f"<input type='hidden' name='method' value='{self.cgi_method}'>"
        for select in self.selects:
            select_html = select.render()
            form_html += Label(f"{select.name}: {select_html}").render()
        
        submit_button_html = "<input type='submit' value='Filter' style='background: #E1703D; border-radius: 5px; padding: 5px; color: white; font-weight: bold; font-size: 1em; border: 0; cursor: pointer'>"
        form_html += submit_button_html
        
        form_html += "</form>"
        return form_html
