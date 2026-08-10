# 1. Purpose

---

# Overview

This document defines the mandatory development rules for implementing ProfitPilot.

It establishes the engineering standards, architectural constraints, implementation guidelines, and development practices that must be followed throughout the project's lifecycle.

Unlike the Architecture Document, which defines **what** the system is, this document defines **how** the system must be implemented.

Every developer, contributor, and AI coding assistant involved in the project must comply with the rules defined in this document.

---

# Objectives

The primary objectives of this document are to:

- Maintain architectural consistency.
- Ensure implementation quality.
- Prevent architectural violations.
- Standardize development practices.
- Reduce ambiguity during implementation.
- Improve maintainability.
- Enable scalable project growth.
- Provide consistent guidance for AI-assisted development.

---

# Scope

These rules apply to every part of the ProfitPilot project, including:

- Core workflow
- AI agents
- LangGraph orchestration
- Autonomous Reasoning Engine
- RAG implementation
- Data processing
- Business analysis
- Report generation
- Testing
- Documentation
- Future enhancements

No implementation is exempt from these rules.

---

# Target Audience

This document is intended for:

- Project Developers
- AI Coding Assistants
- Future Contributors
- Project Review Committee

---

# Relationship with Other Documents

The project documentation follows a layered structure.

```
PRD
        │
        ▼
Architecture
        │
        ▼
Rules
        │
        ▼
Implementation
```

Each document has a distinct responsibility.

| Document | Purpose |
|----------|---------|
| PRD | Defines what the product should achieve |
| Architecture | Defines how the system is designed |
| Rules | Defines how the system must be implemented |

The Rules Document does not replace the Architecture Document.

Instead, it enforces the architectural decisions established in `architecture.md`.

---

# Rule Authority

The rules contained within this document are mandatory.

Terms such as:

- **Must**
- **Must Not**
- **Shall**
- **Shall Not**

indicate mandatory requirements.

Terms such as:

- **May**
- **Can**
- **Should**

indicate optional implementation guidance.

Whenever a conflict exists between implementation convenience and these rules, the rules take precedence.

---

# AI-Assisted Development

ProfitPilot is expected to be developed with assistance from AI coding tools.

Therefore, these rules are written to be both human-readable and AI-readable.

Every AI coding assistant used during development must follow:

- `architecture.md`
- `rules.md`

before generating or modifying project code.

No generated code should violate the architectural principles or implementation rules defined in these documents.

---

# Design Philosophy

The rules defined in this document are intended to preserve:

- Modularity
- Explainability
- Maintainability
- Simplicity
- Consistency
- Scalability

Implementation decisions should always prioritize long-term architectural quality over short-term development convenience.

---

# Section Summary

This document establishes the mandatory engineering rules that govern the implementation of ProfitPilot.

Together with the Architecture Document, it provides a complete foundation for consistent, maintainable, and architecture-compliant development throughout the project lifecycle.

# 2. Development Philosophy

---

# Overview

The development philosophy defines the engineering mindset that guides the implementation of ProfitPilot.

It establishes the principles that influence every architectural decision, software component, AI agent, and implementation strategy throughout the project.

The philosophy ensures that implementation remains consistent with the architectural vision while maintaining software quality, modularity, and long-term maintainability.

---

# Philosophy 1

## Architecture Before Code

Implementation must always follow the architecture.

The architecture defines the structure, responsibilities, communication patterns, and boundaries of the system.

Code must implement the architecture.

The architecture must never be modified simply to simplify implementation.

Whenever implementation and architecture conflict, the architecture takes precedence.

---

# Philosophy 2

## Build the Core Before the Interface

ProfitPilot is an AI system before it is a software application.

The backend workflow must be fully functional before any graphical interface is developed.

Version 1 focuses entirely on validating the autonomous business intelligence workflow through the terminal.

Presentation layers should never influence backend design decisions.

---

# Philosophy 3

## Autonomous by Design

ProfitPilot is designed to operate as an autonomous system.

The objective is to minimize user intervention.

The user provides a single natural language prompt.

From that point onward, the system independently:

- Plans execution
- Collects data
- Processes data
- Performs analysis
- Retrieves business knowledge
- Generates business reasoning
- Produces actionable recommendations
- Generates the final report

Every implementation decision should strengthen this autonomous workflow.

---

# Philosophy 4

## Modular Development

Every architectural component should be implemented independently.

Modules should have:

- One responsibility
- Well-defined inputs
- Well-defined outputs
- Minimal dependencies

Each module should be testable without requiring the entire application to execute.

---

# Philosophy 5

## Explainability Before Complexity

ProfitPilot is an explainable AI system.

Every significant output should be understandable by developers and users.

The implementation should always favour transparent workflows over unnecessarily complex solutions.

If a simpler implementation provides the same capability, the simpler implementation should be preferred.

---

# Philosophy 6

## Evidence-Driven Intelligence

Business recommendations must always originate from evidence.

Evidence consists of:

- Business datasets
- Analytical findings
- Retrieved business knowledge

The system should never generate recommendations without sufficient supporting information.

Reasoning must always be grounded in available evidence.

---

# Philosophy 7

## Separation of Responsibilities

Every component must perform exactly one responsibility.

Responsibilities should never overlap.

For example:

- The Collector Agent collects data.
- The Processing Agent generates KPIs.
- The Analysis Agent produces insights.
- The Reasoning Engine performs reasoning.
- The Business Tactics Agent prepares recommendations.
- The Report Generation Agent presents results.

Implementation should preserve these boundaries.

---

# Philosophy 8

## Keep Components Replaceable

No implementation should tightly couple the system to a specific technology.

Where possible, components should be designed so that they can be replaced independently.

Examples include:

- Reasoning models
- Vector databases
- Databases
- User interfaces

Replacing one component should not require redesigning the entire system.

---

# Philosophy 9

## Incremental Development

ProfitPilot should be implemented incrementally.

Each completed phase should produce a functional and testable system.

Large incomplete implementations should be avoided.

Development should progress through small, verifiable improvements while preserving architectural integrity.

---

# Philosophy 10

## Quality Over Speed

Implementation quality takes precedence over rapid feature development.

Every module should be:

- Readable
- Maintainable
- Testable
- Well documented
- Consistent with the architecture

Temporary shortcuts that compromise long-term maintainability should be avoided.

---

# Philosophy 11

## AI-Assisted Development

AI coding assistants are development partners, not decision makers.

AI-generated code must always comply with:

- architecture.md
- rules.md

Generated code should be reviewed before integration into the project.

Architectural decisions must never be delegated entirely to AI.

---

# Philosophy 12

## Future-Proof Design

Implementation decisions should consider future evolution.

Where practical, solutions should support future enhancements without requiring significant architectural changes.

Examples include:

- User interfaces
- Enterprise integrations
- Cloud deployment
- Additional AI capabilities

Future expansion should be enabled through extension rather than redesign.

---

# Guiding Principles

The implementation of ProfitPilot should always prioritize:

- Simplicity
- Modularity
- Explainability
- Maintainability
- Scalability
- Consistency
- Architectural compliance

These principles should guide every implementation decision throughout the project.

---

# Section Summary

The development philosophy establishes the engineering mindset for implementing ProfitPilot.

By emphasizing architecture-first development, autonomous execution, modular design, explainability, and long-term maintainability, these principles ensure that every implementation decision contributes to a consistent, scalable, and high-quality autonomous business intelligence system.

# 3. Architecture Compliance Rules

---

# Overview

The Architecture Compliance Rules ensure that every implementation remains consistent with the architectural design defined in `architecture.md`.

These rules preserve the integrity of the system by preventing architectural drift during development.

Every source file, software module, AI agent, workflow, and future enhancement must comply with these rules.

No implementation may violate the architectural boundaries established in the Architecture Document.

---

# Rule 1

## Architecture Takes Precedence

The implementation must always follow the architecture defined in `architecture.md`.

Implementation convenience must never justify modifying the architecture.

If implementation conflicts with the architecture, the implementation shall be changed—not the architecture.

---

# Rule 2

## Preserve the Frozen Architecture

The Version 1 architecture is considered frozen.

The following architectural components must remain unchanged:

- Autonomous Reasoning Engine
- LangGraph Orchestrator
- Data Collector Agent
- Data Processing Agent
- Analysis Agent
- RAG Retrieval Layer
- Business Tactics Agent
- Report Generation Agent

No additional architectural components shall be introduced without revising the architecture document.

---

# Rule 3

## Preserve the Workflow

The workflow defined in `architecture.md` shall remain unchanged.

```
User Prompt
        │
        ▼
Planning
        │
        ▼
Orchestrator
        │
        ▼
Collector
        │
        ▼
Processor
        │
        ▼
Analysis
        │
        ▼
RAG
        │
        ▼
Reasoning
        │
        ▼
Business Tactics
        │
        ▼
Report
```

Components must not be reordered, skipped, or bypassed.

---

# Rule 4

## Maintain Single Responsibility

Every architectural component must perform one clearly defined responsibility.

Responsibilities shall never overlap.

Examples:

- Collector Agent collects data.
- Processing Agent computes KPIs.
- Analysis Agent performs analysis.
- RAG retrieves knowledge.
- Reasoning Engine performs reasoning.
- Business Tactics Agent prepares recommendations.
- Report Generation Agent presents results.

Responsibilities must never be duplicated.

---

# Rule 5

## Preserve Centralized Orchestration

All workflow execution shall be coordinated exclusively by the LangGraph Orchestrator.

No component shall invoke another component directly.

Every interaction between architectural components must occur through the Orchestrator.

---

# Rule 6

## Preserve Planning Before Execution

Every workflow must begin with a Planning stage.

The Planning stage is responsible for:

- Understanding the user objective.
- Determining the required workflow.
- Producing the execution plan.

Workflow execution must not begin before planning has completed.

---

# Rule 7

## Preserve Evidence-Based Reasoning

The Autonomous Reasoning Engine shall only reason using available evidence.

Evidence includes:

- Business KPIs
- Analytical findings
- Retrieved business knowledge

The reasoning engine shall not generate unsupported business conclusions.

---

# Rule 8

## Preserve RAG Independence

The RAG Retrieval Layer shall remain an independent architectural component.

The RAG layer:

- Retrieves knowledge.
- Ranks retrieved information.
- Supplies context.

The RAG layer shall never:

- Perform reasoning.
- Generate recommendations.
- Execute business analysis.

---

# Rule 9

## Preserve Recommendation Flow

Business recommendations must always originate from business reasoning.

The workflow shall remain:

```
Evidence
        │
        ▼
Business Reasoning
        │
        ▼
Business Recommendations
```

Recommendations must never be generated directly from analytical outputs.

---

# Rule 10

## Preserve Terminal-First Development

Version 1 shall remain terminal-based.

All architectural components must be fully operational before introducing any graphical user interface.

User interface development shall not influence backend architecture.

---

# Rule 11

## Preserve Modular Boundaries

Architectural modules must remain independent.

No module shall directly access the internal implementation of another module.

Communication must occur only through defined architectural interfaces.

---

# Rule 12

## Preserve Data Ownership

Every architectural component owns its own output.

Components may consume outputs from previous stages but shall not modify data owned by other components.

Data ownership defined in `architecture.md` must be preserved.

---

# Rule 13

## Preserve Explainability

Every recommendation presented to the user must be supported by business reasoning.

Business reasoning must be supported by:

- Business KPIs
- Analytical findings
- Retrieved knowledge

The implementation shall always preserve this chain of evidence.

---

# Rule 14

## Preserve Version 1 Scope

Version 1 is intended to validate the autonomous workflow only.

Features outside this scope shall not be implemented until the core workflow is complete.

Examples include:

- Authentication
- React frontend
- Cloud deployment
- Multi-user support
- Enterprise integrations

These features belong to future versions.

---

# Rule 15

## Preserve Architecture Documentation

Whenever a major architectural change is approved, the following documents must be updated together:

- architecture.md
- rules.md
- phases.md
- memory.md

Documentation shall remain synchronized with the implementation.

---

# Compliance Checklist

Before merging any implementation, verify the following.

- Architecture has not been modified.
- Workflow remains unchanged.
- Agent responsibilities remain unchanged.
- Components remain modular.
- Orchestration remains centralized.
- Recommendations originate from reasoning.
- RAG remains retrieval-only.
- Version 1 scope has not expanded.
- Documentation remains synchronized.

Every item in this checklist must be satisfied before implementation is considered architecture-compliant.

---

# Section Summary

The Architecture Compliance Rules establish the mandatory constraints that preserve the integrity of the ProfitPilot architecture.

By enforcing centralized orchestration, modularity, evidence-based reasoning, and strict separation of responsibilities, these rules ensure that every implementation remains faithful to the architectural vision established in `architecture.md`.

# 4. General Development Rules

---

# Overview

The General Development Rules establish the mandatory engineering practices that govern the implementation of ProfitPilot.

These rules apply to every source file, module, function, class, script, and future enhancement within the project.

The objective is to maintain a clean, modular, maintainable, and scalable codebase throughout the development lifecycle.

Every contributor, whether human or AI-assisted, must comply with these rules.

---

# Rule 1

## Develop One Responsibility at a Time

Every implementation task must focus on one clearly defined responsibility.

Large features should be decomposed into smaller independent modules.

No implementation should attempt to solve multiple architectural responsibilities simultaneously.

---

# Rule 2

## Build Incrementally

Development shall proceed in small, verifiable increments.

Each completed implementation should produce a working and testable result before moving to the next feature.

Large unfinished implementations should be avoided.

---

# Rule 3

## Never Break Existing Functionality

New code must not modify or break previously validated functionality.

Whenever new features are introduced, existing workflows must continue to function correctly.

Backward compatibility shall be preserved within Version 1.

---

# Rule 4

## Keep Code Readable

Code should prioritize readability over cleverness.

Every implementation should be understandable by another developer without requiring extensive explanation.

Readable code is preferred over unnecessarily optimized or complex solutions.

---

# Rule 5

## Minimize Complexity

Implement the simplest solution that satisfies the architectural requirements.

Avoid introducing unnecessary abstractions, design patterns, or dependencies.

Complexity should only be introduced when it provides a measurable architectural benefit.

---

# Rule 6

## Prefer Composition Over Duplication

