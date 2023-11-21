---
id: notes_algo
aliases:
  - Algorithm
  - Simplified Methods
tags: []
---


## Simplified Methods

```python
def applyOperation(self, operation):
    switch operation.type:
        case 'add':
            self.addNode(operation.node)
        case 'delete':
            self.deleteNode(operation.nodeID)
        case 'change':
            self.changeNode(operation.node)

def addNode(self, node):
    if node.parentID in self.nodeIDs:
        parentNode = self.findNode(node.parentID)
        parentNode.addChild(node)
        self.nodeIDs.add(node.ID)
    else:
        // The parent node does not exist, possibly due to a conflict

def deleteNode(self, nodeID):
    if nodeID in self.nodeIDs:
        node = self.findNode(nodeID)
        self.removeNode(node)
        self.nodeIDs.remove(nodeID)
    else:
        // Node already deleted or does not exist

def changeNode(self, newNode):
    oldNode = self.findNode(newNode.ID)
    if oldNode and self.isHigherLevelChange(oldNode, newNode):
        self.updateNode(oldNode, newNode)

```


### Modification

Users make changes to their local copy of the AST while offline. These changes could include editing functions, changing arguments, adding new nodes, or deleting existing ones. Each change can be timestamped and tagged with the user's unique identifier.

### Conflict-Free Merging:

    Node-by-Node Comparison: The merging process involves comparing the ASTs node by node.
    Resolving Conflicts: If a node has been changed by multiple users, the system uses a predefined conflict resolution strategy. This could be as simple as 'last writer wins' based on timestamps or more complex rules depending on the nature of the changes.
    Constructing the Merged AST: The final merged AST is constructed by taking the resolved nodes from each user's AST. This AST represents the latest state of the formula after incorporating all changes.

### Considerations




## Explanation

Here's a textual representation of this strategy:

### Logical Statement of Strategy

1. **Identify the Level of Change in Each Tree:**
   - If one change is at a higher level than the other, replace the entire subtree at that level with the higher-level change.
   - Else, proceed to the next step.

2. **For Changes at the Same Level:**
   - Apply the 'last-writer wins' rule.
   - In case of simultaneous changes, use a predefined tie-breaking mechanism to determine the winner.
   - Replace the conflicting part with the winning change.
   - If no conflict is detected at this level, proceed to the next step.

3. **Addition of New Nodes:**
   - If there are new nodes (additions) in either tree that do not conflict with existing nodes, integrate these into the final tree.

### Visualization (Decision Tree)

```
                  Start
                    |
          Identify Level of Change
              /                \
     Higher Level            Same Level
     Change Wins         Last-Writer Wins
        /                     /       \
Replace Subtree        Tie-Breaker    No Conflict
                           /               \
                Winning Change        Integrate New Nodes
                    Applied
                         |
                Finalize Merged Tree
```

## Simple Rules

### Analysis of Provided Levels

1. **Level 1 - Different Arguments in Inner Function:**

Inner Function:
The first change is `=SUM(A1:A5)`
The second change is `=SUM(A6:A10)`

Value:
The first change is `=SUM(A1:A05)`
The second change is `=SUM(A1:A08)`

   - Strategy is to choose the most recent change works well here. 
   - **Conflict-resolution:** Develop a tie-breaking mechanism if changes are
     simultaneous.

2. **Level 2 - Node Addition vs Change:**

The first change is `=SUM(A1:A05)`
The second change is `=SUM(A1:A10)+A6`

   - New nodes are added while reflecting changes in the deepest common ancestor 
   - **Edge Case to Consider:** Ensure that the addition of new nodes does not violate the syntactical structure of the formula.

3. **Level 3 - Outer Function Changed:**

The first change is `=SUM(A1:A05)`
The second change is `=MIN(A1:A10)`

   - Choosing the most outer function of the two changes 
   - **Edge Case to Consider:** What if the outer functions are entirely different, affecting the interpretation of the formula? User intervention might be necessary

## Where it falls apart


### Much Information lost

1. **Branch perspective:** 

