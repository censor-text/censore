
# GitHub Copilot Instructions for **censore** Project

## Project Overview

**censore** is a Python library for profanity filtering with multi-language support. The code should follow these key principles:

- Type safety using Python type hints
- Clean code practices with clear documentation
- High performance and memory efficiency
- Extensible architecture for multiple languages

## Code Style Guidelines

### Type Hints

- Always use type hints for function parameters and return values
- Use `Optional[]` for nullable parameters
- Use `List[]`, `Dict[]`, `Set[]` from typing module

Example:

```python
def function_name(param: str, optional_param: Optional[List[str]] = None) -> bool:
    pass
```

### Documentation

- Every class and method must have docstrings
- Use Args, Returns, and Raises sections in docstrings
- Include examples for complex methods
- Document performance implications when relevant

### Error Handling

- Use explicit exception handling
- Create custom exceptions when appropriate
- Validate input parameters
- Handle file operations safely

## Core Components Implementation

### ProfanityFilter Class

- Maintain immutable substitution tables
- Use efficient data structures (sets for pattern matching)
- Implement lazy loading for language patterns
- Keep methods focused and single-purpose

### Pattern Matching

- Optimize for performance
- Use set operations where possible
- Implement case-insensitive matching
- Handle character substitutions efficiently

### File Operations

- Use UTF-8 encoding for all file operations
- Implement proper path handling
- Handle missing files gracefully
- Cache file contents when appropriate

## Test Requirements

- Write unit tests for all public methods
- Include edge cases and boundary testing
- Test performance for large datasets
- Verify multi-language functionality

## Performance Considerations

- Prefer set operations over list operations
- Cache frequently used patterns
- Minimize string operations
- Use efficient text processing algorithms

## Security Requirements

- Sanitize all file inputs
- Validate language codes
- Handle large inputs safely
- Protect against malicious patterns

## Do Not

- Use global variables
- Modify immutable data structures
- Leave TODO comments without tickets
- Skip type hints or documentation

## Always

- Follow Black style guide
- Use meaningful variable names
- Write self-documenting code
- Consider memory usage

## Example Patterns

When generating code, follow these patterns:

```python
# Class definition
class ClassName:
    """
    Class description.

    Attributes:
        attr_name (type): description
    """
    def method_name(
        self,
        param: ParamType,
        optional_param: Optional[ParamType] = None
    ) -> ReturnType:
        """
        Method description.

        Args:
            param (ParamType): description
            optional_param (Optional[ParamType]): description

        Returns:
            ReturnType: description

        Raises:
            ExceptionType: description
        """
        # Implementation
```