Common functionality should be reused through shared modules or helper functions.

Code duplication should be eliminated whenever practical.

Business logic should never be copied across multiple components.

---

# Rule 7

## Keep Modules Small

Modules should remain focused and manageable.

If a module becomes difficult to understand or contains multiple unrelated responsibilities, it should be refactored into smaller modules.

Large monolithic files should be avoided.

---

# Rule 8

## One Feature Per Implementation

Each implementation session should focus on completing one feature.

Partially implemented features should not be mixed with unrelated development work.

This simplifies testing, debugging, and version control.

---

# Rule 9

## Preserve Consistency

Implementation should remain consistent across the entire project.

Consistency should be maintained in:

- Project organization
- Module structure
- Function organization
- Naming conventions
- Error handling
- Logging

Consistency improves maintainability and readability.

---

# Rule 10

## Avoid Premature Optimization

Optimization should only occur after functionality has been validated.

The initial objective is correctness and architectural compliance.

Performance improvements may be introduced later when supported by measurable evidence.

---

# Rule 11

## Minimize External Dependencies

Only introduce external libraries when they provide clear architectural value.

Before adding a dependency, verify that:

- Existing project components cannot solve the problem.
- The dependency aligns with project objectives.
- The dependency is actively maintained.
- The dependency is compatible with the existing architecture.

Unnecessary dependencies should be avoided.

---

# Rule 12

## Configuration Must Remain External

Configuration values must never be hardcoded inside the application.

Examples include:

- API keys
- File paths
- Model locations
- Database connections
- Environment-specific values

Configuration should remain separate from application logic.

---

# Rule 13

## Fail Clearly

Applications should fail with meaningful messages.

Unexpected silent failures should never occur.

Whenever execution cannot continue, the system should provide sufficient information to understand:

- What failed
- Where it failed
- Why it failed

Error messages should assist debugging without exposing internal implementation details.

---

# Rule 14

## Keep Business Logic Independent

Business logic should remain independent from:

- User interfaces
- Configuration
- Storage
- Logging
- Utility modules

Business logic belongs only within the architectural components responsible for business intelligence.

---

# Rule 15

## Validate Before Integration

Every newly implemented module should be validated before being integrated into the larger workflow.

Validation should occur as close as possible to the implementation stage.

Broken modules should never be merged into the main workflow.

---

# Rule 16

## Preserve Project Simplicity

The implementation should remain approachable for future developers.

Solutions that significantly increase complexity without providing proportional value should be rejected.

Maintainability should always outweigh implementation novelty.

---

# Development Checklist

Before considering an implementation complete, verify the following.

- The implementation follows the architecture.
- The implementation satisfies its assigned responsibility.
- Existing functionality remains unaffected.
- No unnecessary complexity has been introduced.
- No duplicate business logic exists.
- Configuration remains external.
- Error handling is present.
- The module has been validated.
- The implementation remains readable and maintainable.

Every implementation should satisfy this checklist before progressing to the next development task.

---

# Section Summary

The General Development Rules establish the engineering practices required to build ProfitPilot in a structured, maintainable, and scalable manner.

By emphasizing simplicity, modularity, incremental development, readability, and architectural consistency, these rules ensure that implementation quality remains high throughout the project's lifecycle.

# 5. Coding Standards

---

# Overview

The Coding Standards define the mandatory software engineering practices that govern the implementation of every source file within ProfitPilot.

These standards ensure that the codebase remains readable, maintainable, testable, modular, and consistent regardless of whether the code is written by a human developer or generated using AI-assisted development tools.

Every Python module, class, function, and script within the project shall comply with these standards.

---

# Rule 1

## Every Module Must Have a Single Responsibility

Each source file shall implement one clearly defined responsibility.

A module should not contain unrelated business logic.

When a module begins implementing multiple independent responsibilities, it shall be divided into smaller modules.

---

# Rule 2

## Every Function Must Have One Responsibility

Each function shall perform one logical operation.

Functions should be easy to understand and easy to test.

Large functions performing multiple independent operations shall be refactored.

---

# Rule 3

## Every Public Function Must Have Documentation

Every public function shall include a descriptive docstring.

The documentation should clearly describe:

- Purpose
- Parameters
- Return value
- Possible exceptions

Documentation should explain **why** the function exists rather than repeating the implementation.

---

# Rule 4

## Type Hints Are Mandatory

Every public function shall use explicit type hints.

Type hints improve:

- Readability
- Static analysis
- IDE support
- AI-assisted development

Unannotated public interfaces should be avoided.

---

# Rule 5

## Functions Should Produce Predictable Results

Functions should avoid hidden behaviour.

Given the same input, a function should produce consistent output unless explicitly designed otherwise.

Unexpected side effects should be avoided.

---

# Rule 6

## Avoid Hidden Side Effects

Functions should not unexpectedly modify external state.

Whenever state modification is required, it should be explicit and easy to identify.

Predictable behaviour improves maintainability and testing.

---

# Rule 7

## Prefer Explicit Return Values

Functions should return meaningful values instead of relying on shared or global state.

Data should flow through function inputs and outputs rather than hidden dependencies.

---

# Rule 8

## Business Logic Must Remain Independent

Business logic shall exist only within the architectural components responsible for business intelligence.

Business logic must never be implemented inside:

- Utility modules
- Configuration files
- Logging modules
- Entry-point scripts

---

# Rule 9

## Avoid Hardcoded Values

Implementation should avoid hardcoded values wherever practical.

Examples include:

- File paths
- API keys
- Model locations
- Database connections
- Threshold values
- Configuration parameters

Configuration should remain external to application logic.

---

# Rule 10

## Use Meaningful Names

Variables, functions, classes, and modules shall use descriptive names that communicate their purpose.

Names should improve readability without requiring additional explanation.

Abbreviations should be avoided unless they are widely understood within the project.

---

# Rule 11

## Minimize Nesting

Implementation should avoid excessive nesting.

Deeply nested logic reduces readability and increases maintenance difficulty.

Where possible, simplify conditional logic through early validation and clear control flow.

---

# Rule 12

## Keep Dependencies Explicit

Modules should explicitly import only the dependencies they require.

Unused imports and unnecessary dependencies should be removed.

Dependency relationships should remain clear and minimal.

---

# Rule 13

## Handle Exceptions Intentionally

Exceptions should be handled deliberately.

Generic exception handling should be avoided unless it provides meaningful recovery or reporting.

Exceptions should never be silently ignored.

---

# Rule 14

## Avoid Duplicate Business Logic

Business logic should exist in only one location within the project.

If similar logic is required elsewhere, it should be extracted into an appropriate shared component.

Code duplication increases maintenance cost and inconsistency.

---

# Rule 15

## Prefer Readability Over Cleverness

Code should be written for maintainability rather than novelty.

Readable implementations are preferred over highly optimized but difficult-to-understand solutions unless performance requirements justify additional complexity.

---

# Rule 16

## Keep Modules Testable

Every module should be designed to support independent testing.

Modules should minimize unnecessary external dependencies and expose clear interfaces.

Testing should not require the complete application to execute.

---

# Rule 17

## Preserve Architectural Boundaries

Implementation shall respect the architectural boundaries defined in `architecture.md`.

No source file may introduce responsibilities outside the scope of its assigned architectural component.

---

# Rule 18

## Remove Dead Code

Unused functions, variables, modules, and experimental implementations should not remain in the project.

The repository should contain only code that contributes to the current implementation.

---

# Rule 19

## Maintain Consistent Error Messages

Error messages should be:

- Clear
- Actionable
- Consistent
- Informative

Messages should describe the problem without exposing unnecessary implementation details.

---

# Rule 20

## Review Before Integration

Before integrating any implementation into the project, verify that:

- The code satisfies its intended responsibility.
- The implementation follows the architecture.
- The implementation follows these coding standards.
- No unnecessary complexity has been introduced.
- Existing functionality remains unaffected.

Every implementation should be reviewed before becoming part of the project.

---

# Coding Principles

All code written for ProfitPilot should satisfy the following principles.

- Readable
- Modular
- Maintainable
- Testable
- Predictable
- Consistent
- Architecture-compliant
- AI-friendly

These principles should guide every implementation decision throughout the project.

---

# Section Summary

The Coding Standards establish the mandatory engineering practices for writing high-quality software within ProfitPilot.

By emphasizing readability, modularity, predictability, explicit design, and architectural compliance, these standards ensure that the implementation remains maintainable, scalable, and consistent throughout the project's evolution.

# 6. Project Structure Rules

---

# Overview

The Project Structure Rules define the mandatory organizational principles for the ProfitPilot codebase.

The objective is to ensure that the project structure directly reflects the system architecture defined in `architecture.md`.

Every directory, module, and source file shall have a clearly defined responsibility.

The project structure must remain consistent throughout the development lifecycle.

---

# Rule 1

## The Project Structure Must Mirror the Architecture

The project directory structure shall directly correspond to the architectural components defined in `architecture.md`.

Major architectural components shall be implemented as independent project modules.

Examples include:

- Agents
- LangGraph Orchestrator
- Autonomous Reasoning Engine
- RAG Layer
- Data Layer
- Reporting Layer

The implementation structure must never contradict the architecture.

---

# Rule 2

## One Directory, One Responsibility

Each project directory shall have one clearly defined purpose.

Directories shall not contain unrelated implementations.

Examples:

- `agents/` contains only AI agents.
- `core/` contains workflow execution logic.
- `llm/` contains reasoning engine implementation.
- `knowledge_base/` contains retrieval components.
- `data/` contains datasets and generated data.
- `reports/` contains report generation logic.

Responsibilities must remain separated.

---

# Rule 3

## Modules Must Remain Independent

Modules shall be designed for independent development and testing.

A module should not depend on the internal implementation details of another module.

Communication shall occur only through well-defined interfaces.

---

# Rule 4

## Entry Point Must Remain Minimal

The application's entry point (`main.py`) shall only be responsible for:

- Starting the application.
- Loading configuration.
- Initializing the workflow.
- Invoking the LangGraph Orchestrator.

`main.py` must never contain:

- Business logic
- Data processing
- Analysis
- Business reasoning
- Recommendation generation

---

# Rule 5

## Business Logic Must Stay Inside Architectural Components

Business logic shall only exist inside the component responsible for that responsibility.

Examples:

- Dataset validation belongs to the Collector Agent.
- KPI calculation belongs to the Processing Agent.
- Forecasting belongs to the Analysis Agent.
- Business reasoning belongs to the Autonomous Reasoning Engine.

Business logic shall never be implemented elsewhere.

---

# Rule 6

## Utility Modules Must Remain Generic

The `utils/` directory shall contain only reusable helper functions.

Utility modules must never contain:

- Business rules
- Workflow logic
- Agent logic
- AI reasoning
- Dataset-specific processing

Utility functions should be reusable across multiple components.

---

# Rule 7

## Configuration Must Remain Centralized

Application configuration shall be managed through dedicated configuration modules.

Configuration values must never be duplicated across the project.

Examples include:

- Model paths
- Database connections
- File locations
- Environment variables

Configuration shall remain independent from business logic.

---

# Rule 8

## Data Directories Must Remain Organized

Business datasets shall be organized according to their role within the workflow.

Examples include:

- Raw datasets
- Clean datasets
- Processed datasets
- Generated outputs

Intermediate execution artifacts should not overwrite original datasets.

Original data must always remain preserved.

---

# Rule 9

## Documentation Must Remain Separate

Project documentation shall remain inside the dedicated documentation directory.

Documentation files include:

- PRD
- Architecture
- Rules
- Phases
- Design
- Memory

Documentation should never be mixed with implementation files.

---

# Rule 10

## Tests Must Reflect Project Structure

The testing structure should mirror the implementation structure.

Each architectural component should have corresponding unit and integration tests.

Testing modules should remain organized and independent.

---

# Rule 11

## Logging Must Remain Isolated

Logging functionality shall remain independent from business logic.

Architectural components should report execution events without implementing logging behaviour directly.

Logging implementation should remain centralized.

---

# Rule 12

## Reports Must Remain Independent

Report generation shall remain isolated from workflow execution.

Architectural components should produce outputs required for reporting.

Only the Report Generation Agent shall determine how results are presented.

---

# Rule 13

## Avoid Circular Dependencies

Project modules shall not depend on each other in a circular manner.

Dependencies should always follow the architectural direction defined in `architecture.md`.

Circular imports and cyclic dependencies shall be avoided.

---

# Rule 14

## New Modules Require Architectural Justification

Before introducing a new top-level directory or major module, verify that:

- An existing component cannot fulfil the responsibility.
- The new module aligns with the architecture.
- The responsibility is independent.

Unnecessary project expansion should be avoided.

---

# Rule 15

## Preserve Future Extensibility

The project structure should support future enhancements without requiring major reorganization.

Examples include:

- Additional AI models
- New analytical modules
- New report formats
- Future frontend integration

Expansion should occur through extension rather than restructuring.

---

# Project Organization Principles

The project shall always remain:

- Modular
- Predictable
- Organized
- Scalable
- Easy to navigate
- Architecture-compliant

Developers should be able to understand the project structure without reading the implementation.

---

# Section Summary

The Project Structure Rules ensure that the organization of the ProfitPilot codebase remains consistent with its architecture.

By enforcing clear module boundaries, centralized configuration, independent responsibilities, and scalable organization, these rules provide a maintainable foundation for long-term development while preserving architectural integrity.

# 7. AI Agent Development Rules

---

# Overview

The AI Agent Development Rules define the mandatory engineering standards for implementing every autonomous agent within ProfitPilot.

These rules ensure that all agents behave consistently, remain modular, and comply with the architecture defined in `architecture.md`.

Every agent, regardless of its responsibility, shall follow these implementation rules.

These rules apply to:

- Data Collector Agent
- Data Processing Agent
- Analysis Agent
- Business Tactics Agent
- Report Generation Agent
- Any future architectural agent introduced through an approved architecture revision

---

# Rule 1

## Every Agent Must Have One Responsibility

Each agent shall perform exactly one architectural responsibility.

Responsibilities must never overlap.

Examples:

- Collector Agent collects and validates data.
- Processing Agent generates KPIs.
- Analysis Agent performs business analysis.
- Business Tactics Agent prepares recommendations.
- Report Generation Agent generates reports.

