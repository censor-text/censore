<!-- markdownlint-disable ol-prefix -->

# Censore Project Architecture

## Overview

Censore is a Python library that provides profanity filtering capabilities with support for multiple languages and custom patterns. The library is designed to be flexible, extensible, and easy to use while maintaining high performance.

## Project Structure

```plaintext
├── benchmarks/                      # Performance testing directory
│   └── benchmark.py                 # Benchmark test implementations
|
├── censore/                         # Main package directory
│   ├── data/                        # Resource files directory
│   │   ├── exclude_patterns/        # Folder with patterns to be excluded from filtering
│   │   │   ├── en.txt               # English exclusion patterns
│   │   │   ├── uk.txt               # Ukrainian exclusion patterns
│   │   │   └── ...                  # Other language exclusion patterns
|   |   |
│   │   └── patterns/                # Folder with profanity patterns
│   │       ├── en.txt               # English profanity patterns
│   │       ├── uk.txt               # Ukrainian profanity patterns
│   │       └── ...                  # Other language patterns
|   |
│   ├── __init__.py                  # Package initialization and exports
│   └── profanity_filter.py          # Core filtering implementation
|
└── tests/                           # Test suite directory
    ├── __init__.py                  # Test package initialization
    └── test.py                      # Test implementations
```

### File Descriptions

#### Core Files

- `__init__.py`: Exports the main classes and handles backward compatibility with the deprecated `Censor` class
- `profanity_filter.py`: Contains the main `ProfanityFilter` class implementation with all core functionality

#### Data Files

- `data/patterns/*.txt`: Language-specific pattern files containing:
  - One pattern per line
  - Lowercase entries
  - No duplicates
  - UTF-8 encoding

#### Test Files

- `test_filter.py`: Unit tests for filtering functionality, censoring options, and language support
- `test_patterns.py`: Tests for pattern matching, custom patterns, and exclusion rules

## Core Components

### 1. `ProfanityFilter` Class

The main class that handles all profanity filtering functionality.

#### Key Features

- Multi-language support
- Custom pattern support
- Text normalization
- Configurable censoring options
- Pattern exclusion support

#### Important Methods

- `censor()`: Main method for censoring text
- `contains_profanity()`: Check for presence of profanity
- `add_custom_language()`: Add new language patterns
- `add_custom_profanity_patterns()`: Add custom patterns

### 2. Data Management

#### Pattern Storage

- Location: `/data/patterns/`
- Format: Text files (.txt) for each language
- Structure: One pattern per line
- Naming: `{language_code}.txt`

#### Pattern Types

1. Regular Patterns
   - Standard profanity words
   - Common variations
   - Language-specific terms

2. Exclude Patterns
   - False positive prevention
   - Context-aware exclusions
   - Language-specific exceptions

### 3. Text Processing Pipeline

1. Input Processing

```plaintext
Raw Text → Word Tokenization → Strip Punctuation
```

2. Word Analysis

```plaintext
Word → Normalization → Pattern Matching → Profanity Detection
```

3. Censoring Pipeline

```plaintext
Detected Word → Censoring Rules Application → Text Reconstruction
```

## Key Features Implementation

### 1. Language Support

- Dynamic language loading
- Language-specific pattern sets
- Support for "all" languages option
- Additional language injection
- Custom language definition

### 2. Pattern Matching

- Case-insensitive matching
- Character substitution handling (e.g., "0" → "o")
- Pattern exclusion system
- Custom pattern support

### 3. Censoring Options

- Full word censoring
- Partial censoring (preserving first/last characters)
- Custom censoring character
- Pattern-based replacement

## Data Flow

```plaintext
Input Text
    ↓
Language Selection
    ↓
Pattern Loading
    ↓
Text Tokenization
    ↓
Word Processing
    │
    ├→ Normalization
    │   - Character substitution
    │   - Case normalization
    │
    ├→ Pattern Matching
    │   - Profanity detection
    │   - Exclusion checking
    │
    └→ Censoring
        - Pattern application
        - Text reconstruction
    ↓
Output Text
```

## Performance Considerations

### 1. Pattern Storage

- Uses sets for O(1) lookup
- Cached language patterns
- Optimized pattern loading

### 2. Text Processing

- Efficient string manipulation
- Minimal regex usage
- Optimized word splitting

### 3. Memory Management

- Lazy loading of language patterns
- Pattern set reuse
- Efficient data structures

## Extension Points

### 1. Custom Languages

```python
profanity_filter.add_custom_language(
    language="custom",
    custom_patterns=["word1", "word2"],
    exclude_patterns=["good_word"]
)
```

### 2. Pattern Customization

```python
profanity_filter.add_custom_profanity_patterns(
    custom_patterns=[],
    exclude_patterns=[],
    language="custom"
)
```

### 3. Censoring Customization

```python
profanity_filter.censor(
    text="input text",
    partial_censor=True,
    censor_symbol="*"
)
```

## Best Practices

### 1. Language Management

- Load only required languages
- Use language-specific exclude patterns
- Maintain separate custom patterns

### 2. Pattern Definition

- Use lowercase patterns
- Include common variations
- Define specific exclusions
- Test patterns thoroughly

### 3. Performance Optimization

- Reuse filter instances
- Batch process similar texts
- Cache results when possible

## Future Enhancements

1. **Pattern Management**
   - Pattern scoring system
   - Context-aware filtering
   - Machine learning integration

2. **Performance Optimization**
   - Parallel processing
   - Pattern compilation
   - Cached results

3. **Feature Additions**
   - Regular expression support
   - Contextual analysis
   - Profanity severity levels
   - API integration options

## Testing Strategy

1. **Unit Tests**
   - Individual method testing
   - Pattern matching validation
   - Language loading verification

2. **Integration Tests**
   - Multi-language scenarios
   - Custom pattern integration
   - Full text processing

3. **Performance Tests**
   - Large text processing
   - Multiple language loading
   - Pattern matching speed

## Dependencies

- Python 3.6+
- Standard library only:
  - `os`
  - `string`
  - `typing`

## Security Considerations

1. **Pattern File Security**
   - Validate file contents
   - Protect pattern files
   - Sanitize custom patterns

2. **Input Validation**
   - Text length limits
   - Character encoding
   - Pattern validation

3. **Output Sanitization**
   - Consistent censoring
   - Safe character handling
   - Unicode support
