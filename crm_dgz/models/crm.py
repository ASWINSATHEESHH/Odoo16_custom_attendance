from venv import create

from odoo import models, fields, api
from datetime import datetime, date

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    affiliated_id = fields.Many2one('res.partner', 'Affiliated By')
    stage_duration = fields.Char('Lead Duration', default=0)

    def update_stage_duration(self):
        today = date.today()
        for lead in self.search([]):  # Get all leads
            if lead.create_date:
                delta = (today - lead.create_date.date()).days
                print(lead.create_date.date())
                lead.stage_duration = f"{delta} days"