Agents shall never perform responsibilities assigned to another agent.

---

# Rule 2

## Agents Must Be Independent

Every agent shall be implemented as an independent module.

Agents should be developed, tested, and maintained independently.

Implementation inside one agent should not require modifying another agent.

---

# Rule 3

## Agents Must Never Communicate Directly

Agents shall never invoke another agent.

Examples of prohibited behaviour include:

- Calling another agent's methods.
- Importing another agent's internal implementation.
- Sharing internal state.

All communication shall occur exclusively through the LangGraph Orchestrator.

---

# Rule 4

## Every Agent Must Validate Its Input

Before beginning execution, every agent shall validate the received input.

Validation should verify:

- Required information exists.
- Data format is correct.
- Input is suitable for processing.

Invalid input should immediately terminate the agent's execution and return a meaningful error.

---

# Rule 5

## Every Agent Must Validate Its Output

Before returning results, every agent shall verify that its output is complete and valid.

Only validated outputs may be passed back to the LangGraph Orchestrator.

Incomplete or invalid outputs must never propagate through the workflow.

---

# Rule 6

## Agents Must Remain Stateless

Agents shall not permanently store workflow state.

Each execution should depend only on:

- Received input
- Configuration
- External resources required by the architecture

Workflow state shall be managed exclusively by the LangGraph Orchestrator.

---

# Rule 7

## Agents Must Produce Deterministic Outputs

Given the same input and execution context, an agent should produce consistent output whenever practical.

Unexpected behaviour should be avoided.

Predictable execution simplifies debugging, testing, and maintenance.

---

# Rule 8

## Agents Must Not Perform Workflow Management

Agents shall never determine:

- Execution order
- Workflow transitions
- Component scheduling
- State management

These responsibilities belong exclusively to the LangGraph Orchestrator.

---

# Rule 9

## Agents Must Not Perform Autonomous Reasoning

Business reasoning shall only be performed by the Autonomous Reasoning Engine.

Agents must never:

- Infer business strategy.
- Generate unsupported conclusions.
- Replace reasoning with heuristic logic.

Agents prepare information for reasoning; they do not perform reasoning themselves.

---

# Rule 10

## Agents Must Not Modify Another Agent's Output

Each agent owns its generated output.

Agents may consume outputs produced by previous stages but shall never modify them.

Every transformation should produce a new output rather than altering previous results.

---

# Rule 11

## Agents Must Handle Errors Gracefully

Agents shall detect and report execution failures.

Whenever execution cannot continue, the agent should:

- Stop processing.
- Return meaningful error information.
- Preserve available execution context.

Agents should never fail silently.

---

# Rule 12

## Agents Must Produce Observable Execution

Every significant execution stage should generate meaningful progress information.

Typical events include:

- Execution started.
- Processing.
- Validation.
- Completion.
- Failure.

Execution visibility improves transparency and debugging.

---

# Rule 13

## Agents Must Be Easily Testable

Every agent shall support independent testing.

Testing an agent should not require executing the complete workflow.

Dependencies should remain minimal and well defined.

---

# Rule 14

## Agents Must Remain Replaceable

Agent implementations should remain independent of specific technologies whenever practical.

Replacing the implementation of one agent should not require changes to other agents.

Only the external interface should remain stable.

---

# Rule 15

## Agents Must Preserve Architecture Compliance

Every agent implementation shall comply with:

- architecture.md
- rules.md

No agent shall introduce responsibilities, workflows, or communication patterns that violate the architecture.

---

# Standard Agent Lifecycle

Every agent should conceptually follow the same execution lifecycle.

```
Receive Input
        │
        ▼
Validate Input
        │
        ▼
Execute Responsibility
        │
        ▼
Validate Output
        │
        ▼
Return Result
```

This lifecycle should remain consistent across all architectural agents.

---

# Agent Design Principles

Every agent should be:

- Independent
- Modular
- Stateless
- Testable
- Predictable
- Explainable
- Replaceable
- Architecture-compliant

These principles apply to every present and future agent within ProfitPilot.

---

# Section Summary

The AI Agent Development Rules establish the implementation standards for every autonomous agent within ProfitPilot.

By enforcing independence, single responsibility, stateless execution, centralized orchestration, and consistent validation, these rules ensure that all agents remain modular, maintainable, and fully aligned with the architectural principles defined in the Software Architecture Document.

# 8. LangGraph Rules

---

# Overview

The LangGraph Rules define the mandatory implementation standards governing the orchestration layer of ProfitPilot.

LangGraph is responsible for coordinating the execution of the autonomous business intelligence workflow.

Within ProfitPilot, LangGraph functions as the centralized workflow engine responsible for:

- Workflow execution
- State management
- Component coordination
- Context propagation
- Execution lifecycle management

LangGraph shall never assume responsibilities assigned to architectural components such as reasoning, analysis, or business recommendation generation.

---

# Rule 1

## LangGraph Is the Only Workflow Orchestrator

LangGraph shall be the sole component responsible for workflow orchestration.

No alternative orchestration mechanisms shall exist within the project.

Workflow execution must always begin through the LangGraph Orchestrator.

---

# Rule 2

## Workflow State Must Be Centrally Managed

Workflow state shall be maintained exclusively by LangGraph.

Architectural components shall never manage or persist workflow state independently.

The workflow state represents the single source of truth throughout execution.

---

# Rule 3

## Every Workflow Must Begin with Planning

The first executable stage of every workflow shall be the Planning stage.

The Planning stage is responsible for:

- Understanding the user objective
- Producing an execution plan
- Initializing workflow execution

No architectural component shall execute before planning has completed.

---

# Rule 4

## Nodes Represent Architectural Responsibilities

Every LangGraph node shall correspond to exactly one architectural responsibility.

Examples include:

- Data Collection
- Data Processing
- Business Analysis
- Knowledge Retrieval
- Business Reasoning
- Business Tactics
- Report Generation

Nodes shall not combine multiple architectural responsibilities.

---

# Rule 5

## Nodes Must Remain Independent

Each node shall execute independently.

A node must depend only on:

- Workflow state
- Configuration
- Approved external resources

Nodes shall not directly depend on the internal implementation of other nodes.

---

# Rule 6

## Nodes Must Never Invoke Other Nodes

Workflow transitions shall be controlled exclusively by LangGraph.

Nodes shall never:

- Execute another node
- Import another node's implementation
- Determine the next workflow stage

Node sequencing belongs solely to the LangGraph Orchestrator.

---

# Rule 7

## Workflow State Must Flow Sequentially

Each node receives the current workflow state, performs its assigned responsibility, and returns an updated workflow state.

Nodes should only modify the portion of the workflow state that belongs to their architectural responsibility.

Previously generated information should remain intact unless explicitly updated by the responsible component.

---

# Rule 8

## Workflow Execution Must Remain Observable

The Orchestrator shall record workflow progress throughout execution.

At minimum, each node should indicate:

- Execution started
- Execution completed
- Execution failed

Workflow progress should always be visible during terminal execution.

---

# Rule 9

## Preserve Execution Order

The workflow shall follow the architectural execution sequence defined in `architecture.md`.

Execution order shall not be modified during implementation.

The LangGraph implementation must preserve the approved workflow.

---

# Rule 10

## Context Must Be Passed Through Workflow State

Architectural components shall exchange information exclusively through the workflow state.

Information required by downstream components should be added to the workflow state rather than passed through global variables or direct communication.

The workflow state shall remain the only shared execution context.

---

# Rule 11

## Nodes Must Handle Failures Gracefully

Each node shall validate its execution before returning control to the Orchestrator.

If execution cannot continue:

- The failure should be reported.
- Workflow state should remain valid.
- Meaningful error information should be returned.

The node shall never terminate the application directly.

---

# Rule 12

## Workflow Must Be Deterministic

Given identical inputs and execution context, the workflow should follow the same execution path whenever practical.

Unexpected workflow behaviour should be avoided.

Predictable execution simplifies debugging and testing.

---

# Rule 13

## Workflow State Must Remain Consistent

Workflow state shall always remain internally consistent.

Nodes must not:

- Remove required information.
- Corrupt existing state.
- Produce incomplete workflow data.

Every node is responsible for validating its updates before returning the workflow state.

---

# Rule 14

## LangGraph Must Not Contain Business Logic

The Orchestrator shall only coordinate execution.

Business logic shall remain within the architectural components responsible for:

- Data collection
- Data processing
- Analysis
- Reasoning
- Recommendation generation
- Reporting

The orchestration layer must remain independent of business intelligence logic.

---

# Rule 15

## Preserve Architectural Separation

The LangGraph implementation shall respect all architectural boundaries defined in `architecture.md`.

The Orchestrator coordinates execution but never replaces the responsibilities of individual architectural components.

---

# Standard Workflow Pattern

Every ProfitPilot workflow should conceptually follow the same execution pattern.

```
Initialize Workflow
        │
        ▼
Planning
        │
        ▼
Collector
        │
        ▼
Processor
        │
        ▼
Analysis
        │
        ▼
RAG
        │
        ▼
Reasoning
        │
        ▼
Business Tactics
        │
        ▼
Report
        │
        ▼
Complete Workflow
```

This execution pattern shall remain consistent throughout Version 1.

---

# LangGraph Design Principles

The orchestration layer should remain:

- Centralized
- Predictable
- Modular
- Observable
- Stateless with respect to business logic
- Architecture-compliant

The workflow engine coordinates execution but does not participate in business intelligence.

---

# Section Summary

The LangGraph Rules establish the mandatory implementation standards for the orchestration layer of ProfitPilot.

By enforcing centralized workflow management, sequential execution, consistent workflow state, and strict separation from business logic, these rules ensure that LangGraph remains a reliable and maintainable execution engine while preserving the architectural integrity of the system.

# 9. Autonomous Reasoning Engine Rules

---

# Overview

The Autonomous Reasoning Engine is the intelligence core of ProfitPilot.

It is responsible for understanding user objectives, planning workflow execution, interpreting business evidence, applying retrieved knowledge, and generating structured business reasoning.

Within ProfitPilot, the Autonomous Reasoning Engine is implemented using DeepAnalyze-8B.

No other architectural component shall perform autonomous reasoning.

---

# Rule 1

## The Autonomous Reasoning Engine Is the Only Reasoning Component

Business reasoning shall only be performed by the Autonomous Reasoning Engine.

No other architectural component shall:

- Infer business strategy.
- Generate business conclusions.
- Produce business reasoning.
- Replace autonomous reasoning with hardcoded rules.

Reasoning responsibilities shall remain centralized.

---

# Rule 2

## The Reasoning Engine Must Operate in Two Modes

The reasoning engine shall support two execution modes.

### Planning Mode

Responsible for:

- Understanding user intent.
- Identifying business objectives.
- Producing the execution plan.

---

### Business Reasoning Mode

Responsible for:

- Interpreting analytical evidence.
- Applying retrieved business knowledge.
- Producing business reasoning.

Both modes shall use the same reasoning engine while remaining logically independent.

---

# Rule 3

## Planning Must Always Precede Execution

Planning Mode shall execute before any workflow activity begins.

The execution plan must be generated before the LangGraph Orchestrator invokes architectural components.

Workflow execution shall never bypass the Planning stage.

---

# Rule 4

## Reasoning Must Be Evidence-Driven

Business reasoning shall always be based on available evidence.

Evidence consists of:

- Business KPIs
- Analytical findings
- Retrieved business knowledge

Business reasoning shall never rely on unsupported assumptions.

---

# Rule 5

## Recommendations Must Never Be Generated Directly

The reasoning engine produces:

- Business reasoning

The reasoning engine does not produce:

- Final recommendations
- Reports
- Business tactics

Recommendations shall always be generated by the Business Tactics Agent using the reasoning produced by the Autonomous Reasoning Engine.

---

# Rule 6

## Retrieved Knowledge Must Be Used as Context

Retrieved business knowledge shall support reasoning rather than replace it.

The reasoning engine should:

- Interpret retrieved knowledge.
- Relate knowledge to analytical findings.
- Apply knowledge where appropriate.

Retrieved documents shall not be reproduced without interpretation.

---

# Rule 7

## Preserve Explainability

Every business conclusion should be traceable to available evidence.

Reasoning should demonstrate a logical relationship between:

- Analytical findings
- Retrieved knowledge
- Business conclusions

The reasoning process should remain transparent and understandable.

---

# Rule 8

## Business Reasoning Must Remain Structured

Business reasoning should follow a consistent internal structure.

Typical reasoning should include:

- Interpretation of findings
- Supporting evidence
- Business implications
- Strategic understanding

The exact implementation format is an implementation decision, but consistency shall be maintained throughout the project.

---

# Rule 9

## Do Not Invent Business Evidence

The reasoning engine shall never fabricate:

- Business metrics
- Analytical results
- Retrieved knowledge
- Dataset values

Business reasoning must remain grounded in information generated during workflow execution.

---

# Rule 10

## Reasoning Must Remain Independent

The reasoning engine shall not:

- Access datasets directly.
- Execute business analysis.
- Retrieve knowledge independently.
- Coordinate workflow execution.

The reasoning engine operates only on validated information received from architectural components.

---

# Rule 11

## Validate Reasoning Output

Before returning business reasoning, the reasoning engine shall verify that:

- Reasoning has been generated.
- Business conclusions are coherent.
- Supporting evidence exists.
- Output is complete.

Incomplete reasoning shall not proceed to the Business Tactics Agent.

---

# Rule 12

## Preserve Deterministic Workflow Behaviour

While the reasoning process may involve probabilistic AI models, workflow behaviour shall remain predictable.

The reasoning engine should produce consistent business reasoning when provided with equivalent business context.

Unexpected reasoning behaviour should be minimized wherever practical.

---

# Rule 13

## Separate Reasoning from Presentation

The reasoning engine shall focus exclusively on business understanding.

It shall not concern itself with:

- Terminal formatting
- Report layout
- User interface presentation
- Export formats

Presentation responsibilities belong exclusively to the Report Generation Agent.

---

# Rule 14

## Preserve Architectural Independence

The reasoning engine shall remain independent from:

- LangGraph implementation
- Data persistence
- User interface
- Logging implementation

Only its architectural interfaces should be visible to the remainder of the system.

