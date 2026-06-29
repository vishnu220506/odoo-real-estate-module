from odoo import api, models, fields
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Properties"

    _sql_constraints = [
        (
            "check_expected_price",
            "CHECK(expected_price > 0)",
            "The expected price must be strictly positive.",
        ),
        (
            "check_selling_price",
            "CHECK(selling_price >= 0)",
            "The selling price must be positive.",
        ),
    ]

    name = fields.Char(required=True)
    date_availability = fields.Date()
    description = fields.Text()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    has_garden = fields.Boolean()
    garden_area = fields.Integer()
    expected_price = fields.Float()
    selling_price = fields.Float()
    total_area = fields.Integer(compute="_compute_total_area")

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner")
    salesperson_id = fields.Many2one(
        "res.users",
        string="Real Estate Agent",
        default=lambda self: self.env.user,
    )
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
    )

    best_price = fields.Float(compute="_compute_best_price")

    @api.depends("living_area", "garden_area", "has_garden")
    def _compute_total_area(self):
        for record in self:
            if record.has_garden:
                record.total_area = record.living_area + record.garden_area
            else:
                record.total_area = record.living_area

    def sell_property(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("Cancelled properties cannot be sold")
            else:
                record.state = "sold"

    def cancel_property(self):
        for record in self:
            if record.state == "sold":
                raise UserError("sold properties cannot be cancelled")
            else:
                record.state = "cancelled"

    @api.constrains("expected_price", "selling_price")
    def _check_valid_selling_price(self):
        for record in self:
            if (
                float_compare(
                    record.selling_price,
                    0.9 * record.expected_price,
                    precision_digits=2,
                ) < 0
                and not float_is_zero(record.selling_price, precision_digits=2)
            ):
                raise ValidationError(
                    "selling price must be at least 90 percent of the expected price"
                )

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0.0