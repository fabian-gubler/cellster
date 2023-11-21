---
id: refined_algo
aliases:
  - Algorithm
tags: []
---


# Algorithm

## Identity-Preserved Change Acceptance

**Ockham's Razor**: Emphasizing that changes are permissible and integrated into the system as long as the identity (represented by the node's ID) of the node remained unchanged. Conflict resolution is kept to a minimum. In cases where there is a substantial backlog of unresolved changes, a more hands-on approach is required to ensure that each change aligns with the overall system's integrity.

1. **Unique Node Identification**: Each node in the AST (Abstract Syntax Tree) of the Excel formula is assigned a unique ID. This ID remains consistent even if the node's parent changes, ensuring children nodes can still be modified independently.

2. **Handling Operations**:
   - **Additions**: When a user adds a new branch in the formula, the position and relation to other nodes are explicitly captured. The new node, along with its position information, is sent as an 'add' operation. If sent possitional information is not found, operation is discarded, indicating a prior change, that needs to be taken into account before proceeding.
   - **Deletions**: Deleting a node also removes its children. A 'delete' operation is sent with the ID of the node to be deleted. If the ID is not found, operation is discarded, indicating a prior change that needs to be taken into account before proceeding.
   - **Modifications**: Modifications are sent as 'change' operations. If the to be changed Node is found, a change is allowed. If the to be changed node is not found, operation is discarded, indicating a prior change that needs to be taken into account. Conflicts in modifications are resolved based on the level of change; changes including higher nodes take precedence over lower-level ones. Similarly, deeper changes (i.e. more children affected) take precedence over smaller changes. In other words, first the highest node modified is considerd. Second, if this is equal, the deepness of change is considered.

3. **Conflict Resolution**: If multiple users solely modify the same node within a branch, the algorithm uses timestamps  to resolve conflicts, typically following a 'last writer wins' rule. If the timestamp is equal, a tie-breaking mechanism is used: 1) Amount of submitted operations, 2) Fallback: random choice (assumed to be rare). If deemed beneficial, a counter of previous changes could be included to select and thus reward more involved users' changes.

4. **Tree Integrity and Validation**: After applying all operations, a validation program checks the tree for semantic correctness. It ensures the tree is syntactically correct, has no broken references, and is free from circular dependencies.

5. **Updating Users:** After the merge, the latest version of the AST is distributed back to all users, ensuring everyone has the updated formula.

## Thoughts on Strategy

### Effectivness

1. There will always be undesired changes for other users.
2. Two strategies could be debated.
    a) If a node hasn't been changed, it can be
    b) If a parent node has been changed, its children should not be affected

3. For a real-life use case, the former is prefered. Once connected, indicated in red the
   users sees what other nodes have been changed, before submitting his changed nodes
   (allows reflection on changes) and allowing to discard.

### Conflict Resolution

1. With time-stamps simultaneous changes are almost impossible
2. This however is not necessarily desirable. Changes with few seconds difference do not
   represent clear preference.

3. The users should be allowed to set a timeframe that accurately reflects the trade-off
   between additional conflict-resolution added manual intervention.

## Considerations

### Complexity in Node Identification 

**Problem:** Generating and maintaining unique IDs can be complex.

**Solution:** Ensuring no violation
1. User-prefix (not used for traversal)
2. Check if not taken

### Placement of branches 

**Problem:** If the parent node is the root node we need to ensure the sequence is correct

**Solution:** Rebuilding the tree with new parent node, adhering to the left-to-right evaluation of the formula.

### Supernodes

**Problem:** Changin e.g. a Cell-range into a Number leaves orphan nodes

**Solution:** Orphans must be deleted for such operations
