Simple console program that, from given input with specified format, prints the constructor and getters & setters if needed

Main format:

field(type)[left_boundary:right_boundary] +s +g -re = default_value, ...

* field - field name

* [left_boundary:right_boundary] (optional) - set value boundaries in setters if needed

* +s +g -e (optional) - default arguments, where "-" means False (Remove), and "+" means True (Add)

* s: setters, g:getters, re: raise_exception (if user gives incorrect data, would it raise exception or no)

* = default_value (optional) - set a default value to field via class constructor
