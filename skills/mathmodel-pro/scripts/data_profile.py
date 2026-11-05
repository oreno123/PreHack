#!/usr/bin/env python3
"""Quick data profiling for math modeling competition datasets."""

import argparse
import sys
from pathlib import Path

def profile_csv(filepath, output=None):
    import pandas as pd
    import numpy as np

    # Detect encoding
    for enc in ['utf-8', 'gbk', 'gb2312', 'latin1']:
        try:
            df = pd.read_csv(filepath, encoding=enc)
            break
        except (UnicodeDecodeError, pd.errors.ParserError):
            continue
    else:
        df = pd.read_csv(filepath, encoding='latin1')

    lines = []
    lines.append(f"# Data Profile: {Path(filepath).name}")
    lines.append(f"- Shape: {df.shape[0]} rows x {df.shape[1]} columns")
    lines.append(f"- Memory: {df.memory_usage(deep=True).sum() / 1024:.1f} KB\n")

    # Column overview
    lines.append("## Column Overview")
    lines.append("| Column | Type | Non-null | Null% | Unique | Sample |")
    lines.append("|--------|------|----------|-------|--------|--------|")
    for col in df.columns:
        non_null = df[col].notna().sum()
        null_pct = df[col].isna().sum() / len(df) * 100
        nunique = df[col].nunique()
        sample = str(df[col].dropna().iloc[0]) if non_null > 0 else "N/A"
        if len(sample) > 30:
            sample = sample[:30] + "..."
        lines.append(f"| {col} | {df[col].dtype} | {non_null} | {null_pct:.1f}% | {nunique} | {sample} |")

    # Numeric stats
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        lines.append("\n## Numeric Statistics")
        desc = df[numeric_cols].describe().T
        desc['missing'] = df[numeric_cols].isna().sum()
        desc['skew'] = df[numeric_cols].skew()
        lines.append(desc.round(4).to_markdown())

    # Correlation (top pairs only)
    if len(numeric_cols) >= 2:
        lines.append("\n## Top Correlations (|r| > 0.5)")
        corr = df[numeric_cols].corr()
        pairs = []
        for i in range(len(numeric_cols)):
            for j in range(i + 1, len(numeric_cols)):
                r = corr.iloc[i, j]
                if abs(r) > 0.5:
                    pairs.append((numeric_cols[i], numeric_cols[j], r))
        pairs.sort(key=lambda x: abs(x[2]), reverse=True)
        if pairs:
            lines.append("| Var 1 | Var 2 | Correlation |")
            lines.append("|-------|-------|-------------|")
            for v1, v2, r in pairs[:15]:
                lines.append(f"| {v1} | {v2} | {r:.4f} |")
        else:
            lines.append("No strong correlations found.")

    # Categorical stats
    cat_cols = df.select_dtypes(include=['object', 'category']).columns
    if len(cat_cols) > 0:
        lines.append("\n## Categorical Columns")
        for col in cat_cols:
            vc = df[col].value_counts()
            lines.append(f"\n### {col} ({vc.shape[0]} unique)")
            if vc.shape[0] <= 20:
                for val, cnt in vc.items():
                    lines.append(f"- {val}: {cnt} ({cnt / len(df) * 100:.1f}%)")
            else:
                for val, cnt in vc.head(10).items():
                    lines.append(f"- {val}: {cnt} ({cnt / len(df) * 100:.1f}%)")
                lines.append(f"- ... and {vc.shape[0] - 10} more")

    # Data quality issues
    lines.append("\n## Data Quality Issues")
    issues = []
    for col in df.columns:
        null_pct = df[col].isna().sum() / len(df) * 100
        if null_pct > 0:
            issues.append(f"- **{col}**: {null_pct:.1f}% missing values")
    dup_count = df.duplicated().sum()
    if dup_count > 0:
        issues.append(f"- **Duplicates**: {dup_count} duplicate rows ({dup_count / len(df) * 100:.1f}%)")
    if not issues:
        issues.append("- No obvious quality issues detected")
    lines.extend(issues)

    result = "\n".join(lines)

    if output:
        Path(output).write_text(result, encoding='utf-8')
        print(f"Profile saved to {output}")
    else:
        print(result)

    return result


def profile_excel(filepath, output=None, sheet=None):
    import pandas as pd
    xls = pd.ExcelFile(filepath)
    if sheet:
        sheets = [sheet]
    else:
        sheets = xls.sheet_names
        print(f"Sheets: {sheets}")

    all_results = []
    for s in sheets:
        print(f"\n--- Sheet: {s} ---")
        df = pd.read_excel(filepath, sheet_name=s)
        # Temp save as csv for profiling
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False, mode='w', encoding='utf-8') as f:
            df.to_csv(f.name, index=False)
            result = profile_csv(f.name, output=None)
            all_results.append(f"## Sheet: {s}\n\n{result}")
            Path(f.name).unlink()

    combined = "\n\n".join(all_results)
    if output:
        Path(output).write_text(combined, encoding='utf-8')
        print(f"\nAll profiles saved to {output}")
    return combined


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Quick data profiling')
    parser.add_argument('file', help='CSV or Excel file path')
    parser.add_argument('-o', '--output', help='Output markdown file path')
    parser.add_argument('-s', '--sheet', help='Excel sheet name (default: all)')
    args = parser.parse_args()

    filepath = Path(args.file)
    if not filepath.exists():
        print(f"Error: {filepath} not found")
        sys.exit(1)

    ext = filepath.suffix.lower()
    if ext in ['.xlsx', '.xls']:
        profile_excel(str(filepath), args.output, args.sheet)
    elif ext == '.csv':
        profile_csv(str(filepath), args.output)
    else:
        print(f"Unsupported format: {ext}. Use CSV or Excel.")
        sys.exit(1)