Ensure that this replacement doesn't inadvertently discard significant changes at lower levels. Sometimes, changes at lower levels might be more critical than higher-level changes.

**Better Strategy:** Before winning higher-level change, check how much information has been changed in its nodes

Simple solution - relative Points: (is there a function to not hardcode, e.g. log)
- Root 10:
    - Child Node: 5
        - Child Node: 2
            - Child Node: 1

Calculate the Points for each Change
    - Highest point wins


2. **Formula perspective:**

User 1 has made many changes, whereas User 2 submitted an old change. In case, user 2 has just a higher-level node, where user 1 relied on this might not be good.

**Better Strategy:** Users send Original and Changed Tree. Original is compared to the current source of truth. If there is too much difference, user is prompted to resolve conflicts if he wants to submit the change.

**Git Comparison:** With git merge,  users need to always manually resolve conflicts. With our program we could solve many issues if users, who didn't submited for a long time can `diff` their formula with the newest state before submitting their changes.

### Dealing with Deletions

The first change is a deletion: =""
The second change is an addition: =SUM(A1:A10) + A11.

**Current approach:** Deletion is not yet dealt with.

**General:** Prioritize additions over deletions to preserve more information.

**Resolution Strategy:**
Users must first merge additions before deciding to delete parts.

User 1 decide whether result
a) =SUM(A1:A10) + A11.
b) =A11
c) =""

### Currently not covered


1. **Multiple Conflicts in Different Parts of the Tree (At the same level)**

The first change alters a nested function: =SUM(AVERAGE(A1:A5), A6:A10).
The second change modifies a different part: =SUM(A1:A5) + MIN(A6:A10).

**Current approach:** LWW

**Better Strategy:** Treat each conflict independently, ensuring that the final tree is a valid formula. For instance, merge the changes by combining the non-conflicting parts and applying conflict-resolution rules to the conflicting parts.



### Additional Complexities and Edge Cases

1. **Nested Functions:**
   - If changes occur in nested functions, the conflict resolution needs to be clear at each nested level.
   - **Rule Proposal:** Apply conflict resolution rules starting from the innermost level and work outwards.

2. **Multiple Conflicts in Different Parts of the Tree:**
   - Multiple conflicts could arise in different branches of the tree.
   - **Rule Proposal:** Resolve each conflict independently based on the specified rules, ensuring that the final tree remains syntactically valid.

3. **Structural Changes vs. Content Changes:**
   - Distinguish between structural changes (e.g., function changes, addition/removal of arguments) and content changes (e.g., change in cell range).
   - **Rule Proposal:** Structural changes could have precedence over content changes.

4. **Deletions vs. Additions:**
   - Conflicts between deletions and additions of nodes/functions.
   - **Rule Proposal:** Deletions could take precedence, or a more complex rule based on the nature of the edit might be required.
### Towards a General Strategy and Algorithm

The strategy should incorporate a hierarchical approach to resolving conflicts, starting from the most specific (innermost changes) to the most general (structural changes). It should be robust enough to handle a variety of conflicts, including additions, deletions, and modifications in both content and structure. The algorithm must prioritize maintaining the syntactical integrity of the formula and handle edge cases like simultaneous edits, nested functions, and structural vs. content changes.

To translate this into an algorithm, you'll need to:

1. **Parse the Formula Trees:**
   - Create a robust parser that can turn the Excel formula into a tree structure.

2. **Identify Conflicts:**
   - Develop logic to traverse these trees and identify points of conflict.

3. **Apply Conflict Resolution Rules:**
   - Implement the conflict resolution rules based on the type and location of the conflict.

4. **Rebuild the Tree:**
   - After resolving conflicts, rebuild the tree into a valid Excel formula.

5. **Testing and Edge Case Handling:**
   - Rigorously test with a wide range of formulas and scenarios to ensure all edge cases are covered.

This framework should provide a solid foundation for developing an effective CRDT for Excel formulas. Remember, the key is to balance between choosing the most appropriate edits while maintaining the formula's integrity and user intentions.
