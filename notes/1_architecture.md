# Architecture Diagrams

## Simple
graph TD
    subgraph CRDT System
        Parser[Excel Formula Parser]
        CRDTCore[CRDT Core]
        ASTMod[AST Modification and Tracking]
        MetaData[Metadata Management]
        ConflictRes[Conflict Resolution Engine]
        TestHarness[Test Harness]
    end

## Detailed
graph TD
    subgraph CRDT System
        ParserWrapper[Formula Parser Wrapper]
        Parser[Excel Formula Parser]
        CRDTCore[CRDT Core]
        ASTMod[AST Modification and Tracking]
        MetaData[Metadata Management]
        ConflictRes[Conflict Resolution Engine]
        TestHarness[Test Harness]
    end

    Parser --> ParserWrapper
    ParserWrapper --> ASTMod
    ASTMod --> CRDTCore
    CRDTCore --> MetaData
    MetaData --> ConflictRes
    ConflictRes --> TestHarness

    style CRDT System fill:#f9f,stroke:#333,stroke-width:2px



