class AiderOperatingLayer:
    """
    Future layer:
    - code mutation proposals
    - safe patch generation
    - architecture-aware edits
    """

    def propose_patch(self, violation):
        return {
            "action": "review_required",
            "target": violation.file,
            "rule": violation.rule
        }
