from datetime import datetime as dt
from abc import ABC, abstractmethod

class FormField(ABC):
    def __init__(self, name: str = None, value: str = None):
        self.name = name
        self._value = value
    
    @property
    @abstractmethod
    def value(self) -> str:
        pass
    
    @value.setter
    @abstractmethod
    def value(self, new_value):
        pass

    @abstractmethod
    def render(self):
        pass


class Label:
    def __init__(self, content: str):
        self.content = content

    def render(self):
        return f"<label>{self.content}</label>"

class Option:
    default_value = "ANY"
    
    def __init__(self, value : list[str], is_selected: bool = False):
        self.value = value
        self.is_selected = is_selected

    def render(self):
        if self.is_selected:
            option_html = f"<option value='{self.value}' selected>{self.value}</option>"
        else:
            option_html = f"<option value='{self.value}'>{self.value}</option>"
        
        if self.value == self.default_value:
            option_html += "<option disabled>---</option>"
        
        return option_html

class DateSelector(FormField):
    date_format = "%Y-%m-%d"
    
    def __init__(self, name: str, label_name: str, value: str = None):
        super().__init__(name, value if value else dt.today().strftime(self.date_format))
        self.label_name = label_name if label_name else name.replace("_", " ")
    
    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, new_dt_value: str):
        if new_dt_value is None: return
        try:
            dt.strptime(new_dt_value, self.date_format) # validation
            self._value = new_dt_value
        except Exception:
            raise ValueError(f"Invalid date format for '{new_dt_value}'. Expected format: {self.date_format}")

    def render(self):
        js = """<script>flatpickr(".date-selector", {dateFormat: "Y-m-d"});</script>"""
        return f"<input class='date-selector'type='date' name='{self.name}' value='{self.value}' id='datepicker'>" + js
        
class Select(FormField):
    def __init__(self, name: str, label_name: str, options: list[str], value = None):
        super().__init__(name=name, value=None)
        self.label_name = label_name
        options = [Option(value=o, is_selected=False) for o in options]
        default_option = Option(value=Option.default_value, is_selected=False)
        self._options = [default_option] + options
        self.reset()
        
        self.value = value if value else default_option.value

    @property
    def value(self) -> str:
        '''curent selected option'''
        return self._value.value if self._value else None
    
    @value.setter
    def value(self, opt_val: str):
        '''select option by value'''
        if opt_val is None: return
        self.reset() # single selection
        for option in self.options:
            if str(option.value) == str(opt_val):
                option.is_selected = True
                self._value = option
                return
        raise ValueError(
            f"failed to select value '{opt_val}' in Select '{self.name}'. "
            f"available: {[o.value for o in self.options]}"
        )
    
    @property
    def options(self) -> list[Option]:
        return self._options
    
    def reset(self):
        for option in self.options:
            option.is_selected = False
        self._value = None

    def render(self):
        select_html = f"<select name='{self.name}'>"
        for option in self.options:
            select_html += option.render()
        select_html += "</select>"
        return select_html

class FilterForm:
    def __init__(self, fields: list[FormField], cgi_method:str , action: str = "/dashboard/", request_method: str = "GET"):
        self._fields: list[FormField] = fields
        self.action: str = action
        self.cgi_method: str = cgi_method
        self.request_method: str = request_method
    
    @property
    def fields(self) -> list[FormField]:
        return self._fields
    
    @property
    def field_dict(self) -> dict[str, FormField]:
        return { field.name : field for field in self._fields }

    def update(self, field_values: dict[str, str], is_ignore_unknown_fields: bool = True):
        '''Bulk update field values from a dict, e.g. cgi value'''
        for field_name, field_value in field_values.items():
            try:
                self[field_name] = field_value
            except KeyError:
                if is_ignore_unknown_fields is False: 
                    raise KeyError(f"Field with name '{field_name}' not found in FilterForm.")
                    
    
    def __setitem__(self, field_name: str, field_value: str):
        for i, f in enumerate(self.fields):
            if f.name == field_name:
                f.value = field_value
                self._fields[i] = f
                return
        raise KeyError(f"Field with name '{field_name}' not found in FilterForm.")

    def __getitem__(self, field_name: str) -> str:
        return self.get_field(field_name).value

    def get_field(self, field_name: str) -> FormField:
        f = self.field_dict.get(field_name)
        if f is None:
            raise KeyError(f"Field with name '{field_name}' not found in FilterForm.")
        return f
    
    def set_field(self, field: FormField):
        if field.name is None:
            raise ValueError("Field must have a name to be set in FilterForm.")
        
        for i, f in enumerate(self.fields):
            if f.name == field.name:
                self._fields[i] = field
                return
        raise KeyError(f"Field with name '{field.name}' not found in FilterForm.")

    def render_submit_button(self):
        return "<input type='submit' value='Filter' style='background: #E1703D; border-radius: 5px; padding: 5px; color: white; font-weight: bold; font-size: 1em; border: 0; cursor: pointer'>"

    def render(self) -> str:
    
        form_html = f"<form action='{self.action}' method='{self.request_method}'>"
        form_html += f"<input type='hidden' name='method' value='{self.cgi_method}'>"
    
        fields = self._fields
    
        for field in fields:
            field_html = field.render()
            form_html += Label(f"{field.label_name}: {field_html}").render()
    
        form_html += self.render_submit_button()
        form_html += "</form>"
    
        return form_html
    