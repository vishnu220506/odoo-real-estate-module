from odoo import api, models, fields
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offers on the real estate properties"

    _sql_constraints = [
        (
            "check_offer_price",
            "CHECK(price > 0)",
            "The offer price must be positive.",
        ),
    ]

    price = fields.Float()
    partner_id = fields.Many2one("res.partner")
    property_id = fields.Many2one("estate.property")
    state = fields.Selection(
        [
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        string="Status",
    )

    def accept_offer(self):
        for record in self:
            if record.property_id.state == "offer_accepted":
                raise UserError("This property already has an accepted offer")
            elif record.state == "refused":
                raise UserError("You can't accept a refused offer")
            else:
                record.state = "accepted"
                record.property_id.buyer_id = record.partner_id
                record.property_id.state = "offer_accepted"
                record.property_id.selling_price = record.price

    def refuse_offer(self):
        for record in self:
            if record.state == "accepted":
                raise UserError("Accepted offers cannot be refused")
            else:
                record.state = "refused"