---

# Rule 15

## Maintain Architecture Compliance

Every implementation of the Autonomous Reasoning Engine shall comply with:

- architecture.md
- rules.md

No implementation shall modify its architectural responsibilities without updating the architecture documentation.

---

# Standard Reasoning Lifecycle

The Autonomous Reasoning Engine should conceptually follow the following lifecycle.

```
Receive Context
        │
        ▼
Validate Input
        │
        ▼
Interpret Evidence
        │
        ▼
Apply Business Knowledge
        │
        ▼
Generate Business Reasoning
        │
        ▼
Validate Reasoning
        │
        ▼
Return Result
```

This lifecycle should remain consistent across all reasoning operations.

---

# Reasoning Principles

The Autonomous Reasoning Engine should remain:

- Evidence-driven
- Explainable
- Independent
- Modular
- Predictable
- Architecture-compliant
- Focused solely on reasoning

Business reasoning should always precede business recommendations.

---

# Section Summary

The Autonomous Reasoning Engine Rules establish the implementation standards for the intelligence core of ProfitPilot.

By enforcing evidence-driven reasoning, clear separation of planning and reasoning, structured outputs, and strict architectural boundaries, these rules ensure that the reasoning engine remains explainable, reliable, and fully aligned with the autonomous business intelligence workflow defined in the Software Architecture Document.

# 10. RAG Rules

---

# Overview

The Retrieval-Augmented Generation (RAG) layer provides external business knowledge that supports autonomous business reasoning.

Its responsibility is to retrieve relevant domain knowledge from the prepared knowledge base and provide that information to the Autonomous Reasoning Engine.

The RAG layer shall never perform reasoning, generate business conclusions, or replace the responsibilities of the Autonomous Reasoning Engine.

Within ProfitPilot, the knowledge base is prepared once before application execution and remains available for retrieval throughout runtime.

---

# Rule 1

## The RAG Layer Is Retrieval Only

The RAG layer shall only retrieve relevant knowledge.

It shall never:

- Perform business reasoning.
- Generate recommendations.
- Produce business conclusions.
- Execute analytical operations.
- Modify retrieved knowledge.

Its sole responsibility is knowledge retrieval.

---

# Rule 2

## The Knowledge Base Must Be Prepared Before Runtime

The knowledge base shall be created before the application is executed.

Preparation includes:

- Document collection.
- Text preprocessing.
- Text chunking.
- Embedding generation.
- Vector database indexing.

The application shall never rebuild the knowledge base during normal workflow execution.

---

# Rule 3

## Runtime Shall Perform Retrieval Only

During workflow execution, the RAG layer shall:

- Receive retrieval requests.
- Search the vector database.
- Rank relevant documents.
- Return retrieved knowledge.

Runtime execution shall never perform:

- Embedding generation.
- Document indexing.
- Knowledge base construction.

---

# Rule 4

## Retrieved Knowledge Must Be Relevant

The RAG layer should return knowledge that is relevant to:

- User objective.
- Business context.
- Analytical findings.

Irrelevant information should not be returned to the Autonomous Reasoning Engine.

---

# Rule 5

## Preserve Knowledge Integrity

Retrieved documents shall remain unchanged.

The RAG layer must not:

- Rewrite documents.
- Summarize documents.
- Interpret documents.
- Modify document content.

Knowledge interpretation belongs exclusively to the Autonomous Reasoning Engine.

---

# Rule 6

## The Knowledge Base Must Remain Independent

The knowledge base shall remain independent from:

- Business datasets.
- Workflow state.
- Business analysis.
- Business reasoning.

Business datasets and business knowledge represent separate architectural resources.

---

# Rule 7

## Separate Business Data from Business Knowledge

Business datasets are used for analysis.

Business knowledge is used for reasoning.

These two information sources shall remain independent throughout implementation.

The RAG layer retrieves business knowledge only.

It shall never retrieve analytical data.

---

# Rule 8

## Validate Retrieved Results

Before returning retrieved knowledge, the RAG layer shall verify that:

- Relevant documents exist.
- Retrieved content is valid.
- Retrieval completed successfully.

If no relevant knowledge is available, the workflow should continue while reporting the absence of supporting knowledge.

---

# Rule 9

## Preserve Modular Design

The implementation of the RAG layer shall remain modular.

The following responsibilities should remain logically independent:

- Document preparation.
- Embedding generation.
- Vector storage.
- Similarity search.
- Knowledge retrieval.

Implementation details may evolve without changing architectural responsibilities.

---

# Rule 10

## The RAG Layer Must Remain Replaceable

The implementation shall not depend on a specific vector database.

Replacing the underlying vector database should not require changes to:

- LangGraph
- AI Agents
- Autonomous Reasoning Engine
- Business Logic

Only the retrieval interface should remain stable.

---

# Rule 11

## Avoid Duplicate Knowledge

The same document should not be indexed multiple times.

Duplicate knowledge increases storage requirements and may reduce retrieval quality.

Knowledge preparation should ensure document uniqueness.

---

# Rule 12

## Preserve Retrieval Performance

Knowledge retrieval should remain efficient.

Knowledge preparation should optimize runtime retrieval rather than runtime preprocessing.

The majority of computational work should occur before application execution.

---

# Rule 13

## Handle Retrieval Failures Gracefully

If retrieval cannot be completed:

- Report the failure.
- Preserve workflow state.
- Return meaningful status information.

The RAG layer shall never terminate workflow execution directly.

Failure handling remains the responsibility of the LangGraph Orchestrator.

---

# Rule 14

## Maintain Architecture Compliance

The implementation of the RAG layer shall comply with:

- architecture.md
- rules.md

The RAG layer shall not assume responsibilities belonging to other architectural components.

---

# Rule 15

## Preserve Explainability

Whenever knowledge contributes to business reasoning, the retrieved information should remain traceable.

The workflow should make it possible to determine:

- What knowledge was retrieved.
- Why it was retrieved.
- Where it influenced business reasoning.

Knowledge retrieval should remain transparent throughout workflow execution.

---

# Standard Retrieval Lifecycle

Every retrieval request should conceptually follow the same lifecycle.

```
Receive Retrieval Request
        │
        ▼
Validate Request
        │
        ▼
Search Vector Database
        │
        ▼
Rank Relevant Documents
        │
        ▼
Validate Retrieved Knowledge
        │
        ▼
Return Retrieved Knowledge
```

This lifecycle should remain consistent throughout the implementation.

---

# RAG Design Principles

The RAG implementation should remain:

- Retrieval-only
- Modular
- Independent
- Replaceable
- Explainable
- Efficient
- Architecture-compliant

The RAG layer supplies knowledge.

The Autonomous Reasoning Engine transforms that knowledge into business understanding.

---

# Section Summary

The RAG Rules establish the implementation standards for the knowledge retrieval subsystem of ProfitPilot.

By enforcing retrieval-only behaviour, pre-built knowledge bases, modular implementation, and strict separation from reasoning, these rules ensure that the RAG layer remains efficient, maintainable, and fully aligned with the architectural principles defined in the Software Architecture Document.

# 11. Data Processing Rules

---

# Overview

The Data Processing Rules define the mandatory implementation standards governing data ingestion, validation, preprocessing, transformation, and KPI generation within ProfitPilot.

The objective of the Data Processing layer is to transform raw business datasets into reliable, structured business metrics that can be consumed by the Analysis Agent.

The Data Processing layer shall never perform business reasoning or recommendation generation.

---

# Rule 1

## All Data Must Be Validated Before Processing

Every dataset shall undergo validation before any processing begins.

Validation shall include:

- File availability
- File format
- Required columns
- Missing values
- Data types
- Duplicate records

Processing shall not begin until validation is complete.

---

# Rule 2

## Raw Data Must Never Be Modified

The original business datasets shall remain unchanged.

Cleaning and preprocessing shall always produce a new dataset.

The original data serves as the immutable source of truth.

---

# Rule 3

## Missing Data Must Be Handled Explicitly

Missing values shall never be ignored.

Each missing value should be:

- Removed
- Replaced
- Imputed
- Reported

The chosen strategy shall remain consistent throughout the project.

---

# Rule 4

## Duplicate Records Must Be Managed

Duplicate business records should be identified during preprocessing.

Duplicate handling shall be:

- Consistent
- Documented
- Observable

The processing pipeline shall not silently remove data without recording the action.

---

# Rule 5

## Data Types Must Be Standardized

Every business attribute shall use a consistent data type before processing.

Examples include:

- Dates
- Currency values
- Numerical quantities
- Categorical values

Invalid data types should be corrected or rejected before further processing.

---

# Rule 6

## Business KPIs Must Be Generated Only by the Data Processing Agent

Only the Data Processing Agent shall generate business KPIs.

Examples include:

- Revenue
- Profit
- Profit Margin
- ROI
- Inventory Turnover
- Customer Lifetime Value

No other architectural component shall calculate business KPIs.

---

# Rule 7

## Processing Must Be Deterministic

Given identical business datasets, the processing stage should produce identical outputs.

Unexpected variability should be avoided.

Consistent processing improves reproducibility and testing.

---

# Rule 8

## Preserve Data Lineage

Every processed dataset should remain traceable to its original source.

The processing pipeline should preserve the relationship between:

- Raw data
- Clean data
- Processed data
- Generated KPIs

Traceability supports debugging and explainability.

---

# Rule 9

## Data Processing Must Remain Independent

The Data Processing Agent shall remain independent from:

- Business reasoning
- Knowledge retrieval
- Recommendation generation
- Report formatting

Its sole responsibility is transforming validated data into structured business metrics.

---

# Rule 10

## Validate Generated KPIs

Before returning processed results, the Data Processing Agent shall verify that:

- KPI calculations completed successfully.
- Required metrics are available.
- Results are internally consistent.

Invalid KPI outputs shall not proceed to the Analysis Agent.

---

# Rule 11

## Preserve Processing Transparency

Every significant processing step should be observable.

Typical processing stages include:

- Dataset loaded
- Validation completed
- Missing values handled
- Duplicates processed
- KPIs generated

These stages should be visible through the project's logging system.

---

# Rule 12

## Handle Processing Failures Gracefully

If processing cannot continue:

- Stop processing safely.
- Report the failure.
- Preserve available execution context.
- Return meaningful status information.

The Data Processing Agent shall never terminate the workflow directly.

---

# Rule 13

## Avoid Hardcoded Dataset Assumptions

The processing pipeline should avoid assumptions specific to a single dataset.

Processing logic should remain adaptable to compatible business datasets.

Dataset-specific behaviour should be configurable rather than hardcoded.

---

# Rule 14

## Preserve Architectural Boundaries

The Data Processing layer shall comply with:

- architecture.md
- rules.md

It shall never assume responsibilities belonging to:

- Analysis Agent
- Autonomous Reasoning Engine
- Business Tactics Agent
- Report Generation Agent

---

# Rule 15

## Output Must Be Analysis Ready

The final output of the Data Processing Agent must be suitable for immediate consumption by the Analysis Agent.

No additional preprocessing should be required before business analysis begins.

---

# Standard Processing Lifecycle

Every processing task should conceptually follow the same lifecycle.

```
Receive Dataset
        │
        ▼
Validate Dataset
        │
        ▼
Clean Data
        │
        ▼
Transform Data
        │
        ▼
Generate Business KPIs
        │
        ▼
Validate Results
        │
        ▼
Return Processed Data
```

This lifecycle should remain consistent across all data processing operations.

---

# Data Processing Principles

The Data Processing layer should remain:

- Reliable
- Deterministic
- Transparent
- Modular
- Independent
- Reproducible
- Architecture-compliant

The purpose of this layer is to transform business data into reliable analytical evidence.

---

# Section Summary

The Data Processing Rules establish the implementation standards for transforming raw business datasets into structured business metrics within ProfitPilot.

By enforcing rigorous validation, deterministic processing, transparent transformations, and strict architectural boundaries, these rules ensure that every downstream component receives reliable and consistent business information for analysis, reasoning, and recommendation generation.

# 12. Business Analysis Rules

---

# Overview

The Business Analysis Rules define the mandatory implementation standards governing analytical operations within ProfitPilot.

The Analysis Agent is responsible for transforming business KPIs into structured analytical insights that describe the current state and behaviour of the business.

The Analysis Agent shall not perform business reasoning, recommendation generation, or workflow orchestration.

Its sole responsibility is producing reliable analytical evidence for the Autonomous Reasoning Engine.

---

# Rule 1

## The Analysis Agent Shall Perform Analysis Only

The Analysis Agent shall only perform analytical operations.

It shall never:

- Perform business reasoning.
- Generate business recommendations.
- Retrieve business knowledge.
- Coordinate workflow execution.
- Produce reports.

Analytical responsibilities shall remain independent from reasoning and decision-making.

---

# Rule 2

## Analysis Shall Be Based on Validated Business KPIs

The Analysis Agent shall operate only on validated outputs produced by the Data Processing Agent.

Raw datasets shall never be analysed directly.

The Analysis Agent assumes that all received business metrics have already completed validation and preprocessing.

---

# Rule 3

## Analysis Must Produce Evidence

The primary output of the Analysis Agent is business evidence.

Examples include:

- Sales trends
- Revenue patterns
- Profit trends
- Customer behaviour
- Product performance
- Regional performance
- Inventory trends
- Forecast results
- Detected anomalies

These outputs become evidence for autonomous reasoning.

---

# Rule 4

## Separate Observation from Interpretation

The Analysis Agent shall describe what the data indicates.

Examples include:

- Sales increased.
- Revenue declined.
- Inventory turnover decreased.
- Customer retention improved.

The Analysis Agent shall not explain why these observations occurred.

Interpretation belongs exclusively to the Autonomous Reasoning Engine.

---

# Rule 5

## Analytical Methods Must Remain Independent

Each analytical capability should remain logically independent.

Examples include:

- Trend analysis
- Forecasting
- Anomaly detection
- Product analysis
- Customer analysis
- Regional analysis

The failure of one analytical operation should not prevent unrelated analyses from executing whenever practical.

---

# Rule 6

## Preserve Analytical Transparency

Every analytical result should be traceable to its supporting business metrics.

The Analysis Agent should avoid producing conclusions that cannot be supported by processed business data.

Analytical outputs should remain explainable and reproducible.

