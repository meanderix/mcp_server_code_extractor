; Tree-sitter query for Python symbol extraction

; Classes
(class_definition
  name: (identifier) @class.name) @class.definition

; Methods (functions inside classes)
(class_definition
  body: (block
    (function_definition
      name: (identifier) @method.name
      parameters: (parameters) @method.parameters) @method.definition))

; Decorated methods (decorated functions inside classes)
(class_definition
  body: (block
    (decorated_definition
      definition: (function_definition
        name: (identifier) @decorated_method.name
        parameters: (parameters) @decorated_method.parameters) @decorated_method.definition)))

; Top-level functions
(module
  (function_definition
    name: (identifier) @function.name
    parameters: (parameters) @function.parameters) @function.definition)

; Top-level decorated functions
(module
  (decorated_definition
    definition: (function_definition
      name: (identifier) @decorated_function.name
      parameters: (parameters) @decorated_function.parameters) @decorated_function.definition))