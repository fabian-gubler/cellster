from parser.tree_operations import find_node, find_parent_and_child, replace_node, add_node, delete_node

class NodeNotFoundError(Exception):
    pass

def merge_ast(original_ast, changes):
    def calculate_depth(original_history, updated_history):
        last_common_index = -1
        for i in range(min(len(original_history), len(updated_history))):
            if original_history[i] == updated_history[i]:
                last_common_index = i
            else:
                break

        # Calculate depth based on lengths after the last common ID
        if last_common_index != -1:
            return len(updated_history) - last_common_index - 1
        return -1  # No common history found

    for change in changes:
        # Handle modifications

        if change['type'] == 'modification':
            modified_node = change['node']
            original_node = find_node(original_ast, modified_node.id_history)

            # print("Modified node ID history: ", modified_node.id_history)
            # print("Original node ID history: ", original_node.id_history)

            if not original_node:
                raise NodeNotFoundError("Node not found in original AST")
            depth = calculate_depth(original_node.id_history, modified_node.id_history)

            if depth > 0:
                replace_node(original_ast, original_node.id_history, modified_node)
            elif depth == 0:
                conflict_resolution(original_node, modified_node)  # Placeholder for conflict resolution logic

        # Handle additions
        elif change['type'] == 'addition':
            parent_node = find_node(original_ast, change["parent_id_history"])
            add_node(parent_node, change["node"], child_side=change["child_side"])

        # Handle deletions
        elif change['type'] == 'deletion':
            parent, child_to_delete = find_parent_and_child(original_ast, change["node"].id_history)
            if parent and child_to_delete:
                delete_node(parent, child_to_delete.id_history)
        
        else: 
            raise Exception("Invalid change type")

    return original_ast

def conflict_resolution(original_node, updated_node):
    # Placeholder function for conflict resolution
    # Implement conflict resolution logic here
    pass