---

# Rule 7

## Forecasting Shall Remain Analytical

Forecasting is considered an analytical operation.

Forecast results shall be treated as business evidence.

Forecasting shall not directly generate recommendations or business strategies.

---

# Rule 8

## Detect Anomalies Without Interpretation

The Analysis Agent may identify unusual business behaviour.

Examples include:

- Unexpected revenue decline.
- Inventory spikes.
- Sales outliers.
- Abnormal customer activity.

The Analysis Agent shall report anomalies without attempting to determine their business causes.

---

# Rule 9

## Validate Analytical Outputs

Before returning results, the Analysis Agent shall verify that:

- Analysis completed successfully.
- Required insights were generated.
- Outputs are internally consistent.
- No invalid analytical results exist.

Only validated analytical outputs shall be passed to the next stage.

---

# Rule 10

## Preserve Analytical Independence

The Analysis Agent shall remain independent from:

- LangGraph implementation
- Data collection
- Data persistence
- Knowledge retrieval
- Business reasoning
- Recommendation generation

Its responsibility ends after producing business insights.

---

# Rule 11

## Handle Analytical Failures Gracefully

If an analytical operation cannot be completed:

- Report the failure.
- Preserve completed analytical outputs.
- Continue independent analyses where appropriate.
- Return meaningful execution information.

The Analysis Agent shall never terminate workflow execution directly.

---

# Rule 12

## Maintain Deterministic Analysis

Given identical business metrics and analytical configuration, the Analysis Agent should produce consistent analytical results whenever practical.

Analytical behaviour should remain predictable and reproducible.

---

# Rule 13

## Preserve Architecture Compliance

The Analysis Agent shall comply with:

- architecture.md
- rules.md

It shall never assume responsibilities assigned to:

- Autonomous Reasoning Engine
- Business Tactics Agent
- Report Generation Agent

Architectural boundaries shall remain unchanged.

---

# Rule 14

## Prepare Outputs for Reasoning

The Analysis Agent shall produce outputs that are immediately consumable by:

- RAG Retrieval Layer
- Autonomous Reasoning Engine

No additional analytical processing should be required after the Analysis stage.

---

# Rule 15

## Business Insights Must Remain Structured

Business insights should remain organized and consistent.

Analytical outputs should clearly distinguish between different categories of evidence.

Examples include:

- Trends
- Forecasts
- Anomalies
- Product performance
- Customer behaviour
- Regional performance

Consistency simplifies downstream reasoning.

---

# Standard Analysis Lifecycle

Every analytical operation should conceptually follow the following lifecycle.

```
Receive Business KPIs
        │
        ▼
Validate Input
        │
        ▼
Perform Analysis
        │
        ▼
Generate Business Insights
        │
        ▼
Validate Insights
        │
        ▼
Return Analytical Results
```

This lifecycle should remain consistent across all analytical operations.

---

# Business Analysis Principles

The Analysis Agent should remain:

- Objective
- Evidence-based
- Independent
- Explainable
- Reproducible
- Modular
- Architecture-compliant

The Analysis Agent describes the business.

It does not explain the business.

---

# Section Summary

The Business Analysis Rules establish the implementation standards for generating analytical evidence within ProfitPilot.

By enforcing strict separation between observation and interpretation, ensuring analytical transparency, validating outputs, and preserving architectural boundaries, these rules ensure that the Analysis Agent provides reliable, explainable, and structured business insights that serve as the foundation for autonomous reasoning.

# 13. Report Generation Rules

---

# Overview

The Report Generation Rules define the mandatory implementation standards governing the presentation of workflow results within ProfitPilot.

The Report Generation Agent is the final architectural component executed during the autonomous business intelligence workflow.

Its responsibility is to transform validated outputs from previous architectural components into a structured, understandable, and explainable report.

The Report Generation Agent shall never perform business reasoning, business analysis, knowledge retrieval, or recommendation generation.

---

# Rule 1

## The Report Generation Agent Is a Presentation Component

The Report Generation Agent shall only present information.

It shall never:

- Perform analysis.
- Generate business reasoning.
- Retrieve knowledge.
- Create business recommendations.
- Modify analytical outputs.

Its responsibility is limited to organizing and presenting workflow results.

---

# Rule 2

## Reports Must Represent Workflow Outputs

Every section of the report shall originate from validated outputs produced during workflow execution.

Examples include:

- Business KPIs
- Business insights
- Retrieved knowledge
- Business reasoning
- Business recommendations

The Report Generation Agent shall never invent new information.

---

# Rule 3

## Preserve Explainability

The report should clearly demonstrate how the final recommendations were produced.

The report should preserve the relationship between:

Business Data

↓

Business Analysis

↓

Retrieved Knowledge

↓

Business Reasoning

↓

Business Recommendations

This chain of evidence should remain visible throughout the report.

---

# Rule 4

## Reports Must Be Structured

The report should present information in a consistent order.

Typical sections include:

- User Objective
- Business KPIs
- Analytical Findings
- Retrieved Knowledge Summary
- Business Reasoning
- Business Recommendations
- Workflow Summary

Presentation consistency should be maintained across all executions.

---

# Rule 5

## Preserve Information Integrity

The Report Generation Agent shall faithfully represent information produced by previous architectural components.

It shall not:

- Modify business metrics.
- Alter analytical findings.
- Change business reasoning.
- Rewrite recommendations.

Presentation should preserve the integrity of workflow outputs.

---

# Rule 6

## Reports Must Remain Readable

Reports should prioritize clarity over complexity.

Information should be organized in a logical sequence that allows users to understand the progression from data to recommendations.

The report should remain understandable without requiring knowledge of the internal implementation.

---

# Rule 7

## Terminal Output Is the Primary Report Format

Version 1 of ProfitPilot shall present reports through the terminal.

The terminal report represents the official output of the autonomous workflow.

Additional presentation formats may be introduced in future versions without modifying the reporting architecture.

---

# Rule 8

## Report Generation Must Remain Independent

The Report Generation Agent shall remain independent from:

- LangGraph implementation
- Business analysis
- Knowledge retrieval
- Autonomous reasoning
- Business tactics

It shall only consume validated workflow outputs.

---

# Rule 9

## Reports Must Reflect Workflow Completion

The report shall only be generated after successful completion of the autonomous workflow.

Partial reports shall only be generated when explicitly supported by the workflow design.

Incomplete workflow execution shall not produce a final business report.

---

# Rule 10

## Preserve Workflow Transparency

The report should communicate:

- What was analysed.
- What knowledge was retrieved.
- What reasoning was generated.
- What recommendations were produced.

Users should understand how the workflow progressed from the initial prompt to the final output.

---

# Rule 11

## Handle Report Generation Failures Gracefully

If report generation cannot be completed:

- Report the failure.
- Preserve workflow outputs.
- Return meaningful execution information.

The Report Generation Agent shall never terminate the application directly.

Workflow failure management remains the responsibility of the LangGraph Orchestrator.

---

# Rule 12

## Reports Must Be Deterministic

Given identical workflow outputs, the generated report should remain consistent.

Presentation should not vary unnecessarily between executions.

Consistent reporting improves reproducibility and usability.

---

# Rule 13

## Preserve Architectural Compliance

The Report Generation Agent shall comply with:

- architecture.md
- rules.md

It shall never assume responsibilities assigned to:

- Analysis Agent
- Autonomous Reasoning Engine
- Business Tactics Agent

Architectural boundaries shall remain unchanged.

---

# Rule 14

## Reports Must Support Future Expansion

The reporting architecture should support future presentation formats without modifying report generation logic.

Examples include:

- Terminal reports
- PDF reports
- HTML reports
- Dashboard views
- API responses

The reporting component should remain presentation-independent.

---

# Rule 15

## Every Workflow Must Produce a Final Summary

Every completed workflow should conclude with a structured summary.

The summary should include:

- Workflow status
- Business objective
- Key analytical findings
- Business reasoning summary
- Actionable recommendations

This summary represents the final output of the autonomous workflow.

---

# Standard Report Generation Lifecycle

Every reporting operation should conceptually follow the following lifecycle.

```
Receive Workflow Outputs
        │
        ▼
Validate Inputs
        │
        ▼
Organize Information
        │
        ▼
Generate Report
        │
        ▼
Validate Report
        │
        ▼
Present Final Output
```

This lifecycle should remain consistent throughout the implementation.

---

# Report Generation Principles

The Report Generation Agent should remain:

- Independent
- Deterministic
- Explainable
- Readable
- Consistent
- Presentation-focused
- Architecture-compliant

The Report Generation Agent presents knowledge.

It does not generate knowledge.

---

# Section Summary

The Report Generation Rules establish the implementation standards for presenting workflow results within ProfitPilot.

By enforcing presentation-only responsibilities, preserving explainability, maintaining information integrity, and supporting structured reporting, these rules ensure that every autonomous workflow concludes with a clear, consistent, and trustworthy business report while preserving the architectural separation between intelligence and presentation.

# 14. Fault Tolerance & Error Handling Rules

---

# Overview

The Fault Tolerance & Error Handling Rules define the mandatory implementation standards governing failure detection, validation, recovery, and error reporting throughout ProfitPilot.

As an autonomous business intelligence system, ProfitPilot must remain robust against unexpected failures while preserving workflow integrity and architectural consistency.

Every architectural component shall detect failures within its own responsibility, report them clearly, and allow the LangGraph Orchestrator to determine the appropriate workflow action.

Unexpected application termination should be avoided whenever possible.

---

# Rule 1

## Every Component Must Validate Its Inputs

Every architectural component shall validate all required inputs before execution begins.

Validation should verify:

- Required data exists.
- Data format is valid.
- Required dependencies are available.
- Input satisfies the component's expectations.

Execution shall not continue with invalid input.

---

# Rule 2

## Every Component Must Validate Its Outputs

Before returning control to the LangGraph Orchestrator, every component shall verify that:

- Processing completed successfully.
- Output is complete.
- Output is internally consistent.
- Required information has been produced.

Invalid outputs shall not propagate through the workflow.

---

# Rule 3

## Detect Failures at Their Source

Failures should be detected by the architectural component in which they occur.

Components shall not assume downstream components will detect upstream failures.

Early detection simplifies debugging and improves workflow reliability.

---

# Rule 4

## Fail Gracefully

Whenever execution cannot continue, the affected component shall:

- Stop safely.
- Preserve execution context.
- Report meaningful failure information.
- Return control to the LangGraph Orchestrator.

Components shall never terminate the application directly.

---

# Rule 5

## Never Continue with Invalid Data

Invalid data shall never be passed to downstream components.

Whenever validation fails:

- Stop processing.
- Report the failure.
- Prevent invalid workflow progression.

Workflow integrity always takes priority over workflow completion.

---

# Rule 6

## Error Messages Must Be Meaningful

Error messages should clearly communicate:

- What failed.
- Where the failure occurred.
- Why execution failed.
- Whether recovery is possible.

Messages should support debugging without exposing unnecessary implementation details.

---

# Rule 7

## Preserve Workflow State

Workflow state shall remain valid even when failures occur.

Components shall never corrupt or partially overwrite workflow state.

The LangGraph Orchestrator remains responsible for preserving workflow consistency.

---

# Rule 8

## Distinguish Recoverable and Non-Recoverable Failures

Recoverable failures include situations where workflow execution may continue safely.

Examples include:

- Missing optional knowledge.
- Empty retrieval results.
- Minor data quality warnings.

Non-recoverable failures include situations where meaningful execution cannot continue.

Examples include:

- Missing business dataset.
- Corrupted workflow state.
- Invalid execution plan.
- Failure of the Autonomous Reasoning Engine.

Failure severity should be communicated clearly.

---

# Rule 9

## Preserve Partial Results

Whenever practical, successfully completed workflow outputs should be preserved even if later stages fail.

Previously validated outputs should not be discarded unnecessarily.

This improves debugging and future recovery capabilities.

---

# Rule 10

## Components Must Remain Responsible for Their Own Errors

Every architectural component shall detect and report failures within its own responsibility.

Examples include:

- Collector Agent validates datasets.
- Processing Agent validates KPIs.
- Analysis Agent validates insights.
- RAG validates retrieval results.
- Autonomous Reasoning Engine validates reasoning.
- Report Generation Agent validates reports.

Responsibility for error detection shall remain local to each component.

---

# Rule 11

## Exceptions Must Never Be Ignored

Exceptions shall never be silently suppressed.

Every exception should result in one of the following:

- Recovery.
- Meaningful reporting.
- Graceful workflow termination.

Silent failures reduce observability and complicate debugging.

---

# Rule 12

## Preserve Observability

Every execution failure shall be observable through the project's logging system.

Failure information should include:

- Component name.
- Workflow stage.
- Failure category.
- Execution status.

This information improves transparency and debugging.

---

# Rule 13

## Recovery Must Preserve Architecture

Recovery mechanisms shall never violate architectural boundaries.

Components shall not assume responsibilities belonging to other architectural components in an attempt to recover from failures.

Architectural integrity shall always be preserved.

---

# Rule 14

## Maintain Architecture Compliance

All fault handling implementations shall comply with:

- architecture.md
- rules.md

Failure handling must never introduce architectural shortcuts or bypass approved workflow stages.

---

# Rule 15

## Prepare for Future Recovery Strategies

Version 1 focuses on graceful failure handling.

Future versions may introduce:

- Automatic retries.
- Checkpoint recovery.
- Workflow resumption.
- Intelligent recovery strategies.

The current implementation should not prevent these future enhancements.

---

# Standard Failure Lifecycle

Every failure should conceptually follow the following lifecycle.

```
Detect Failure
        │
        ▼
Validate Failure
        │
        ▼
Classify Severity
        │
        ▼
Record Failure
        │
        ▼
Return Control
        │
        ▼
LangGraph Determines Next Action
```

This lifecycle should remain consistent across all architectural components.

---

# Fault Handling Principles

The fault handling system should remain:

- Predictable
- Observable
- Modular
- Explainable
- Recoverable where practical
- Architecture-compliant

Failures should be managed in a controlled manner while preserving workflow integrity.

---

# Section Summary

The Fault Tolerance & Error Handling Rules establish the implementation standards for managing failures throughout ProfitPilot.

