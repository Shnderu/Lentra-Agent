from lentra.core.typesystem.contracts.layer_matrix import (
    ALLOWED_CONNECTIONS
)


class LayerTypeViolation(Exception):
    pass


class TypeValidator:

    @staticmethod
    def validate(source_type, target_type):

        allowed = ALLOWED_CONNECTIONS.get(
            source_type,
            set()
        )

        if target_type not in allowed:
            raise LayerTypeViolation(
                f"{source_type} -> {target_type} forbidden"
            )

        return True
