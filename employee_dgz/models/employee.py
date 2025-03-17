# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Hr_Employee(models.Model):
     _inherit = 'hr.employee'
     _description = 'employee_dgz.employee_dgz'

     work_location_ids = fields.Many2many('work.locations')


class WorkLocation(models.Model):

    _name = 'work.locations'
    _rec_name = 'name'

    name = fields.Char('Locations')
