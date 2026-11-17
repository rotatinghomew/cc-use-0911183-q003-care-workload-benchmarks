from statistics import mean
from .ledger import grade_at, span_minutes


def service_overview(store):
    groups = {}
    for row in store.all('services'):
        group = groups.setdefault(row['kind'], [])
        group.append(span_minutes(row['start'], row['end']))
    return [{'kind': key, 'count': len(values), 'mean_elapsed_minutes': mean(values)} for key, values in sorted(groups.items())]


def service_detail(store, key):
    row = store.get('services', key)
    return {**row, 'elapsed_minutes': span_minutes(row['start'], row['end']), 'grade': grade_at(store, row['resident'], row['start'][:10])}
