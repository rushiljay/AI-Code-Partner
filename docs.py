import libcst as cst
import ast
import astor

#TODO: use ollama to generate documentation


class DocstringAdder(cst.CSTTransformer):
    """
    Transformer that adds a placeholder docstring to every function, class,
    and method that lacks one.
    """

    def leave_FunctionDef(self, original_node, updated_node):
        # Check if the function already has a docstring
        if updated_node.body.body and isinstance(
            updated_node.body.body[0], cst.SimpleStatementLine
        ):
            first_stmt = updated_node.body.body[0]
            if isinstance(first_stmt.body[0], cst.Expr) and isinstance(
                first_stmt.body[0].value, cst.SimpleString
            ):
                return updated_node  # Docstring exists, do nothing
        # Add a placeholder docstring
        docstring = cst.SimpleStatementLine(
            body=[cst.Expr(value=cst.SimpleString('"""TODO: Add docstring"""'))]
        )
        new_body = [docstring] + list(updated_node.body.body)
        return updated_node.with_changes(
            body=updated_node.body.with_changes(body=new_body)
        )

    def leave_ClassDef(self, original_node, updated_node):
        # Similar to leave_FunctionDef, add docstrings to classes
        if updated_node.body.body and isinstance(
            updated_node.body.body[0], cst.SimpleStatementLine
        ):
            first_stmt = updated_node.body.body[0]
            if isinstance(first_stmt.body[0], cst.Expr) and isinstance(
                first_stmt.body[0].value, cst.SimpleString
            ):
                return updated_node  # Docstring exists, do nothing
        docstring = cst.SimpleStatementLine(
            body=[cst.Expr(value=cst.SimpleString('"""TODO: Add docstring""""'))]
        )
        new_body = [docstring] + list(updated_node.body.body)
        return updated_node.with_changes(
            body=updated_node.body.with_changes(body=new_body)
        )


def add_docstrings_to_files(input_file: str, output_file: str):
    # Read the source code from a file
    with open(input_file, "r") as file:
        source_code = file.read()

    # Parse the source code into a CST
    tree = cst.parse_module(source_code)

    # Transform the CST by adding docstrings
    modified_tree = tree.visit(DocstringAdder())

    # Write the modified code back to another file
    with open(output_file, "w") as file:
        file.write(modified_tree.code)

    # TODO, use below for the pdocs (removes comments automatically)

    # with open('modified_script.py', 'r') as file:
    #     tree = ast.parse(file.read())

    # with open('modified_script.py', 'w') as file: # make sure to delete this file
    #     file.write(astor.to_source(tree))

    # use above for file explainer, as well as docs generation for each function, use a hybrid approach between local and remote llm


# Example usage
add_docstrings_to_files("coder.py", "coder_with_docstrings.py")
