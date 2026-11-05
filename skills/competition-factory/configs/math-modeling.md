# Math Modeling Competition Config

Delegates to `mathmodel-pro` skill for full pipeline.

## Quick Reference
- **Roles**: Analyst, Modeler, Coder, Artist, Writer, Reviewer (6 subagents)
- **Pipeline**: 10 stages (see mathmodel-pro SKILL.md)
- **Output**: Academic paper in Markdown + LaTeX notation
- **Paper language**: Chinese (CUMCM) or English (MCM/ICM)
- **Deadline pressure**: 3 days typical, prioritize working code over elegant math

## When to override mathmodel-pro defaults
- If competition specifies output format (e.g., LaTeX template), follow competition spec
- If no data files provided (pure modeling), skip data processing stage
- If partial data provided, note missing data in assumptions section

## Key files
- Model knowledge base: `mathmodel-pro/references/model-knowledge-base.md`
- Paper template: `mathmodel-pro/references/paper-template.md`
- Visualization guide: `mathmodel-pro/references/visualization-guide.md`
- Data profiler: `mathmodel-pro/scripts/data_profile.py`
