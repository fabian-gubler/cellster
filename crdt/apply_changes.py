from parser.tree_operations import delete_node, find_node, replace_node, edit_node, find_parent_and_child, add_node, delete_node

from parser.ast_nodes import BaseNode, Function, Binary, Unary


class StructuralChangeException(Exception): pass

def apply_changes_to_ast(original_ast, changes):
    for change in changes:
        if change['type'] == 'modification':
            # Find and replace the modified node
            original_node = find_node(original_ast, change['original'].id_history)
            replace_node(original_ast, original_node.id_history, change['modified'])
        
        elif change['type'] == 'addition':
            # Logic to add a node to the AST
            # This uses add_node() from tree_operations.py

            # find parent node to add to
            parent_node = find_node(original_ast, change['parent_id_history'])

            # syntax: def add_node(parent, new_node, position=None, child_side=None):
            add_node(parent_node, change['node'], child_side=change['child_side'])



        elif change['type'] == 'deletion':
            # Logic to remove a node from the AST
            # This uses delete_node() from tree_operations.py
            parent, child_to_delete = find_parent_and_child(original_ast, change['node'].id_history)
            delete_node(parent, child_to_delete.id_history)


        elif change['type'] == 'root_change':
            raise StructuralChangeException("Root change detected")


    return original_ast


def apply_addition(ast, change):
    # Assuming change['node'] is the node to be added
    # and change['parent_id'] identifies where to add it
    parent_node = find_node(ast, change['parent_id'])
    if parent_node:
        # Logic to insert the new node into the parent's children
        # This will vary based on the type of the parent node
        if isinstance(parent_node, Function):
            parent_node.arguments.append(change['node'])
        # Add similar logic for other composite node types if necessary
        # Update parent-child relationship
        change['node'].parent = parent_node


def apply_deletion(ast, change):
    parent, child_to_delete = find_parent_and_child(ast, change['node'].id_history)
    if parent and child_to_delete:
        # Remove the child from the parent's children
        if isinstance(parent, Function):
            parent.arguments.remove(child_to_delete)
        # Add similar logic for other composite node types if necessary