By enforcing early validation, meaningful error reporting, graceful failure handling, workflow integrity, and strict architectural compliance, these rules ensure that the autonomous business intelligence workflow remains reliable, transparent, and maintainable even when unexpected execution failures occur.

# 15. Logging Rules

---

# Overview

The Logging Rules define the mandatory implementation standards governing execution visibility throughout ProfitPilot.

Logging is considered an architectural feature rather than a debugging utility.

The objective of logging is to provide complete transparency into the autonomous workflow by allowing users and developers to observe every significant stage of execution.

Every architectural component shall produce meaningful execution logs while preserving the separation between logging and business logic.

---

# Rule 1

## Every Workflow Must Be Observable

Every execution of ProfitPilot shall produce observable terminal output.

The user should always know:

- What stage is currently executing.
- Which architectural component is active.
- Whether execution succeeded or failed.

No stage of the workflow should execute silently.

---

# Rule 2

## Every Architectural Component Must Report Its Execution

Each architectural component shall report:

- Execution started.
- Current activity.
- Execution completed.
- Execution failed.

Examples include:

- Planning
- Data Collection
- Data Processing
- Business Analysis
- Knowledge Retrieval
- Business Reasoning
- Business Tactics
- Report Generation

Execution progress should remain visible throughout the workflow.

---

# Rule 3

## Logs Must Describe Workflow Progress

Logs should explain what the system is doing rather than how it is implemented.

Examples include:

- Loading business dataset...
- Validating dataset...
- Calculating business KPIs...
- Performing trend analysis...
- Retrieving business knowledge...
- Generating business reasoning...
- Producing business recommendations...
- Generating final report...

Implementation-specific details should remain hidden unless required for debugging.

---

# Rule 4

## Logging Must Remain Independent

Logging shall remain separate from business logic.

Architectural components should report execution events without implementing logging behaviour directly.

Logging implementation should remain centralized and reusable.

---

# Rule 5

## Preserve Execution Order in Logs

The terminal output shall reflect the actual workflow execution order.

The log sequence should mirror the architecture.

```
Planning
        │
        ▼
Collector
        │
        ▼
Processor
        │
        ▼
Analysis
        │
        ▼
RAG
        │
        ▼
Reasoning
        │
        ▼
Business Tactics
        │
        ▼
Report
```

Users should be able to understand workflow progression by reading the logs.

---

# Rule 6

## Display Meaningful Intermediate Outputs

Whenever practical, important intermediate results should be displayed.

Examples include:

- Dataset successfully loaded.
- Number of records processed.
- KPIs generated.
- Trends detected.
- Number of knowledge documents retrieved.
- Business reasoning completed.
- Recommendations generated.

Intermediate outputs improve transparency and user confidence.

---

# Rule 7

## Preserve Consistent Log Structure

Logs should follow a consistent presentation throughout the project.

Each log entry should clearly communicate:

- Active component.
- Current operation.
- Execution status.

Consistency improves readability and debugging.

---

# Rule 8

## Errors Must Be Clearly Logged

Whenever execution fails, logs should clearly indicate:

- Workflow stage.
- Responsible component.
- Failure description.
- Execution status.

Failures should never be hidden from the user.

---

# Rule 9

## Logs Must Never Alter Workflow Behaviour

Logging shall be observational only.

Removing or disabling logging should not affect workflow execution or business logic.

Logging should remain independent from system behaviour.

---

# Rule 10

## Preserve Explainability Through Logging

The logging system should demonstrate how the workflow progresses from the initial user prompt to the final report.

The execution path should remain understandable without inspecting the source code.

Logging contributes directly to the explainability of the autonomous system.

---

# Rule 11

## Sensitive Information Must Not Be Logged

Logs shall not expose confidential or sensitive information.

Examples include:

- API keys
- Authentication credentials
- Environment variables
- Internal secrets
- Private user information

Logging should balance transparency with security.

---

# Rule 12

## Preserve Terminal-First Development

Version 1 shall use terminal output as the primary execution interface.

The terminal should display the complete lifecycle of the autonomous workflow.

Future presentation layers may extend logging without replacing terminal observability.

---

# Rule 13

## Every Workflow Must End With a Summary

After successful execution, the logging system should present a concise execution summary.

The summary should include:

- Workflow status.
- Components executed.
- Business objective.
- Report generation status.
- Total execution duration.

This summary confirms successful workflow completion.

---

# Rule 14

## Maintain Architecture Compliance

The logging implementation shall comply with:

- architecture.md
- rules.md

Logging shall never introduce business logic or violate architectural responsibilities.

---

# Rule 15

## Logging Must Support Future Expansion

The logging architecture should support future enhancements without requiring major redesign.

Examples include:

- File-based logging.
- Structured logs.
- Execution history.
- Performance metrics.
- Audit trails.
- Dashboard monitoring.

Version 1 focuses exclusively on terminal-based execution visibility.

---

# Standard Logging Lifecycle

Every architectural component should conceptually follow the following logging lifecycle.

```
Execution Started
        │
        ▼
Current Operation
        │
        ▼
Intermediate Progress
        │
        ▼
Execution Completed
        │
        ▼
Workflow Summary
```

This lifecycle should remain consistent throughout the implementation.

---

# Logging Principles

The logging system should remain:

- Observable
- Consistent
- Explainable
- Independent
- Informative
- Non-intrusive
- Architecture-compliant

Logging exists to make the autonomous workflow transparent without influencing its behaviour.

---

# Section Summary

The Logging Rules establish the implementation standards for execution visibility within ProfitPilot.

By enforcing consistent workflow reporting, meaningful progress updates, structured terminal output, and clear separation from business logic, these rules ensure that every autonomous workflow remains transparent, explainable, and easy to monitor while preserving the architectural integrity of the system.

# 16. Testing Rules

---

# Overview

The Testing Rules define the mandatory implementation standards governing software verification within ProfitPilot.

Testing ensures that every architectural component performs its assigned responsibility correctly while preserving the integrity of the autonomous business intelligence workflow.

Testing shall verify both individual architectural components and the complete end-to-end workflow.

Every implementation introduced into the project shall be validated before integration.

---

# Rule 1

## Every Architectural Component Must Be Testable

Each architectural component shall support independent testing.

Components should be testable without requiring execution of the complete application.

Examples include:

- Data Collector Agent
- Data Processing Agent
- Analysis Agent
- RAG Retrieval Layer
- Autonomous Reasoning Engine
- Business Tactics Agent
- Report Generation Agent

Independent testing simplifies debugging and maintenance.

---

# Rule 2

## Validate Every Component Independently

Every architectural component shall be validated before integration.

Validation should verify:

- Input handling.
- Output generation.
- Responsibility boundaries.
- Error handling.
- Architecture compliance.

A component shall not be integrated until it has successfully completed individual testing.

---

# Rule 3

## Preserve Architectural Responsibilities

Testing shall verify that every component performs only its assigned responsibility.

Examples include:

- The Analysis Agent performs analysis only.
- The Autonomous Reasoning Engine performs reasoning only.
- The Report Generation Agent performs presentation only.

Architectural boundaries shall remain unchanged during testing.

---

# Rule 4

## Verify Workflow Execution

The complete autonomous workflow shall be tested from the initial user prompt to the final report.

The workflow should verify:

- Planning.
- Workflow orchestration.
- Data collection.
- Data processing.
- Business analysis.
- Knowledge retrieval.
- Business reasoning.
- Recommendation generation.
- Report generation.

The workflow shall complete without requiring additional user interaction.

---

# Rule 5

## Validate Workflow State

Testing shall verify that workflow state remains valid throughout execution.

Every architectural component should:

- Receive valid workflow state.
- Produce valid workflow state.
- Preserve information generated by previous stages.

Workflow state consistency shall be maintained from beginning to end.

---

# Rule 6

## Validate Business Evidence

Testing shall confirm that analytical evidence is produced correctly.

Evidence includes:

- Business KPIs.
- Business insights.
- Forecast results.
- Detected anomalies.

The quality of downstream reasoning depends on the quality of generated evidence.

---

# Rule 7

## Validate Knowledge Retrieval

Testing shall verify that the RAG layer:

- Retrieves relevant documents.
- Returns valid results.
- Preserves knowledge integrity.
- Handles empty retrieval gracefully.

Knowledge retrieval should remain independent from reasoning.

---

# Rule 8

## Validate Business Reasoning

Testing shall verify that business reasoning:

- Uses available evidence.
- Uses retrieved knowledge.
- Produces structured reasoning.
- Avoids unsupported conclusions.

Business reasoning should remain explainable and evidence-driven.

---

# Rule 9

## Validate Recommendation Generation

Testing shall verify that business recommendations:

- Originate from business reasoning.
- Remain actionable.
- Remain relevant to the business objective.

Recommendations shall never bypass the reasoning stage.

---

# Rule 10

## Validate Report Generation

Testing shall verify that the final report:

- Includes all required sections.
- Preserves workflow outputs.
- Presents information consistently.
- Remains readable and explainable.

The report shall faithfully represent workflow execution.

---

# Rule 11

## Validate Fault Handling

Testing shall verify that every architectural component correctly handles failures.

Examples include:

- Missing datasets.
- Invalid inputs.
- Empty retrieval results.
- Model failures.
- Report generation failures.

Failure handling shall remain consistent with the architecture.

---

# Rule 12

## Validate Logging

Testing shall verify that:

- Every workflow stage produces terminal output.
- Component execution remains observable.
- Errors are logged clearly.
- Workflow completion is reported.

Logging should accurately represent workflow execution.

---

# Rule 13

## Preserve Deterministic Behaviour

Whenever practical, identical inputs should produce consistent workflow behaviour.

Testing should verify that:

- Workflow execution order remains unchanged.
- Architectural responsibilities remain consistent.
- Outputs remain predictable within acceptable limits.

---

# Rule 14

## Regression Testing Is Mandatory

Whenever a component is modified, previously validated functionality shall be tested again.

New implementations shall not introduce regressions into existing workflow stages.

Regression testing shall preserve system stability throughout development.

---

# Rule 15

## Validate Architecture Compliance

Every completed implementation shall be evaluated against:

- architecture.md
- rules.md

Testing shall verify that implementation remains fully compliant with the approved architecture.

---

# Standard Testing Lifecycle

Every implementation should conceptually follow the following testing lifecycle.

```
Implement Feature
        │
        ▼
Unit Testing
        │
        ▼
Component Validation
        │
        ▼
Integration Testing
        │
        ▼
End-to-End Workflow Testing
        │
        ▼
Architecture Compliance Review
        │
        ▼
Merge Implementation
```

This lifecycle should remain consistent throughout the project.

---

# Testing Principles

Testing within ProfitPilot should remain:

- Systematic
- Independent
- Repeatable
- Explainable
- Architecture-driven
- Workflow-oriented
- Quality-focused

Testing exists to verify architectural correctness rather than simply detecting software defects.

---

# Section Summary

The Testing Rules establish the implementation standards for verifying the correctness, reliability, and architectural compliance of ProfitPilot.

By enforcing independent component validation, end-to-end workflow verification, regression testing, and architecture-focused quality assurance, these rules ensure that every implementation maintains the integrity, reliability, and explainability of the autonomous business intelligence system.

# 17. Documentation Rules

---

# Overview

The Documentation Rules define the mandatory implementation standards governing all project documentation within ProfitPilot.

Documentation is considered an essential engineering artifact rather than an optional development activity.

Every architectural decision, implementation, module, workflow, and major feature shall be documented sufficiently to support future development, maintenance, and AI-assisted implementation.

Documentation shall remain synchronized with the implementation throughout the project lifecycle.

---

# Rule 1

## Documentation Is Mandatory

Every major implementation shall be accompanied by appropriate documentation.

Documentation shall exist for:

- Architectural components.
- AI agents.
- Workflow execution.
- Configuration.
- Project setup.
- Major implementation decisions.
- Public interfaces.

Undocumented major implementations shall be considered incomplete.

---

# Rule 2

## Documentation Must Reflect Implementation

Documentation shall accurately describe the current implementation.

Documentation must never describe functionality that does not exist.

Whenever implementation changes, the corresponding documentation shall be updated.

Implementation and documentation shall remain synchronized.

---

# Rule 3

## Architecture Is the Source of Truth

The Software Architecture Document (`architecture.md`) defines the approved system design.

Implementation documentation shall never contradict the architecture.

Whenever architectural changes are approved, all related documentation shall be updated accordingly.

---

# Rule 4

## Rules Document Governs Implementation

The Rules Document (`rules.md`) defines mandatory implementation standards.

Every implementation should remain consistent with the rules established in this document.

Documentation shall reinforce these implementation standards rather than duplicate them.

---

# Rule 5

## Project Memory Must Remain Current

The project memory document (`memory.md`) shall be updated throughout development.

Typical updates include:

- Current implementation status.
- Completed phases.
- Active development tasks.
- Architectural decisions.
- Known issues.
- Next implementation steps.

The memory document serves as the project's ongoing development record.

---

# Rule 6

## Phase Documentation Must Remain Accurate

The project phase document (`phases.md`) shall accurately reflect implementation progress.

Completed phases should be marked accordingly.

Future phases should remain aligned with the project roadmap.

Phase documentation should never misrepresent project status.

---

# Rule 7

## Public Interfaces Must Be Documented

Every public class, module, and function should include documentation describing:

- Purpose.
- Inputs.
- Outputs.
- Responsibilities.

Documentation should explain why the interface exists rather than describing implementation details.

---

# Rule 8

## Explain Architectural Decisions

Whenever a significant implementation decision is made, the rationale should be documented.

Examples include:

- Technology selection.
- Model replacement.
- Architectural modifications.
- Workflow changes.
- Major optimizations.

The reasoning behind important decisions should remain available for future reference.

---

# Rule 9

## Avoid Duplicate Documentation

Information should exist in one authoritative location whenever practical.

Examples include:

- Architecture → architecture.md
- Implementation rules → rules.md
- Project requirements → prd.md
- Development progress → memory.md

Documentation should reference authoritative sources rather than duplicate them.

---

# Rule 10

## Documentation Must Be Readable

Documentation should prioritize clarity and organization.

Every document should:

- Follow consistent formatting.
- Use descriptive headings.
- Present information logically.
- Avoid unnecessary repetition.

