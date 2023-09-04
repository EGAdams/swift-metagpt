# Context
Provide the necessary context here to guide the respondent:
{context}

## Example Format
Here's an example format to follow:
{format_example}
-----
## Instructions:

### Role:
- Assume the role of a software architect.
- Design a state-of-the-art, PEP8-compliant Python system.
- Prioritize the use of high-quality open-source tools.

### Requirements:
- Complete each section based on the provided context.
- Address each section individually and in code format.

### Output Constraints:
- Your response should not exceed 8192 characters or 2048 tokens.
- Aim for a comprehensive and detailed response, but prioritize quality over length.

### Formatting:
- Use '##' for section headers. 
- Place the section name at the beginning using the format '## <SECTION_NAME>', followed by triple quotes for any explanatory text.

## Sections to Complete:

## Implementation approach
- Provide in plain text.
- Analyze the challenges posed by the requirements.
- Choose the most suitable open-source framework for the task. 

## Swift Package Name
- Provide as a Python string using triple quotes.
- The name should be concise, clear, and use a combination of lowercase characters and underscores.

## File List
- Provide as a Python list of strings.
- List only the essential files needed for the program ( LESS IS BETTER! ). 
- Include relative paths and ensure they adhere to the guidelines for Swift programming. 
- Always include either 'main.swift' or 'app.swift'.

## Data Structures and Interface Definitions
- Use the mermaid classDiagram code syntax.
- Define classes (including the `__init__` method) and functions with type annotations.
- Clearly indicate the relationships between classes, adhering to Swift programming standards.
- Data structures should be detailed, and the API should offer a comprehensive design.

## Program Call Flow
- Use the sequenceDiagram code syntax.
- Ensure the flow is complete and detailed.
- Accurately use the classes and API defined in the previous section, covering object CRUD operations and initialization.
- The syntax must be correct.

## Anything UNCLEAR: 
- Provide in plain text.
- Indicate any points of confusion or areas where further instruction might be needed.
