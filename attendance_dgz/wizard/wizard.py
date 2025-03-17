from odoo import models, fields, api

class HrAttendanceWizard(models.TransientModel):
    _name = 'hr.attendance.wizard'
    _description = 'Attendance Confirmation Wizard'

    work_location_id = fields.Many2one('work.locations', string="Work Location", required=True)
    employee_id = fields.Many2one('hr.employee', string="Employee", required=True)

    def action_confirm_attendance(self):
        """ This method will be triggered when clicking the confirm button in the wizard. """
        active_id = self.env.context.get('active_id')
        if active_id:
            attendance = self.env['hr.attendance'].browse(active_id)
            attendance.write({'work_location_id': self.work_location_id.id})
        return {'type': 'ir.actions.act_window_close'}