Documentation should remain understandable by future developers.

---

# Rule 11

## AI-Generated Documentation Must Be Reviewed

Documentation produced with AI assistance shall be reviewed before integration.

Documentation should accurately represent the implementation and comply with the project's documentation standards.

AI assistance does not replace engineering review.

---

# Rule 12

## Keep Examples Consistent

Whenever examples are provided, they should remain consistent with:

- architecture.md
- rules.md
- Current implementation

Examples should not introduce conflicting architectural patterns.

---

# Rule 13

## Preserve Version Consistency

Project documentation should clearly represent the current implementation version.

Future features shall not be documented as completed functionality.

Documentation should distinguish between:

- Current implementation.
- Planned enhancements.
- Future versions.

---

# Rule 14

## Maintain Documentation Quality

Documentation should remain:

- Accurate.
- Complete.
- Consistent.
- Organized.
- Maintainable.

Poor-quality documentation increases maintenance effort and reduces development efficiency.

---

# Rule 15

## Documentation Shall Evolve with the Project

Documentation is a living component of ProfitPilot.

As the project evolves, documentation should evolve alongside it.

Every major implementation milestone should be reflected in the project's documentation.

Documentation should never become obsolete.

---

# Standard Documentation Lifecycle

Every significant implementation should conceptually follow the following documentation lifecycle.

```
Design Feature
        │
        ▼
Implement Feature
        │
        ▼
Validate Feature
        │
        ▼
Update Documentation
        │
        ▼
Review Documentation
        │
        ▼
Merge Implementation
```

Documentation should remain synchronized with every development milestone.

---

# Documentation Principles

Project documentation should remain:

- Accurate
- Consistent
- Maintainable
- Readable
- Traceable
- Architecture-compliant
- Implementation-driven

Documentation exists to preserve knowledge, support development, and ensure long-term maintainability.

---

# Section Summary

The Documentation Rules establish the implementation standards for maintaining high-quality project documentation throughout the lifecycle of ProfitPilot.

By enforcing synchronized documentation, architectural consistency, clear ownership, and continuous maintenance, these rules ensure that the project's knowledge remains accurate, accessible, and valuable for both developers and AI-assisted development throughout future evolution.

# 18. Git & Version Control Rules

---

# Overview

The Git & Version Control Rules define the mandatory standards governing source code management throughout the development lifecycle of ProfitPilot.

Version control exists to preserve project history, maintain implementation quality, enable controlled evolution, and ensure that every change remains traceable and compliant with the approved architecture.

Every modification to the project shall be managed through version control.

---

# Rule 1

## Every Change Must Be Version Controlled

Every implementation, documentation update, configuration change, and project asset shall be tracked through the project's version control system.

No significant project change should exist outside version control.

Version history represents the authoritative record of project evolution.

---

# Rule 2

## Commit Logical Units of Work

Each commit shall represent one logical implementation task.

Examples include:

- Implementing a new architectural component.
- Fixing a specific defect.
- Updating documentation.
- Refactoring an existing module.

Unrelated changes shall not be combined into a single commit.

---

# Rule 3

## Preserve a Stable Main Branch

The main branch shall always remain in a stable and executable state.

Incomplete implementations, experimental features, or broken functionality shall not be committed directly to the main branch.

The main branch should always represent the latest stable version of ProfitPilot.

---

# Rule 4

## Every Commit Must Preserve Architecture Compliance

Before committing changes, verify that the implementation complies with:

- architecture.md
- rules.md

No commit shall introduce architectural violations.

Version control should preserve the integrity of the approved architecture.

---

# Rule 5

## Commit Messages Must Be Meaningful

Commit messages should clearly describe the purpose of the change.

Examples include:

- Add Data Processing Agent
- Implement RAG Retrieval Layer
- Refactor Business Analysis Module
- Update Architecture Documentation

Commit messages should describe **what** changed rather than listing modified files.

---

# Rule 6

## Documentation Changes Must Be Version Controlled

Updates to:

- PRD
- Architecture
- Rules
- Phases
- Design
- Memory

shall be committed alongside related implementation changes whenever applicable.

Documentation and implementation should evolve together.

---

# Rule 7

## Preserve Project History

Existing commit history shall remain intact.

History should accurately represent the evolution of the project.

Rewriting published project history should be avoided unless absolutely necessary.

Project history serves as the permanent development record.

---

# Rule 8

## Review Before Integration

Before integrating any completed implementation, verify:

- Architecture compliance.
- Rule compliance.
- Successful testing.
- Documentation updates.

Only validated implementations should become part of the stable codebase.

---

# Rule 9

## Separate Experimental Work

Experimental implementations should remain isolated from stable development.

Research prototypes, proof-of-concepts, and unfinished ideas should not affect the primary implementation until they have been validated.

This preserves the reliability of the main codebase.

---

# Rule 10

## Maintain Repository Organization

The repository should remain organized throughout development.

Project directories should continue to reflect:

- System architecture.
- Module responsibilities.
- Documentation structure.
- Testing organization.

Repository organization should remain consistent across all versions.

---

# Rule 11

## Preserve Traceability

Every significant implementation should be traceable through version history.

Project history should make it possible to determine:

- What changed.
- Why it changed.
- When it changed.

Traceability improves maintenance and future development.

---

# Rule 12

## Tag Significant Milestones

Major development milestones should be identified using version tags.

Examples include:

- Architecture Complete
- Phase 1 Complete
- End-to-End Workflow Complete
- Version 1.0

Tags provide stable reference points throughout project evolution.

---

# Rule 13

## Preserve Configuration Consistency

Configuration changes shall be committed in a controlled manner.

Configuration files should remain synchronized with the current implementation.

Environment-specific files containing sensitive information shall not be committed to the repository.

---

# Rule 14

## Maintain Repository Quality

The repository shall contain only project-related assets.

Examples of files that should not be committed include:

- Temporary files.
- Generated cache files.
- Local environment artifacts.
- Build outputs.
- Personal development files.

The repository should remain clean and reproducible.

---

# Rule 15

## Version Control Must Support Long-Term Evolution

The version control strategy should support future project growth.

Future contributors should be able to understand the evolution of ProfitPilot through:

- Commit history.
- Documentation history.
- Version tags.
- Repository organization.

The repository should remain maintainable throughout the lifetime of the project.

---

# Standard Version Control Lifecycle

Every implementation should conceptually follow the following lifecycle.

```
Design Feature
        │
        ▼
Implement Feature
        │
        ▼
Test Feature
        │
        ▼
Update Documentation
        │
        ▼
Review Implementation
        │
        ▼
Commit Changes
        │
        ▼
Merge into Stable Codebase
```

This lifecycle should remain consistent throughout development.

---

# Version Control Principles

The project's version control strategy should remain:

- Traceable
- Organized
- Consistent
- Reviewable
- Reproducible
- Architecture-compliant

Version control exists to preserve the quality, integrity, and history of ProfitPilot throughout its development.

---

# Section Summary

The Git & Version Control Rules establish the implementation standards for managing the evolution of the ProfitPilot codebase.

By enforcing logical commits, stable integration, architecture compliance, meaningful history, and synchronized documentation, these rules ensure that the project remains organized, maintainable, and fully traceable as it evolves from an academic prototype into a mature software system.

# 19. Performance & Security Rules

---

# Overview

The Performance & Security Rules define the mandatory implementation standards governing the operational quality of ProfitPilot.

These rules ensure that the system remains efficient, reliable, and secure while preserving the architectural principles established in `architecture.md`.

Performance optimization and security shall always support the architecture rather than compromise it.

Version 1 focuses on practical engineering practices appropriate for a terminal-based autonomous business intelligence system.

---

# Performance Rules

---

# Rule 1

## Correctness Before Performance

The implementation shall prioritize correctness and architectural compliance before optimization.

Performance improvements shall only be introduced after functionality has been validated.

Premature optimization should be avoided.

---

# Rule 2

## Avoid Unnecessary Computation

Components shall perform only the work required to complete their assigned responsibility.

Duplicate calculations, repeated processing, and unnecessary model invocations should be avoided whenever practical.

Efficient execution improves overall workflow performance.

---

# Rule 3

## Perform Expensive Operations Once

Computationally expensive operations should be executed once whenever practical.

Examples include:

- Knowledge base preparation.
- Embedding generation.
- Dataset preprocessing.
- Model initialization.

Runtime execution should reuse prepared resources instead of recreating them.

---

# Rule 4

## Optimize for Workflow Efficiency

The objective of optimization shall be reducing total workflow execution time rather than optimizing isolated components.

Performance improvements should benefit the complete autonomous workflow.

---

# Rule 5

## Preserve Modular Performance

Performance optimizations shall not violate architectural boundaries.

Components shall remain:

- Independent.
- Modular.
- Replaceable.

Architectural integrity shall always take precedence over optimization.

---

# Rule 6

## Avoid Unnecessary Memory Usage

The application should retain only the information required for the current workflow.

Temporary objects, intermediate artifacts, and unused resources should be released whenever practical.

Memory usage should remain proportional to the workflow requirements.

---

# Rule 7

## Minimize External Dependencies

External services and libraries should only be used when they provide measurable value.

Reducing unnecessary dependencies improves startup time, maintainability, and long-term stability.

---

# Rule 8

## Preserve Reproducibility

Performance optimizations shall not change the functional behaviour of the workflow.

Equivalent inputs should continue producing equivalent outputs after optimization.

---

# Security Rules

---

# Rule 9

## Sensitive Information Must Never Be Hardcoded

Sensitive information shall never be stored directly in the source code.

Examples include:

- API keys.
- Authentication tokens.
- Database credentials.
- Environment secrets.

Sensitive configuration should remain external to the application.

---

# Rule 10

## Validate External Inputs

All external inputs shall be validated before use.

Examples include:

- User prompts.
- Business datasets.
- Configuration files.
- External documents.

Validation reduces unexpected behaviour and improves system reliability.

---

# Rule 11

## Preserve Data Integrity

Business datasets shall remain protected throughout workflow execution.

Original datasets should never be overwritten.

Processing should always generate new outputs while preserving the original source data.

---

# Rule 12

## Limit Component Privileges

Architectural components should access only the resources required to perform their assigned responsibility.

Components should not access unrelated datasets, configuration, or internal implementation details.

Least-privilege principles improve maintainability and reduce unintended coupling.

---

# Rule 13

## Avoid Information Leakage

The application shall avoid exposing sensitive implementation details through:

- Error messages.
- Terminal output.
- Logs.
- Generated reports.

Only information relevant to the user or developer should be displayed.

---

# Rule 14

## Preserve Dependency Security

Project dependencies should originate from trusted and actively maintained sources.

Unverified or unnecessary third-party libraries should not be introduced without architectural justification.

Dependencies should be reviewed periodically throughout development.

---

# Rule 15

## Maintain Architecture Compliance

Performance improvements and security enhancements shall comply with:

- architecture.md
- rules.md

Neither optimization nor security measures shall violate architectural responsibilities or workflow integrity.

---

# Standard Operational Lifecycle

Operational improvements should conceptually follow the following lifecycle.

```
Implement Feature
        │
        ▼
Validate Correctness
        │
        ▼
Evaluate Performance
        │
        ▼
Review Security
        │
        ▼
Verify Architecture Compliance
        │
        ▼
Integrate Implementation
```

This lifecycle should remain consistent throughout the project.

---

# Performance & Security Principles

The implementation should remain:

- Efficient
- Reliable
- Secure
- Predictable
- Maintainable
- Modular
- Architecture-compliant

Operational improvements should strengthen the system without compromising architectural quality.

---

# Section Summary

The Performance & Security Rules establish the implementation standards for maintaining an efficient, reliable, and secure autonomous business intelligence system.

By prioritizing correctness before optimization, protecting sensitive information, preserving data integrity, minimizing unnecessary computation, and enforcing architectural compliance, these rules ensure that ProfitPilot remains performant, maintainable, and secure throughout its development and future evolution.

# 20. Things to Avoid

---

# Overview

This section defines the implementation practices, architectural violations, and software engineering anti-patterns that must be avoided throughout the development of ProfitPilot.

These guidelines exist to preserve architectural integrity, maintainability, explainability, and long-term scalability.

Every developer and AI coding assistant should review this section before implementing new functionality.

---

# Rule 1

## Never Violate the Architecture

The architecture defined in `architecture.md` shall never be bypassed or modified during implementation.

Implementation must always adapt to the architecture.

The architecture must never be changed simply to simplify coding.

---

# Rule 2

## Never Bypass the Autonomous Reasoning Engine

Business reasoning shall always be performed by the Autonomous Reasoning Engine.

Do not:

- Generate recommendations directly from business metrics.
- Skip the reasoning stage.
- Replace reasoning with hardcoded business rules.

Business reasoning is mandatory.

---

# Rule 3

## Never Allow Direct Agent Communication

Architectural agents shall never communicate directly.

Examples of prohibited behaviour include:

- Agent-to-agent method calls.
- Shared internal state.
- Direct imports between agent implementations.
- Manual workflow transitions.

All communication shall occur exclusively through the LangGraph Orchestrator.

---

# Rule 4

## Never Place Business Logic Outside Architectural Components

Business logic shall never exist inside:

- `main.py`
- Utility modules
- Configuration files
- Logging modules
- Test files

Business logic belongs only within the architectural component responsible for that functionality.

---

# Rule 5

## Never Modify Raw Business Data

Original business datasets shall remain unchanged throughout workflow execution.

Cleaning, transformation, and preprocessing should always produce new outputs.

The raw dataset is the permanent source of truth.

---

# Rule 6

## Never Hardcode Configuration

The implementation shall never hardcode:

- API keys.
- File paths.
- Model locations.
- Database credentials.
- Environment-specific values.

Configuration shall remain external to the application.

---

# Rule 7

## Never Mix Architectural Responsibilities

Every architectural component has exactly one responsibility.

Examples of prohibited behaviour include:

- Analysis Agent performing reasoning.
- RAG layer generating recommendations.
- Report Generation Agent performing analysis.
- LangGraph executing business logic.

Responsibilities shall remain independent.

---

# Rule 8

## Never Ignore Validation

Inputs and outputs shall always be validated.

The implementation shall never assume:

