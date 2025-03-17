odoo.define('attendance_dgz.my_attendance_extension', function (require) {
    "use strict";

    var MyAttendances = require('hr_attendance.my_attendances');
    var core = require('web.core');
    var rpc = require('web.rpc');
    var Dialog = require('web.Dialog');

    MyAttendances.include({
        update_attendance: function () {
            var self = this;
            console.log("Custom update_attendance method triggered");

            rpc.query({
                model: 'hr.attendance',
                method: 'search_read',
                domain: [['employee_id', '=', self.employee.id], ['check_out', '=', false]],
                fields: ['id']
            }).then(function (attendanceRecords) {
                if (attendanceRecords.length > 0) {
                    console.log("Checking out, directly updating the record.");
                    self._processAttendance(null);
                } else {
                    self._fetchWorkLocations();
                }
            }).catch(function (error) {
                console.error("Error checking attendance state:", error);
            });
        },

        _fetchWorkLocations: function () {
            var self = this;

            rpc.query({
                model: 'hr.employee',
                method: 'read',
                args: [[self.employee.id], ['work_location_ids']],
            }).then(function (result) {
                if (result.length > 0 && result[0].work_location_ids.length > 0) {
                    var locationIds = result[0].work_location_ids;

                    rpc.query({
                        model: 'work.locations',
                        method: 'read',
                        args: [locationIds, ['name']],
                    }).then(function (locations) {
                        var locationOptions = locations.map(loc => ({
                            id: loc.id,
                            name: loc.name
                        }));

                        self._showWorkLocationPopup(locationOptions);
                    });
                } else {
                    console.warn("No work locations assigned to this employee.");
                }
            }).catch(function (error) {
                console.error("Error fetching work locations:", error);
            });
        },

        _showWorkLocationPopup: function (locationOptions) {
            var self = this;

            var $content = $("<div>").append(
                $("<label>").text("Select Work Location:"),
                $("<select>", { id: "work_location_select", class: "form-control" })
            );

            locationOptions.forEach(function (location) {
                $("#work_location_select", $content).append(
                    $("<option>", { value: location.id }).text(location.name)
                );
            });

            var dialog = new Dialog(this, {
                title: "Work Location Selection",
                size: "medium",
                $content: $content,
                buttons: [
                    {
                        text: "Confirm",
                        classes: "btn-primary",
                        close: true,
                        click: function () {
                            var selectedLocationId = $("#work_location_select").val();
                            var selectedLocationName = $("#work_location_select option:selected").text();
                            console.log("Selected Work Location ID:", selectedLocationId);
                            console.log("Selected Work Location Name:", selectedLocationName);

                            self._processAttendance(selectedLocationName);
                        },
                    },
                    {
                        text: "Cancel",
                        close: true,
                    },
                ],
            });

            dialog.open();
        },

        _processAttendance: function (locationName) {
            var self = this;
            console.log("Processing attendance for location:", locationName);

            rpc.query({
                model: 'hr.attendance',
                method: 'create_attendance_with_location',
                args: [self.employee.id, locationName],
            }).then(function (response) {
                console.log("Attendance updated successfully with location:", locationName);
                window.location.reload();
            }).catch(function (error) {
                console.error("Error updating attendance:", error);
            });
        },

    });

    return MyAttendances;
});
