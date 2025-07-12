; Tree-sitter query for Python symbol extraction

; Classes (including nested)
(class_definition
  name: (identifier) @class.name
  body: (block
    (expression_statement
      (string) @class.docstring)?)) @class.definition

; Methods (functions inside classes)
(class_definition
  body: (block
    (function_definition
      name: (identifier) @method.name
      parameters: (parameters) @method.parameters
      return_type: (type)? @method.return_type) @method.definition))

; Async methods
(class_definition
  body: (block
    (function_definition
      name: (identifier) @async_method.name
      parameters: (parameters) @async_method.parameters
      return_type: (type)? @async_method.return_type) @async_method.definition))

; Decorated methods (decorated functions inside classes)
(class_definition
  body: (block
    (decorated_definition
      definition: (function_definition
        name: (identifier) @decorated_method.name
        parameters: (parameters) @decorated_method.parameters
        return_type: (type)? @decorated_method.return_type) @decorated_method.definition)))

; Top-level functions
(function_definition
  name: (identifier) @function.name
  parameters: (parameters) @function.parameters
  return_type: (type)? @function.return_type) @function.definition

; Top-level decorated functions
(decorated_definition
  definition: (function_definition
    name: (identifier) @decorated_function.name
    parameters: (parameters) @decorated_function.parameters
    return_type: (type)? @decorated_function.return_type) @decorated_function.definition)

; Variables and constants (simple assignments)
(assignment
  left: (identifier) @variable.name
  right: (_) @variable.value) @variable.definition