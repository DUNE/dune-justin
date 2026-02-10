from typing import Union

class Option:
    default_value = "ANY"
    
    def __init__(self, label: str, value: str = None, is_selected: bool = False):
        self.label = label
        self.value = value if value else label
        self.is_selected = is_selected
    
    def render(self):
        option_html = f"<option value='{self.value}' {'selected' if self.is_selected else ''}>{self.label}</option>"
        if self.value == self.__class__.default_value:
            option_html += self.__class__.render_divider()
        return option_html

    @classmethod
    def render_divider(cls):
        return "<option disabled>---</option>"

    @classmethod
    def create_default_option(cls):
        return cls(label=cls.default_value, value=cls.default_value, is_selected=True)
        
class Select:
    def __init__(self, label_name: str, options: list[Option]):
        self.name = label_name
        self.options = options
        self.reset()
    
    @property
    def attr_name(self):
        return self.name.lower().replace(" ", "_")
    
    @property
    def current_selected_option(self) -> Union[Option, None]:
        for option in self.options:
            if option.is_selected:
                return option
    
    def reset(self):
        for option in self.options:
            option.is_selected = False
            
    def select_option(self, opt_val: str) -> Union[Option, None]:
        self.reset()
        for option in self.options:
            if str(option.value) == str(opt_val):
                option.is_selected = True
                return option
    
    def prepend_option(self, option: Option) -> None:
        self.options = [option] + self.options

    def render(self):
        select_html = f"<select name='{self.attr_name}'>"
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
    def __init__(self, selects: list[Select], cgi_method:str , action: str = "/dashboard/", request_method: str = "GET"):
        
        for select in selects:
            select.reset()
            select.prepend_option(Option.create_default_option())
        
        self.selects: list[Select] = selects
        self.action: str = action
        self.cgi_method: str = cgi_method
        self.request_method: str = request_method
        self._filter_dict: dict[str, str] = {
            select.attr_name : select.current_selected_option.value for select in selects
        }

    @classmethod
    def create_from_dict(cls, data: dict[str, list[str]], cgi_method, action: str = "/dashboard/", request_method: str = "GET"):
        selects: list[Select] = []
        for column_name, values in data.items():
            options = [Option(label=value, value=value, is_selected=False) for value in values]
            select = Select(label_name=column_name, options=options)
            selects.append(select)
        return cls(selects=selects, cgi_method=cgi_method, action=action, request_method=request_method)
    
    def _update_filter_dict(self, select: Select) -> None:
        if self._filter_dict.get(select.attr_name) is None:
            raise ValueError(f"Select with name '{select.attr_name}' not found in filter_dict.")
        self._filter_dict[select.attr_name] = select.current_selected_option.value

    def set_filter(self, col_name: str, filter_val: str) -> None:
        if filter_val is None: 
            return
        for select in self.selects:
            if select.attr_name == col_name:
                selected_option = select.select_option(opt_val=filter_val)
                if selected_option is None:
                    raise ValueError(f"Option with value '{filter_val}' not found in select '{col_name}'.")
                self._update_filter_dict(select)
                return
        raise ValueError(f"Select with name '{col_name}' not found in the form.")
    
    def render_submit_button(self):
        return "<input type='submit' value='Filter' style='background: #E1703D; border-radius: 5px; padding: 5px; color: white; font-weight: bold; font-size: 1em; border: 0; cursor: pointer'>"
        
    def render(self) -> str:
        form_html = f"<form action='{self.action}' method='{self.request_method}'>"
        form_html += f"<input type='hidden' name='method' value='{self.cgi_method}'>"
        for select in self.selects:
            select_html = select.render()
            form_html += Label(f"{select.name}: {select_html}").render()
        
        form_html += self.render_submit_button()
        
        form_html += "</form>"
        return form_html
