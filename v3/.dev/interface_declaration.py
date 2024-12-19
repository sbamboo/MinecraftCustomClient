class MenuHolder():
    def __init__(self,resources={}):
        self.resources = resources
    def gen_schema(self):
        def gen_schema(self):
            # Retrieve all method names of the class
            method_names = [method for method in dir(self) if callable(getattr(self, method))]
            # Filter out methods starting with an underscore
            public_methods = {method.replace('_', '.'): getattr(self, method) for method in method_names if not method.startswith('_')}
            toret = {
                "resources": self.resources,
                "actions": {},
                "callbacks": {}
            }
            for x,y in public_methods.items():
                if "." in x:
                    parts = x.split(".")
                    if parts[0] == "callback":
                        toret["callbacks"][ parts[1:].join(".") ] = y
                    else:
                        toret["actions"][ parts[1:].join(".") ] = y
                else:
                    toret["actions"] = y

# Example
class MainMenu(MenuHolder):
    def __init__(self,interfaceHost,resources):
        self.interfaceHost = interfaceHost
        super(resources)

    def button_install():

    def button_uninstal():

    def button_openinstloc():

    def button_exit():


# 