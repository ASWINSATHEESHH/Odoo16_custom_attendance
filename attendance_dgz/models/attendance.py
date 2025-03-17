# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime, time, timedelta


class AttendanceDGZ(models.Model):
    _inherit = 'hr.attendance'
    _description = 'Attendance DGZ'

    work_location_id = fields.Many2one('work.locations',string='Work Location')
    status = fields.Selection([('on_time', 'On Time'), ('late', 'Late')], string='Status', compute='_compute_status',
                              store=True)

    @api.depends('check_in')
    def _compute_status(self):
        for record in self:
            check_in_time = fields.Datetime.from_string(record.check_in) + timedelta(hours=5, minutes=30)
            threshold_time = time(9, 10)
            if check_in_time.time() > threshold_time:
                record.status = 'late'
            elif check_in_time.time() < threshold_time:
                record.status = 'on_time'

    @api.model
    def create_attendance_with_location(self, employee_id, work_location_name=None):
        """Create attendance and store the selected work location if checking in, else check out."""
        employee = self.env['hr.employee'].browse(employee_id)

        # Check if there is an active (unchecked-out) attendance record
        attendance = self.env['hr.attendance'].search([
            ('employee_id', '=', employee.id),
            ('check_out', '=', False)
        ], limit=1)

        if attendance:
            # If an open record exists, update check-out time
            attendance.write({'check_out': fields.Datetime.now()})
            return {'status': 'checked_out', 'attendance_id': attendance.id}

        # If no open record exists, it's a check-in
        if work_location_name:
            work_location = self.env['work.locations'].search([('name', '=', work_location_name)], limit=1)
            if not work_location:
                raise ValueError(f"Work location '{work_location_name}' not found.")

            attendance = self.env['hr.attendance'].create({
                'employee_id': employee.id,
                'check_in': fields.Datetime.now(),
                'work_location_id': work_location.id,  # Store the work location ID
            })
            return {'status': 'checked_in', 'attendance_id': attendance.id}

        return {'status': 'error', 'message': 'Invalid attendance action'}

    @api.model
    def auto_checkout_attendance(self):
        records_not_check_out = self.search([('check_out', '=', False)])
        current_datetime = fields.Datetime.now()
        threshold_time = time(22, 0)  # 10 PM
        current_time = (current_datetime + timedelta(hours=5, minutes=30)).time()

        print("Current Time:", current_time)
        print("Threshold Time:", threshold_time)

        for record in records_not_check_out:
            if current_time >= threshold_time:
                print("Current time is past 10 PM. Checking out...")

                next_day = current_datetime.date() + timedelta(days=0)
                store_time = time(16, 30)
                check_out_datetime = datetime.combine(next_day, store_time)

                print("Check-out datetime:", check_out_datetime)
                record.write({'check_out': check_out_datetime})
            else:
                print("Current time is before 10 PM. No action taken.")

        return True
