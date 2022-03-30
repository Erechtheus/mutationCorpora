# entity

*List of named entities*

## Items

- **Items** *(object)*
  - **`ID`** *(string)*: Unique entity identifier.
  - **`type`** *(string)*: Entity type (by original corpus).
  - **`normalizedtype`** *(string)*: Entity type (normalized by us). Must be one of: `['Gene', 'Mutation', 'dbSNP']`.
  - **`begin`** *(number)*: Entity offset begin.
  - **`end`** *(number)*: Entity offset end.
  - **`text`** *(string)*: Entity string representation.
