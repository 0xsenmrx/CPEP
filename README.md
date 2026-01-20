# CPEP: Cross-Platform Enumeration, PrivEsc & Persistence

CPEP is a structured execution framework designed to consolidate security enumeration, privilege escalation, and persistence (post-exploitation in one word) scripts into a unified, modular system. It serves as an orchestration layer that maps specific security plugins to target environments based on operating system, architecture, and functional category.

The project's primary goal is to provide a standardized interface for executing disparate Python-based security tools while maintaining strict control over execution scope and environmental compatibility.

## Concept and Architecture

The framework operates on a "Path-to-Plugin" philosophy. By enforcing a rigid directory structure, the engine ensures that security researchers only execute relevant code against a detected or specified target. This mitigates the risk of running incompatible exploits and organizes vast libraries of scripts into a logical hierarchy.



### Milestone Completion: Phase One

The initial phase has focused on the development of the core engine and the UI/UX environment. The following milestones have been achieved:

* **Standardized Pathing Engine**: Implemented a core logic that resolves paths based on `plugins/<os>/<arch>/<category>/<subcategory>/`.
* **Hierarchical Execution Control**: Developed a strict flag-based system (`-c`, `-sc`, `-p`) that requires explicit scope definitions.
* **Automatic Scope Escalation**: Built an intelligent handler that detects comma-separated lists to automatically switch from single-plugin execution to recursive directory sweeps.
* **Environmental Fingerprinting**: Integrated automatic detection of the host OS and CPU architecture with optional manual overrides for remote target modeling.
* **UI Normalization**: Created a terminal-aware interface that dynamically adjusts headers and borders to the current terminal width, providing a clean and readable output regardless of the display environment.
* **Execution Isolation**: Configured a subprocess management system that executes plugins with a 300-second timeout and captures STDOUT/STDERR for centralized logging and formatting.

## Usage and Logic Flow

CPEP utilizes a tiered approach to command execution. If a user provides multiple items at any level of the hierarchy, the engine assumes a broader scope is required and executes recursively.

### Direct Execution
To execute a specific script within a known subcategory:
```bash
python3 cpep.py -c enumeration -sc users -p check_sudo
```

### Recursive Category Sweep
To execute every script within a category across all subcategories:
```bash 
python3 cpep.py -c enumeration -sca
```

### Multi-Target Escalation
To sweep multiple specific categories or subcategories:
```bash
python3 cpep.py -c enumeration,privesc -sca
```

## Technical Requirements

* Python Version: 3.7 or higher.
* Dependencies: Zero external dependencies. All core logic utilizes the Python Standard Library (os, sys, subprocess, argparse, shutil, platform).

## Framework Markers 

The engine intercepts plugin output to apply standardized status highlighting:

* `[+]` : Indicates a successful finding or confirmed vulnerability. 
* `[!]` : Indicates a warning, a configuration note, or a point of interest.
* `[ERROR]` : Indicates a script-level failure or execution exception.

--- 

_*Developed for efficient, structured, and modular security testing.*_
