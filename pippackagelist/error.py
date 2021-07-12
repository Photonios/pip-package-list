from .entry import RequirementsEntry


class ConstraintWithoutNameError(RuntimeError):
    def __init__(self, requirement: RequirementsEntry) -> None:
        super().__init__(f"Constraint '{requirement}' does not have a name")
