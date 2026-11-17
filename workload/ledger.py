from datetime import datetime


def span_minutes(start, end):
    delta = (datetime.fromisoformat(end) - datetime.fromisoformat(start)).total_seconds()
    if delta < 0 or delta % 60:
        raise ValueError('服务区间须按完整分钟递增')
    return int(delta // 60)


def save_service(store, row):
    span_minutes(row['start'], row['end'])
    if len(set(row['people'])) != len(row['people']):
        raise ValueError('参与人员重复')
    if row['status'] not in ['completed', 'interrupted']:
        raise ValueError('服务状态不合法')
    return store.put('services', row)


def grade_at(store, resident, day):
    rows = [row for row in store.all('grades') if row['resident'] == resident and row['effective'] <= day]
    if not rows:
        return None
    return max(rows, key=lambda row: (row['effective'], row['recorded']))['grade']
