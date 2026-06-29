from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Types"

    _sql_constraints = [
        (
            "unique_type_name",
            "UNIQUE(name)",
            "The property type must be unique.",
        ),
    ]

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")