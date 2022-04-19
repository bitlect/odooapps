# -*- coding: utf-8 -*-


from hashlib import new
import logging
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.addons.license_manager.utils.key_generator import Key
from odoo.addons.license_manager.utils.date_tools import months_between

import datetime

_logger = logging.getLogger(__name__)
class License(models.Model):

    _name="lm.license"
    _description = "License"

    state = fields.Selection([
        ('deactivate','Deactivated'),
        ('activate','Activated'),
        ('expired','Expired')],
        default="deactivate"
    )

    name = fields.Char()
    partner_id = fields.Many2one("res.partner",string="Partner",required=True)
    product_id = fields.Many2one(
        "product.product",
        "Product",
        domain="[('type','=','service')]",
        required=True
    )
    date_from = fields.Datetime('Valid From', required=True)
    date_to = fields.Datetime('Valid Till', required=True)
    duration = fields.Integer('Duration(months)', compute="_compute_duration")
    license_key = fields.Char(string="License Key")
    dbuuid = fields.Char('Database UUID', required=True)
    eula_id = fields.Many2one('lm.eula','EULA')
    eula_html = fields.Html(
        "EULA Content", 
        compute="_compute_eula_html", 
        inverse="_inverse_eula_html"
    )


    @api.depends('eula_id')
    def _compute_eula_html(self):
        for rec in self:
            if rec.eula_id:
                rec.eula_html = rec.eula_id.content
            else:
                rec.eula_html = False


    @api.depends('eula_id')
    def _inverse_eula_html(self):
        for rec in self:
            return True

    @api.depends('date_from','date_to')
    def _compute_duration(self):
        for rec in self:
            if rec.date_from and rec.date_to:
                rec.duration = months_between(rec.date_from, rec.date_to)
            else:
                rec.duration = False

# --------------------------------------------
# Onchange methods & Constraints
# --------------------------------------------
    # @api.constrains('date_from')
    # def _check_date_from(self):
    #     today = fields.Datetime.now()
    #     if self.date_from and self.date_from < today:
    #         raise ValidationError(_(
    #             "The selected Start Date {start_dt} cannot be less than today"
    #         ).format(
    #             start_dt = self.date_from
    #         ))


    @api.onchange('date_to')
    def _onchange_end_date(self):
        end_date = self.date_to
        if self.date_to and self.date_from and (self.date_to < self.date_from):
            raise ValidationError(_(
                "End date {end_dt} cannot be less than the start date {start_dt}"
            ).format(
                end_dt = end_date,  
                start_dt = self.date_from
            ))


# --------------------------------------------
# ORM Methods Override
# --------------------------------------------
    @api.model
    def create(self, vals):
        res = super(License, self).create(vals)
        seq = self.env['ir.sequence'].next_by_code('license.name') or '/'
        #check if user inputed the name "manually"
        if 'name' in vals and vals.get('name'):
            seq = vals.get("name")
        res.write({'name': seq})
        return res

# --------------------------------------------
# Business logic
# --------------------------------------------
    def action_activate(self):
        for rec in self:
            if not rec.license_key:
                raise ValidationError(_('Please generate a license key before activation'))
            rec.write({'state':'activate'})

    def action_deactivate(self):
        self.write({'state':'deactivate'})

    def generate_license_key(self):
        for rec in self:
            if not rec.license_key:
                key = Key()
                _logger.info(f"LICENSE KEY => {key}")
                data = str(key).split(":")
                if data and data[1] == 'Valid':
                    rec.license_key = data[0]


class Eula(models.Model):

    _name="lm.eula"
    _description = "End User License Agreement (EULA)"

    
    name = fields.Char('Name of the agreement',required=True)
    content = fields.Html()


 

