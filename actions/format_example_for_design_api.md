
## Implementation approach
We will ...

## Swift package name
```python
"airport_gauge_test"
```

## File list
```swift
[
    "main.swift",
]
```

## Data structures and interface definitions
```mermaid
classDiagram
    class Game{
        +int score
    }
    
    Game "1" -- "1" Food: has
```

## Program call flow
```mermaid
sequenceDiagram
    participant M as Main
    G->>M: start game
    G->>M: end game
```