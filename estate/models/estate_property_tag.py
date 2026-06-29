from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tags"

    _sql_constraints = [
        (
            "unique_tag_name",
            "UNIQUE(name)",
            "The tag name must be unique.",
        ),
    ]

    name = fields.Char(required=True)
    color = fields.Integer("Color")