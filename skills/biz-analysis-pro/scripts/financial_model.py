#!/usr/bin/env python3
"""Financial projection model for business analysis competitions."""

import argparse
import json
import sys
from pathlib import Path


def project_financials(
    starting_users: float,
    monthly_growth_rate: float,
    monthly_churn_rate: float,
    arpu: float,
    fixed_costs_monthly: float,
    variable_cost_per_user: float,
    one_time_investment: float = 0,
    years: int = 5,
):
    """Project financials over N years."""

    months = years * 12
    users = starting_users
    monthly_data = []

    for m in range(1, months + 1):
        new_users = users * monthly_growth_rate
        lost_users = users * monthly_churn_rate
        users = users + new_users - lost_users

        revenue = users * arpu
        variable_cost = users * variable_cost_per_user
        total_cost = fixed_costs_monthly + variable_cost
        profit = revenue - total_cost

        monthly_data.append({
            'month': m,
            'users': round(users),
            'new_users': round(new_users),
            'lost_users': round(lost_users),
            'revenue': round(revenue),
            'total_cost': round(total_cost),
            'profit': round(profit),
        })

    # Aggregate to yearly
    yearly = []
    for y in range(years):
        start = y * 12
        end = start + 12
        year_months = monthly_data[start:end]

        avg_users = sum(m['users'] for m in year_months) / 12
        total_revenue = sum(m['revenue'] for m in year_months)
        total_cost = sum(m['total_cost'] for m in year_months)
        gross_profit = total_revenue - total_cost

        yearly.append({
            'year': y + 1,
            'avg_users': round(avg_users),
            'end_users': year_months[-1]['users'],
            'revenue': round(total_revenue),
            'cost': round(total_cost),
            'gross_profit': round(gross_profit),
            'gross_margin': round(gross_profit / total_revenue * 100, 1) if total_revenue else 0,
        })

    # Key metrics
    ltv = arpu * 12 / monthly_churn_rate if monthly_churn_rate > 0 else float('inf')
    # Estimate CAC from fixed costs / new users in first year
    first_year_new = sum(m['new_users'] for m in monthly_data[:12])
    first_year_fixed = fixed_costs_monthly * 12
    cac = first_year_fixed / first_year_new if first_year_new > 0 else float('inf')
    ltv_cac = ltv / cac if cac > 0 and cac != float('inf') else float('inf')

    # Break-even month
    cumulative = -one_time_investment
    break_even_month = None
    for m in monthly_data:
        cumulative += m['profit']
        if cumulative >= 0 and break_even_month is None:
            break_even_month = m['month']

    metrics = {
        'ltv': round(ltv),
        'cac': round(cac),
        'ltv_cac_ratio': round(ltv_cac, 1) if ltv_cac != float('inf') else 'N/A',
        'break_even_month': break_even_month or 'Not within projection period',
        'final_year_users': yearly[-1]['end_users'],
        'final_year_revenue': yearly[-1]['revenue'],
    }

    return {
        'assumptions': {
            'starting_users': starting_users,
            'monthly_growth_rate': f'{monthly_growth_rate*100:.1f}%',
            'monthly_churn_rate': f'{monthly_churn_rate*100:.1f}%',
            'arpu': arpu,
            'fixed_costs_monthly': fixed_costs_monthly,
            'variable_cost_per_user': variable_cost_per_user,
            'one_time_investment': one_time_investment,
            'projection_years': years,
        },
        'yearly_projection': yearly,
        'key_metrics': metrics,
    }


def format_report(result):
    """Format results as markdown report."""
    lines = []
    lines.append('# Financial Projection Report\n')

    lines.append('## Assumptions\n')
    lines.append('| Parameter | Value |')
    lines.append('|-----------|-------|')
    for k, v in result['assumptions'].items():
        lines.append(f'| {k} | {v} |')

    lines.append('\n## Yearly Projection\n')
    lines.append('| Year | Avg Users | End Users | Revenue | Cost | Gross Profit | Margin |')
    lines.append('|------|-----------|-----------|---------|------|-------------|--------|')
    for y in result['yearly_projection']:
        lines.append(
            f"| {y['year']} | {y['avg_users']:,} | {y['end_users']:,} | "
            f"¥{y['revenue']:,} | ¥{y['cost']:,} | ¥{y['gross_profit']:,} | "
            f"{y['gross_margin']}% |"
        )

    lines.append('\n## Key Metrics\n')
    m = result['key_metrics']
    lines.append(f'- **LTV**: ¥{m["ltv"]:,}')
    lines.append(f'- **CAC**: ¥{m["cac"]:,}')
    lines.append(f'- **LTV/CAC**: {m["ltv_cac_ratio"]}')
    lines.append(f'- **Break-even Month**: {m["break_even_month"]}')
    lines.append(f'- **Final Year Users**: {m["final_year_users"]:,}')
    lines.append(f'- **Final Year Revenue**: ¥{m["final_year_revenue"]:,}')

    return '\n'.join(lines)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Financial projection for business competitions')
    parser.add_argument('--users', type=float, default=1000, help='Starting users')
    parser.add_argument('--growth', type=float, default=0.08, help='Monthly growth rate (e.g. 0.08 = 8%%)')
    parser.add_argument('--churn', type=float, default=0.05, help='Monthly churn rate')
    parser.add_argument('--arpu', type=float, default=50, help='Monthly ARPU')
    parser.add_argument('--fixed-cost', type=float, default=100000, help='Monthly fixed costs')
    parser.add_argument('--var-cost', type=float, default=10, help='Variable cost per user per month')
    parser.add_argument('--investment', type=float, default=0, help='One-time investment')
    parser.add_argument('--years', type=int, default=5, help='Projection years')
    parser.add_argument('-o', '--output', help='Output file (md or json)')
    args = parser.parse_args()

    result = project_financials(
        starting_users=args.users,
        monthly_growth_rate=args.growth,
        monthly_churn_rate=args.churn,
        arpu=args.arpu,
        fixed_costs_monthly=args.fixed_cost,
        variable_cost_per_user=args.var_cost,
        one_time_investment=args.investment,
        years=args.years,
    )

    if args.output:
        output_path = Path(args.output)
        if output_path.suffix == '.json':
            output_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')
        else:
            output_path.write_text(format_report(result), encoding='utf-8')
        print(f'Saved to {args.output}')
    else:
        print(format_report())
