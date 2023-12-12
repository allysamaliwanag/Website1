$(document).ready(function () {
    // Initialize the flatpickr date picker

    function getTeacherInfo() {
        // Get the student's teacher information
        $.get('/get_teacher_for_student', function (data) {
            if (data.error) {
                alert(data.error);
            } else { 
                // Update the modal with teacher information
                $('#teacherName').text(data.name);
                $('#teacherEmail').text(data.email);
                $('#teacherSection').text(data.section);
                $('#teacherGradeLevel').text(data.grade_level);
                $('#teacherModal').modal('show');
            }
        });
    }

 
    function filterAttendanceRecords() {
        const statusFilter = $("#statusFilter").val();
        const selectedDate = $("#dateFilter").val();

        if (studentID && selectedDate) {
            $.get('/get_filtered_attendance_records', {
                studentID: studentID,
                statusFilter: statusFilter,
                selectedDate: selectedDate,
            }, function (data) {
                const table = $('#attendanceRecordsTable');
                table.empty();

                let presentCount = 0;
                let absentCount = 0;

                if (data.length > 0) {
                    data.forEach(function (record) {
                        const row = $("<tr>");
                        row.append($("<td>").text(record.date));
                        row.append($("<td>").text(record.status));
                        table.append(row);

                        if (record.status === 'Present') {
                            presentCount++;
                        } else if (record.status === 'Absent') {
                            absentCount++;
                        }
                    });
                } else {
                    alert("No attendance records found for this student.");
                }

                $('#presentCount').text(presentCount);
                $('#absentCount').text(absentCount);
            });
        } else {
            alert("Student session not established. Please log in.");
        }
    }

    // Initialize Flatpickr for the date filter input with calendar
    flatpickr("#dateFilter", {
        dateFormat: "Y-m-d",
        enableTime: false,
        inline: false,
        enable: [
            function (date) {
                return true;
            }
        ],
    });

    // Add click event handlers to the buttons
    $('#teacherInfoBtn').click(function () {
        getTeacherInfo();
    });

    $('#filterRecordsBtn').click(function () {
        filterAttendanceRecords();
    });

    $('#clearDateFilterBtn').click(function () {
        $("#dateFilter").flatpickr().clear();
        filterAttendanceRecords();
    });

    // Call getAttendanceRecords() when the page loads
    filterAttendanceRecords();
});