import unittest
from workload.app import Application
from workload.store import Store
from workload.ledger import span_minutes, grade_at, save_service
from workload.comparison import service_detail, service_overview
from workload.settlement import draft_invoice, confirm_invoice


class WorkloadTests(unittest.TestCase):
    def setUp(self):
        self.store = Store(':memory:')
        Application(self.store).seed()

    def tearDown(self):
        self.store.close()

    def test_span(self):
        self.assertEqual(span_minutes('2026-10-01T23:50', '2026-10-02T00:20'), 30)

    def test_reverse_span(self):
        with self.assertRaises(ValueError):
            span_minutes('2026-10-01T12:00', '2026-10-01T11:00')

    def test_grade_effective_date(self):
        self.assertEqual(grade_at(self.store, 'r1', '2026-10-16'), 'high')
        self.assertEqual(grade_at(self.store, 'r1', '2026-10-14'), 'moderate')

    def test_unknown_grade(self):
        self.assertIsNone(grade_at(self.store, 'missing', '2026-10-01'))

    def test_detail_does_not_multiply_elapsed(self):
        self.assertEqual(service_detail(self.store, 's1')['elapsed_minutes'], 40)

    def test_descriptive_mean(self):
        row = next(row for row in service_overview(self.store) if row['kind'] == 'bathing')
        self.assertEqual(row['mean_elapsed_minutes'], 30)

    def test_duplicate_participant(self):
        row = dict(self.store.get('services', 's1'), people=['p1', 'p1'])
        with self.assertRaises(ValueError):
            save_service(self.store, row)

    def test_draft_cost(self):
        self.assertEqual(draft_invoice(self.store, 'east', '2026-10')['cents'], 4000)

    def test_confirmed_invoice_is_preserved(self):
        before = confirm_invoice(self.store, 'east', '2026-10')
        self.store.put('rates', {'id': 'bathing', 'cents_per_unit': 9000})
        self.assertEqual(confirm_invoice(self.store, 'east', '2026-10'), before)

    def test_empty_month_has_zero_units(self):
        self.assertEqual(draft_invoice(self.store, 'east', '2027-01')['cents'], 0)
