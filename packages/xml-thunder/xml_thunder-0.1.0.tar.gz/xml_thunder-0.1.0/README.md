# XML Thunder

## Installation
    pip install xml_thunder

## Usage
XML Thunder provides a class called 'Lightning'.
The Lightning class's primary purpose is used for creating an XML parser.
The Lightning class provides the following methods:

---

- \_\_init\_\_(self)
  - Initializes an empty private dictionary
####
- \_\_repr\_\_(self)
  - Returns the string of the private dictionary
####
- \_\_str\_\_(self)
  - Returns the string of the private dictionary
####
- \_\_contains\_\_(self, route: String)
  - Returns a bool if the route is in the keys of the private dictionary
####
- \_\_getitem\_\_(self, route: String)
  - Returns None or a Callable from the private dictionary
####
- \_\_setitem\_\_(self, route: String, function: Callable)
  - Maps a route to the function
  - Returns None
####
- \_\_delitem\_\_(self, route: String)
  - Deletes the specified route
  - Returns None
####
- \_\_len\_\_(self)
  - Returns the length of a private dictionary
####
- \_\_bool\_\_(self)
  - Returns True if the private dictionary is empty

---

- get_all_routes(self)
  - Returns all registered routes in the private dictionary
####
- route(self, path: String)
  - Creates a route for the provided 'path'
  - 'path' is any valid xPath
  - _Note that this method is a decorator and should be used as such_
####
- parse(self, xml_like_document: String | FileObject)
  - The entrypoint for parsing xml strings/files
  - Returns None
