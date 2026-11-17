def draft_invoice(store, team, month):
    rows = [row for row in store.all('units') if row['team'] == team and row['month'] == month]
    total = 0
    for row in rows:
        rate = store.get('rates', row['kind'])['cents_per_unit']
        total += row['units'] * rate
    return {'id': team + ':' + month, 'team': team, 'month': month, 'cents': total, 'unit_ids': sorted(row['id'] for row in rows)}


def confirm_invoice(store, team, month):
    key = team + ':' + month
    existing = [row for row in store.all('invoices') if row['id'] == key]
    if existing:
        return existing[0]
    invoice = draft_invoice(store, team, month)
    store.put('invoices', invoice, expected=0)
    return invoice
