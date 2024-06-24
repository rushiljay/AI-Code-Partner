import libcst as cst
import ast
import astor

class DocstringAdder(cst.CSTTransformer):
    def leave_ClassDef(self, original_node, updated_node):
        # Check if the class has a docstring
        if not updated_node.body.body[0].__class__ is cst.SimpleStatementLine:
            docstring = cst.SimpleStatementLine(body=[cst.Expr(value=cst.SimpleString('"""This class represents something."""'))])
            new_body = cst.IndentedBlock(body=[docstring] + list(updated_node.body.body))
            return updated_node.with_changes(body=new_body)
        return updated_node

    def leave_FunctionDef(self, original_node, updated_node):
        # Check if the function has a docstring
        if not updated_node.body.body[0].__class__ is cst.SimpleStatementLine:
            docstring = cst.SimpleStatementLine(body=[cst.Expr(value=cst.SimpleString('"""This function does something."""'))])
            new_body = cst.IndentedBlock(body=[docstring] + list(updated_node.body.body))
            return updated_node.with_changes(body=new_body)
        return updated_node

def add_docstrings_to_file(filename):
    with open(filename, "r") as source:
        tree = cst.parse_module(source.read())

    transformer = DocstringAdder()
    modified_tree = tree.visit(transformer)

    # Write the modified tree back to the file
    with open("modified_script.py", "w") as source: #TODO: change this to the original filename
        source.write(modified_tree.code)

    with open("modified_script.py", "w") as source: #TODO: change this to the original filename
        source.write(modified_tree.code)

    # with open('modified_script.py', 'r') as file:
    #     tree = ast.parse(file.read())

    # with open('modified_script.py', 'w') as file:
    #     file.write(astor.to_source(tree))

# Example usage
add_docstrings_to_file("coder.py")