- Data is correct.
- Files always exist.
- Models always respond.
- External resources are always available.

Validation is mandatory at every stage.

---

# Rule 9

## Never Ignore Exceptions

Exceptions shall never be:

- Silently suppressed.
- Ignored.
- Hidden.

Every failure should result in:

- Recovery.
- Meaningful reporting.
- Graceful termination.

Unexpected failures must remain observable.

---

# Rule 10

## Never Duplicate Business Logic

Business logic shall exist in only one implementation location.

If functionality is required by multiple components, it should be extracted into an appropriate shared module.

Copy-paste implementations shall be avoided.

---

# Rule 11

## Never Introduce Unnecessary Complexity

Do not introduce:

- Unnecessary abstractions.
- Unused design patterns.
- Premature optimizations.
- Redundant dependencies.

The simplest architecture-compliant solution should always be preferred.

---

# Rule 12

## Never Leave Dead Code in the Repository

The project shall not contain:

- Unused functions.
- Commented-out implementations.
- Obsolete modules.
- Experimental code no longer in use.

The repository should contain only active, maintainable code.

---

# Rule 13

## Never Introduce Circular Dependencies

Modules shall not depend upon one another in a circular manner.

Dependencies should always follow the architectural direction defined in `architecture.md`.

Circular imports reduce maintainability and increase implementation complexity.

---

# Rule 14

## Never Compromise Explainability

The implementation shall never produce:

- Unsupported business conclusions.
- Untraceable recommendations.
- Hidden workflow behaviour.

Every recommendation should remain traceable to:

- Business data.
- Business analysis.
- Retrieved knowledge.
- Business reasoning.

Explainability is a core architectural requirement.

---

# Rule 15

## Never Expand Version 1 Scope Prematurely

Version 1 focuses exclusively on validating the autonomous workflow.

Avoid implementing unrelated features such as:

- Authentication.
- User management.
- Cloud deployment.
- Multi-user support.
- Dashboard enhancements.
- Enterprise integrations.

These features belong to future versions.

---

# Rule 16

## Never Allow Documentation to Become Outdated

Project documentation shall never fall behind implementation.

Whenever implementation changes, update:

- architecture.md
- rules.md
- phases.md
- memory.md

Documentation should remain synchronized with the project.

---

# Rule 17

## Never Commit Broken Implementations

Code shall never be committed if it:

- Breaks existing functionality.
- Violates the architecture.
- Fails validation.
- Produces inconsistent workflow behaviour.

Only validated implementations should become part of the stable codebase.

---

# Rule 18

## Never Prioritize Speed Over Quality

Implementation shortcuts that reduce:

- Maintainability.
- Readability.
- Modularity.
- Explainability.
- Architecture compliance.

shall be avoided.

Long-term software quality always takes precedence over short-term development speed.

---

# Rule 19

## Never Let AI Override Engineering Decisions

AI coding assistants shall assist implementation.

They shall not:

- Redesign the architecture.
- Introduce new responsibilities.
- Modify workflow execution.
- Override documented engineering decisions.

Human-reviewed project documentation remains the authoritative source of truth.

---

# Rule 20

## Never Compromise the Core Philosophy of ProfitPilot

The implementation shall never violate the central philosophy of the project.

The user provides one business objective.

From that point onward, ProfitPilot autonomously:

- Plans execution.
- Collects data.
- Processes data.
- Performs business analysis.
- Retrieves knowledge.
- Generates business reasoning.
- Produces actionable recommendations.
- Generates the final report.

No implementation should compromise this autonomous workflow.

---

# Anti-Pattern Checklist

Before integrating any implementation, verify that none of the following have occurred.

- Architecture has been bypassed.
- Agents communicate directly.
- Business logic exists outside architectural components.
- Raw datasets have been modified.
- Configuration has been hardcoded.
- Responsibilities have been mixed.
- Validation has been skipped.
- Exceptions have been ignored.
- Business logic has been duplicated.
- Circular dependencies have been introduced.
- Documentation has become outdated.
- Version 1 scope has expanded unnecessarily.

If any item in this checklist is true, the implementation should be revised before integration.

---

# Guiding Principle

When faced with multiple implementation choices:

- Choose the simplest solution.
- Preserve the architecture.
- Maintain modularity.
- Protect explainability.
- Keep the workflow autonomous.

These principles should take precedence over implementation convenience.

---

# Section Summary

The Things to Avoid section defines the architectural and engineering anti-patterns that must never appear within ProfitPilot.

By identifying prohibited implementation practices, preserving architectural integrity, preventing workflow violations, and reinforcing the project's autonomous design philosophy, these rules help ensure that ProfitPilot remains consistent, maintainable, explainable, and aligned with its long-term vision.

# 21. Non-Negotiable Rules

---

# Overview

The Non-Negotiable Rules define the immutable implementation principles of ProfitPilot.

These rules establish the core identity of the system and shall remain unchanged throughout Version 1 development.

Unlike other implementation guidelines, these rules are absolute.

No implementation convenience, optimization, AI-generated suggestion, or development shortcut shall justify violating these principles.

Every implementation decision must preserve these rules.

---

# Rule 1

## Preserve the Approved Architecture

The architecture defined in `architecture.md` is the authoritative blueprint of ProfitPilot.

Implementation shall conform to the architecture.

The architecture shall never be modified to simplify implementation.

---

# Rule 2

## Preserve the Autonomous Workflow

The autonomous workflow shall always remain:

```
User Prompt
        │
        ▼
Planning
        │
        ▼
LangGraph Orchestrator
        │
        ▼
Data Collector Agent
        │
        ▼
Data Processing Agent
        │
        ▼
Analysis Agent
        │
        ▼
RAG Retrieval Layer
        │
        ▼
Autonomous Reasoning Engine
        │
        ▼
Business Tactics Agent
        │
        ▼
Report Generation Agent
```

No architectural component shall be removed, reordered, bypassed, or replaced.

---

# Rule 3

## Single Prompt Execution Is Mandatory

The user shall provide only one business objective.

After receiving the initial prompt, ProfitPilot shall complete the entire workflow autonomously.

The system shall not request additional user input during workflow execution.

---

# Rule 4

## Preserve Centralized Orchestration

The LangGraph Orchestrator shall remain the only workflow execution controller.

Architectural components shall never communicate directly.

Workflow execution shall always remain centralized.

---

# Rule 5

## Preserve the Four-Agent Architecture

The following architectural agents shall remain independent:

- Data Collector Agent
- Data Processing Agent
- Analysis Agent
- Business Tactics Agent

Each agent shall perform exactly one architectural responsibility.

Responsibilities shall never overlap.

---

# Rule 6

## Preserve the Autonomous Reasoning Engine

Business reasoning shall always be performed exclusively by the Autonomous Reasoning Engine.

Business reasoning shall never be replaced by:

- Hardcoded rules.
- Manual decision trees.
- Heuristic shortcuts.
- Direct recommendation generation.

The intelligence of ProfitPilot remains centralized within the Autonomous Reasoning Engine.

---

# Rule 7

## Preserve the Separation Between Analysis and Reasoning

The Analysis Agent answers:

**What is happening?**

The Autonomous Reasoning Engine answers:

**Why is it happening?**

The Business Tactics Agent answers:

**What should be done?**

These responsibilities shall remain permanently separated.

---

# Rule 8

## Recommendations Must Always Originate from Reasoning

Business recommendations shall always be generated from validated business reasoning.

The workflow shall never generate recommendations directly from:

- Business KPIs.
- Analytical outputs.
- Retrieved knowledge.

Business reasoning is mandatory.

---

# Rule 9

## Preserve the RAG Architecture

The RAG layer shall remain retrieval-only.

It shall never:

- Perform reasoning.
- Generate recommendations.
- Execute analysis.
- Interpret business knowledge.

Knowledge retrieval and business reasoning shall remain independent.

---

# Rule 10

## Preserve Explainability

Every recommendation shall remain traceable through the complete chain of evidence.

```
Business Data
        │
        ▼
Business KPIs
        │
        ▼
Business Analysis
        │
        ▼
Retrieved Knowledge
        │
        ▼
Business Reasoning
        │
        ▼
Business Recommendations
```

No implementation shall bypass this evidence chain.

---

# Rule 11

## Preserve Terminal-First Development

Version 1 shall remain terminal-based.

The terminal shall display:

- Workflow execution.
- Intermediate outputs.
- Business reasoning progress.
- Final report.

User interface development shall not influence Version 1 implementation.

---

# Rule 12

## Preserve Modular Architecture

Every architectural component shall remain:

- Independent.
- Replaceable.
- Testable.
- Maintainable.

Architectural responsibilities shall never become tightly coupled.

---

# Rule 13

## Preserve Version 1 Scope

Version 1 exists to validate the autonomous business intelligence workflow.

The implementation shall remain focused on:

- Autonomous execution.
- Business intelligence.
- Explainable reasoning.
- Actionable recommendations.

Features outside this objective shall remain deferred to future versions.

---

# Rule 14

## Preserve Documentation Integrity

The following project documents shall remain synchronized throughout development:

- prd.md
- architecture.md
- rules.md
- phases.md
- design.md
- memory.md

Documentation shall accurately reflect the current implementation at all times.

---

# Rule 15

## Every Implementation Must Respect These Rules

Every source file, module, AI agent, workflow, implementation decision, and future enhancement shall comply with:

- architecture.md
- rules.md

No implementation is exempt from these requirements.

These rules represent the permanent engineering foundation of ProfitPilot Version 1.

---

# Immutable Principles

The following principles shall never be compromised during Version 1 development.

- Autonomous execution.
- Single prompt interaction.
- Centralized orchestration.
- Four-agent architecture.
- Retrieval-Augmented Generation.
- Autonomous business reasoning.
- Explainable recommendations.
- Terminal-first implementation.
- Modular architecture.
- Architecture-first development.

These principles define the identity of ProfitPilot.

---

# Final Compliance Checklist

Before accepting any implementation, verify the following.

- The architecture remains unchanged.
- The workflow remains autonomous.
- LangGraph remains the only orchestrator.
- Agents remain independent.
- The RAG layer remains retrieval-only.
- Business reasoning remains centralized.
- Recommendations originate from reasoning.
- Explainability has been preserved.
- Terminal execution remains functional.
- Documentation remains synchronized.

Every item in this checklist must be satisfied before implementation is considered complete.

---

# Final Principle

Whenever an implementation decision conflicts with these rules:

**The implementation shall change.**

**The rules shall not.**

These Non-Negotiable Rules define the permanent engineering identity of ProfitPilot Version 1.

---

# Section Summary

The Non-Negotiable Rules establish the immutable engineering principles that govern the implementation of ProfitPilot.

They preserve the project's architectural integrity, autonomous workflow, explainable reasoning, modular design, and long-term vision.

Every implementation decision throughout Version 1 development shall conform to these principles, ensuring that ProfitPilot remains faithful to its original architectural philosophy regardless of future enhancements or implementation changes.

# 22. Conclusion

---

# Overview

The Rules Document establishes the engineering standards that govern the implementation of ProfitPilot.

While the Software Architecture Document defines the structural design of the system, this document defines the implementation practices required to preserve that design throughout the development lifecycle.

Together, these documents provide a complete framework for building an autonomous, explainable, modular, and maintainable business intelligence system.

---

# Engineering Foundation

The rules defined in this document are intended to ensure that every implementation remains consistent with the architectural vision of ProfitPilot.

They provide a common engineering standard for:

- Software development
- AI-assisted implementation
- Code quality
- Architectural compliance
- Long-term maintainability

By following these rules, every contributor works within the same engineering framework regardless of experience or development environment.

---

# Relationship with the Architecture

The Software Architecture Document defines:

**What ProfitPilot is.**

The Rules Document defines:

**How ProfitPilot must be implemented.**

Neither document replaces the other.

Instead, they work together to ensure that implementation faithfully reflects the approved architectural design.

Whenever implementation decisions are made, both documents shall be treated as authoritative references.

---

# Purpose of These Rules

The primary purpose of these rules is to preserve:

- Architectural integrity
- Autonomous execution
- Explainability
- Modularity
- Maintainability
- Consistency
- Scalability

Every implementation decision should strengthen these principles rather than compromise them.

---

# Long-Term Engineering Vision

ProfitPilot is designed to evolve through incremental development while preserving its architectural foundation.

Future enhancements may introduce:

- Graphical user interfaces
- Enterprise capabilities
- Cloud deployment
- Organization-specific knowledge bases
- Additional analytical capabilities

Regardless of future expansion, the implementation should continue to follow the engineering principles established within this document.

The architecture may evolve through formal revision, but implementation quality shall remain governed by disciplined engineering practices.

---

# AI-Assisted Development

ProfitPilot is intentionally designed to support AI-assisted software development.

These rules provide a shared engineering standard for both human developers and AI coding assistants.

Before generating, modifying, or reviewing code, every AI assistant should comply with:

- architecture.md
- rules.md

This ensures that AI-generated implementations remain consistent with the project's architectural philosophy and engineering standards.

---

# Engineering Philosophy

Every implementation should strive to be:

- Simple
- Modular
- Explainable
- Maintainable
- Testable
- Predictable
- Architecture-compliant

Implementation quality should always take precedence over development speed or unnecessary complexity.

---

# Final Engineering Statement

ProfitPilot is more than a collection of software modules.

It is an autonomous business intelligence system whose value depends on disciplined engineering, clear architectural boundaries, explainable reasoning, and consistent implementation.

The rules defined in this document exist to preserve those qualities throughout the entire lifecycle of the project.

Every implementation should contribute to a system that is understandable, reliable, extensible, and faithful to its original architectural vision.

---

# Closing Principle

Whenever uncertainty exists during implementation:

- Follow the architecture.
- Follow the rules.
- Preserve modularity.
- Preserve explainability.
- Preserve autonomy.

If an implementation conflicts with these principles, the implementation should change—not the principles.

---

# Final Declaration

This Rules Document serves as the official implementation standard for ProfitPilot Version 1.

Every architectural component, source file, workflow, AI agent, and future enhancement shall be implemented in accordance with the engineering standards established herein.

Together with the Software Architecture Document, this document forms the permanent engineering foundation upon which ProfitPilot is designed, implemented, validated, and evolved.

---

**End of Rules Document**