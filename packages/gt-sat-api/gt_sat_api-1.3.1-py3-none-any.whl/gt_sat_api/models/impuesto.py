from dataclasses import dataclass


@dataclass
class Impuesto:
    """Agrupa los datos de un Impuesto."""

    nombre_corto: str
    codigo_unidad_gravable: int
    monto_gravable: float

    tax_percentage = 12.0

    @property
    def monto_impuesto(self) -> float:
        """Get monto_impuesto based on tax_percentage and monto_gravable

        Returns:
            float
        """
        _monto_impuesto = self.tax_percentage / 100 * self.monto_gravable
        return _monto_impuesto
