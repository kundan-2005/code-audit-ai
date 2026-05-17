# Architecture

## System Overview

Code Audit AI is built on a multi-agent architecture where specialized agents work together to perform comprehensive code analysis.

```
┌─────────────────────────┐
│   CodeAuditor (Main)    │
└────────────┬────────────┘
             │
      ┌──────┴──────┬────────────┬──────────────┐
      │             │            │              │
   ┌──▼──┐      ┌──▼──┐     ┌───▼────┐    ┌───▼──────┐
   │SEC  │      │PERF │     │QUALITY │    │FUNCTION  │
   │AGENT│      │AGENT│     │AGENT   │    │AGENT     │
   └─────┘      └─────┘     └────────┘    └──────────┘
      │             │            │              │
      └──────────────┴────────────┴──────────────┘
                     │
              ┌──────▼──────┐
              │ AuditResult │
              └─────────────┘
```

## Components

### 1. CodeAuditor (Main Orchestrator)
- Coordinates all agents
- Manages configuration
- Filters results by severity
- Generates reports

### 2. Agents

#### SecurityAgent
- Detects hardcoded credentials
- Identifies SQL injection vulnerabilities
- Checks for insecure random usage
- Detects dangerous functions (eval, pickle.loads)

#### PerformanceAgent
- Identifies nested loops
- Detects inefficient string operations
- Finds imports inside loops
- Warns about unoptimized list operations

#### QualityAgent
- Checks for missing docstrings
- Identifies long functions
- Detects complex conditionals
- Finds magic numbers
- Validates naming conventions

#### FunctionalityAgent
- Detects unreachable code
- Finds unused variables
- Checks exception handling
- Validates return statement consistency

### 3. Models

**AuditConfig**
- Configuration for audit behavior
- Severity filtering
- Language specification
- Performance parameters

**Issue**
- Represents a code issue
- Contains severity, type, line number
- Includes suggestions for fixes

**AuditResult**
- Aggregates all issues found
- Metadata about the audit
- Timestamp and configuration used

### 4. Utils

**Logger**
- Structured logging throughout system
- Debug and info level messages

**Validators**
- Input validation for code
- Configuration validation

**Helpers**
- Formatting utilities
- Issue grouping

## Data Flow

1. User provides code and optional config
2. CodeAuditor validates inputs
3. Each agent analyzes the code in parallel
4. Issues are collected and filtered
5. AuditResult is created
6. Optional report generation

## Extensibility

New agents can be added by:
1. Extending BaseAgent
2. Implementing analyze() method
3. Adding to CodeAuditor orchestration
4. Registering in agents/__init__.py

## Performance Considerations

- Agents run sequentially (can be parallelized in future)
- Timeout parameter prevents long analyses
- Issue filtering reduces report size
- Configurable agent enablement
