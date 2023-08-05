# XML Thunder

### Installation
    pip install xml_thunder

### Usage
XML Thunder provides a class called 'Lightning'.
The Lightning class's primary purpose is used for creating an XML parser.
The Lightning class provides the following methods:

---

- \_\_init\_\_(self)
  - Initializes an empty private dictionary
####
- \_\_getitem\_\_(self, route: String)
  - Returns None or a Callable from the private dictionary
####
- \_\_len\_\_(self)
  - Returns the length of a private dictionary
####
- \_\_bool\_\_(self)
  - Returns True if the private dictionary is empty
    
---

- get_route(self, route: String)
  - Returns a registered route if there is one at 'route'
####
- get_all_routes(self)
  - Returns all registered routes in the private dictionary
####
- add_route(self, path: String, function: Callable)
  - Adds a route at 'path' with 'function' as the value
  - Returns None
####
- route(self, path: String)
  - Creates a route for the provided 'path'
  - 'path' is any valid xPath
  - _Note that this method is a decorator and should be used as such_
####
- parse(self, xml_like_document: String | FileObject)
  - The entrypoint for parsing xml strings/files
  - Returns None
