from unittest import TestCase

from ..controllers import Capacity


class TestCapacity(TestCase):
    def test_capacity(self):
        capacity = Capacity(
            name="faculty",
            students_count=1272,
            teacher_to_student_ratio=35,
            locality_percentage=0.5,
            local_fulltime_specialist_count=16,
            local_fulltime_supportive_count=6,
            foreign_fulltime_specialist_count=1,
            foreign_fulltime_supportive_count=0,
            parttime_specialist_count=9,
            parttime_supportive_count=9,
            master_count=14
        )
        self.assertEqual(capacity.capacity, 1575)
        self.assertEqual(capacity.required_local_count, 21)

    def test_capacity_2(self):
        capacity = Capacity(
            name="faculty",
            students_count=1344,
            teacher_to_student_ratio=35,
            locality_percentage=0.5,
            local_fulltime_specialist_count=20,
            local_fulltime_supportive_count=1,
            foreign_fulltime_specialist_count=6,
            foreign_fulltime_supportive_count=0,
            parttime_specialist_count=14,
            parttime_supportive_count=1,
            master_count=4
        )
        self.assertEqual(capacity.capacity, 1540)
        self.assertEqual(capacity.required_local_count, 21)

    def test_capacity_3(self):
        capacity = Capacity(
            name="faculty",
            students_count=2110,
            teacher_to_student_ratio=35,
            locality_percentage=0.5,
            local_fulltime_specialist_count=15,
            local_fulltime_supportive_count=4,
            foreign_fulltime_specialist_count=11,
            foreign_fulltime_supportive_count=0,
            parttime_specialist_count=9,
            parttime_supportive_count=4,
            master_count=0
        )
        self.assertEqual(capacity.capacity, 1505)
        self.assertEqual(capacity.required_local_count, 22)