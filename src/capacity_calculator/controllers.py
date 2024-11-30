import math
from dataclasses import InitVar, asdict, dataclass, field


@dataclass
class Capacity:
    name: str
    students_count: int
    teacher_to_student_ratio: int
    locality_percentage: InitVar[float]

    local_fulltime_specialist_count: int
    local_fulltime_supportive_count: int
    foreign_fulltime_specialist_count: int
    foreign_fulltime_supportive_count: int
    parttime_specialist_count: int
    parttime_supportive_count: int
    master_count: int

    fulltime_specialist_count: int = field(init=False)
    fulltime_supportive_count: int = field(init=False)

    allowed_specialist_parttime_count: int = field(init=False)
    allowed_supportive_parttime_count: int = field(init=False)
    allowed_parttime_count: int = field(init=False)

    allowed_masters_count: int = field(init=False)

    capacity: int = field(init=False)
    capacity_difference: int = field(init=False)

    local_count: int = field(init=False)
    required_local_count: int = field(init=False)

    locality_difference: int = field(init=False)

    def model_dump(self) -> dict:
        return asdict(self)

    def __post_init__(self, locality_percentage=0.5):
        if locality_percentage < 0 or locality_percentage > 1:
            raise ValueError("Locality percentage must be between 0 and 1")

        if self.teacher_to_student_ratio < 35 or self.teacher_to_student_ratio > 50:
            raise ValueError(
                "Teacher to student ratio must be between 35 and 50"
            )

        self.fulltime_specialist_count = (
            self.local_fulltime_specialist_count
            + self.foreign_fulltime_specialist_count
        )
        self.fulltime_supportive_count = (
            self.local_fulltime_supportive_count
            + self.foreign_fulltime_supportive_count
        )

        if self.fulltime_specialist_count < self.parttime_specialist_count:
            self.allowed_specialist_parttime_count = self.fulltime_specialist_count
        else:
            self.allowed_specialist_parttime_count = self.parttime_specialist_count

        if self.fulltime_supportive_count < self.parttime_supportive_count:
            self.allowed_supportive_parttime_count = self.fulltime_supportive_count
        else:
            self.allowed_supportive_parttime_count = self.parttime_supportive_count

        self.allowed_parttime_count = (
            self.allowed_specialist_parttime_count
            + self.allowed_supportive_parttime_count
        )

        if self.fulltime_specialist_count < self.master_count:
            self.allowed_masters_count = self.fulltime_specialist_count
        else:
            self.allowed_masters_count = self.master_count

        self.capacity = (
            self.allowed_parttime_count
            + self.fulltime_specialist_count
            + self.fulltime_supportive_count
            + math.floor(self.allowed_masters_count / 2)
        ) * self.teacher_to_student_ratio

        self.capacity_difference = self.capacity - self.students_count

        self.required_local_count = math.ceil(
            (
                self.fulltime_specialist_count
                + self.fulltime_supportive_count
                + self.allowed_parttime_count
            )
            * locality_percentage
        )

        self.local_count = (
            self.local_fulltime_specialist_count + self.local_fulltime_supportive_count
        )

        self.locality_difference = self.local_count - self.required_local_count