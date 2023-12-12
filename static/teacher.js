let schoolDaysCount = 0;


var studentTable;

$(document).ready(function() {
    var sectionTable = $('#sectionTable').DataTable({
        paging: false,
        lengthChange: false,
        info: true, 
        scrollY: '300px',
        scrollCollapse: true,
        scroller: true,
        searching: true,
        language: {
            info: 'Total Students: _TOTAL_', // Customize the info message
        }
    });


    function clearSectionTable() {
        sectionTable.clear().draw();
    }
    
    // Handling the "Clear" button for the section table
    $('#clearButton').click(function() {
        clearSectionTable();
    });

    // Handling the "Refresh" button for the section table
    $('#refreshButton').click(function() {
        fetchStudentDataForSection(); // Function to fetch student data for the teacher's section
    });

    function populateSectionTable(data) {
        sectionTable.clear().draw();
        data.forEach(function (student) {
            sectionTable.row.add([
                student.studentID,
                student.name,
                student.email,
                student.section
            ]).draw(false);
        });
    }

    function fetchStudentDataForSection() {
        $.ajax({
            url: '/get_students_for_section', // Replace with the actual API endpoint to get students for the teacher's section
            method: 'GET',
            success: function (data) {
                populateSectionTable(data);
            },
            error: function (error) {
                console.error('Error fetching student data:', error);
            }
        });
    }

    // Add the new code for the reports table
    var reportsTable = $('#reportsTable').DataTable({
        paging: false,
        lengthChange: false,
        info: false,
        scrollY: '300px',
        scrollCollapse: true,
        scroller: true,
        searching: true
    });

    function populateReportsTable(data) {
        reportsTable.clear().draw();
        data.forEach(function (report) {
            reportsTable.row.add([
                report.name,
                report.section,
                report.timestamp,
                report.description,
                report.status
            ]).draw(false);
        });
    }
    
    function clearReportsTable() {
        reportsTable.clear().draw();
    }

    // Handling the "Refresh" button for the reports table
    $('#refreshReportsButton').click(function() {
        fetchReportsForSection(); // Function to fetch reports for the teacher's section
    });

    // Fetch and populate reports data for the teacher's section
    function fetchReportsForSection() {
        $.ajax({
            url: '/get_reports_for_section', // Replace with the actual API endpoint to get reports for the teacher's section
            method: 'GET',
            success: function (data) {
                populateReportsTable(data);
            },
            error: function (error) {
                console.error('Error fetching reports:', error);
            }
        });
    }

    // Handling the "Clear Reports" button
    $('#clearReportsButton').click(function() {
        clearReportsTable();
    });

    // Add the new code for the attendance table
    var attendanceTable = $('#attendanceTable').DataTable({
        paging: false,
        lengthChange: false,
        info: false,
        scrollY: '300px',
        scrollCollapse: true,
        scroller: true,
        searching: true
    });

    function populateAttendanceTable(data) {
        attendanceTable.clear().draw();
        data.forEach(function (student) {
            attendanceTable.row.add([
                student.studentID,
                student.name,
                student.attendance
            ]).draw(false);
        });
    }

    // Handling the "Refresh" button for the attendance table
    $('#refreshAttendanceButton').click(function() {
        fetchAttendanceDataForSection(); // Function to fetch attendance data for the teacher's section
    });

    // Fetch and populate attendance data for the teacher's section
    function fetchAttendanceDataForSection() {
        $.ajax({
            url: '/get_attendance_for_section', // Replace with the actual API endpoint to get attendance data for the teacher's section
            method: 'GET',
            success: function (data) {
                populateAttendanceTable(data);
            },
            error: function (error) {
                console.error('Error fetching attendance data:', error);
            }
        });
    }

    // Handling the "Clear Attendance" button
    $('#clearAttendanceButton').click(function() {
        clearAttendanceTable();
    });

    function clearAttendanceTable() {
        attendanceTable.clear().draw();
    }

    // Initial fetch of attendance data when the page loads
    fetchAttendanceDataForSection();

    $('#openModalButton').click(function() {
        // Function to fetch all student records and display them in the modal
        function fetchAllStudents() {
            $.ajax({
                url: '/get_all_students', // Replace with the actual API endpoint to get all student records
                method: 'GET',
                success: function(data) {
                    if (data && data.length > 0) {
                        if ($.fn.DataTable.isDataTable('#studentTable')) {
                            // If the DataTable is already initialized, destroy it first
                            studentTable.destroy();
                        }

                        studentTable = $('#studentTable').DataTable({
                            paging: false,
                            lengthChange: false,
                            info: false,
                            scrollY: '300px',
                            scrollCollapse: true,
                            searching: true,
                            ordering: false, // Disable column sorting
                            columns: [
                                { title: "Student ID" },
                                { title: "Name" },
                                { title: "Email" },
                                { title: "NFC Tag" },
                                { title: "Section" },
                                { title: "Grade Level" },
                                {
                                    title: "Edit",
                                    data: null,
                                    defaultContent: '<button class="edit-button">Edit</button>',
                                },
                            ],
                        });

                        studentTable.clear().draw();
                        data.forEach(function(student) {
                            studentTable.row.add([
                                student.studentID,
                                student.name,
                                student.email,
                                student.nfcTag,
                                student.section,
                                student.grade_level,
                                '<button class="edit-button" data-student-id="' + student.studentID + '">Edit</button>'
                            ]).draw(false);
                        });

                        $('#studentModal').modal('show');

                        // Handle the "Edit" button click within the student data table
                        $('#studentTable').on('click', '.edit-button', function() {
                            // Remove the "selected" class from all rows
                            $('#studentTable tr.selected').removeClass('selected');

                            // Add the "selected" class to the parent row of the clicked button
                            $(this).closest('tr').addClass('selected');
                        });
                    }
                },
                error: function(error) {
                    console.error('Error fetching student records:', error);
                }
            });
        }

        // Fetch all student records when the modal is opened
        fetchAllStudents();
    });
   
    let studentID;
   // Handle the "Edit" button click within the student data table
$('#studentTable').on('click', '.edit-button', function() {
    // Get the data of the clicked row
    var rowData = studentTable.row($(this).parents('tr')).data();
    studentID = rowData[0]; // Assuming the first column is the student ID

    console.log('studentID:', studentID);
    // Use this studentID to fetch the student's data and populate the edit form
    // You can make an AJAX request to get the student details and populate the form

    // For example, assuming you have an endpoint '/get_student_data' to get student details
    $.ajax({
        url: '/get_student_data',
        method: 'GET',
        data: { studentID: studentID },
        success: function(data) {
            // Populate the edit form fields with the student's data
            $('#editStudentID').val(studentID);
            $('#editStudentName').val(data.name);
            $('#editStudentEmail').val(data.email);
            $('#editStudentNfcTag').val(data.nfcTag);
            $('#editStudentSection').val(data.section);
            $('#editStudentGradeLevel').val(data.grade_level);
        },
        error: function(error) {
            console.error('Error fetching student data:', error);
        }
    });

    // Show the edit modal
    $('#editStudentModal').modal('show');
});

// Handle the "Save" button click within the edit modal
$('#saveEditButton').click(function() {
    var editedStudentData = {
        studentID: $('#editStudentID').val(), // Include studentID
        name: $('#editStudentName').val(),
        email: $('#editStudentEmail').val(),
        nfcTag: $('#editStudentNfcTag').val(),
        section: $('#editStudentSection').val(),
        grade_level: $('#editStudentGradeLevel').val()
    };

    console.log('Edited Student Data:', editedStudentData);

    $.ajax({
        url: '/update_student_data/' + studentID,
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(editedStudentData),
        success: function(response) {
            console.log(response.message);
            // Handle success as needed, e.g., close the modal
            $('#editStudentModal').modal('hide');
        },
        error: function(error) {
            console.error('Error updating student data:', error);
        }
    });

    // Update the DataTable row with the edited data
    var selectedRow = studentTable.row('.selected');

    if (selectedRow && selectedRow.length) {
        var rowData = selectedRow.data();
        console.log('Row Data:', rowData);

        if (rowData && rowData.length >= 6) {
            rowData[0] = editedStudentData.studentID; // Update studentID
            rowData[1] = editedStudentData.name;
            rowData[2] = editedStudentData.email;
            rowData[3] = editedStudentData.nfcTag;
            rowData[4] = editedStudentData.section;
            rowData[5] = editedStudentData.grade_level;

            selectedRow.data(rowData);
            studentTable.draw(); // Redraw the DataTable
        } else {
            console.error('Invalid data structure in the selected row.');
        }
    } else {
        console.error('Selected row not found or invalid data.');
    }


    // Close the edit modal
    $('#editStudentModal').modal('hide');
});



$('#customOpenModalButton').click(function () {
    $('#attendanceModal').modal('show');
});

$('#closeCustomModalButton').click(function () {
    $('#attendanceModal').modal('hide');
});


// Handle the "Filter" button click for the attendance modal
$('#filterAttendanceButton').click(function () {
    // Get the filter criteria (date and status) from the form
    var date = $('#filterDateInput').val();
    var status = $('input[name="statusRadio"]:checked').val(); // Assuming you are using radio buttons

    // Send an AJAX request to the server to fetch filtered attendance records
    $.ajax({
        url: '/get_filtered_attendance',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ date: date, status: status }),
        success: function (data) {
            // Clear the existing table and populate it with filtered records
            var attendanceTable = $('#filteredAttendanceTable').DataTable();
            attendanceTable.clear().draw();
            data.forEach(function (student) {
                attendanceTable.row.add([
                    student.studentID,
                    student.name,
                    student.email,
                    student.date,
                    student.status,
                    student.section
                ]).draw(false);
            });
        },
        error: function (error) {
            console.error('Error fetching filtered attendance data:', error);
        }
    });
});

// Initialize the attendance modal and fetch initial attendance data
$('#attendanceModal').on('show.bs.modal', function (e) {
    // Clear the filter form
    $('#filterDateInput').val('');

    // Ensure "Present" is selected by default (if using radio buttons)
    $('input[name="statusRadio"][value="Present"]').prop('checked', true);
    $('input[name="statusRadio"][value="Absent"]').prop('checked', false);

    // Fetch and display initial attendance data for the teacher's section
    fetchInitialAttendanceDataForSection();
});

// Function to fetch and populate initial attendance data for the teacher's section
function fetchInitialAttendanceDataForSection() {
    $.ajax({
        url: '/get_initial_attendance_data', // Replace with your actual API endpoint
        method: 'GET',
        success: function(data) {
            // Populate the attendance table in the modal with initial data
            updateAttendanceTable(data);
        },
        error: function(error) {
            console.error('Error fetching initial attendance data:', error);
        }
    });
}

// Function to populate the attendance table in the attendance modal
function updateAttendanceTable(data) {
    var attendanceTable = $('#filteredAttendanceTable').DataTable(); // Assuming you want to populate the attendance modal's table
    attendanceTable.clear().draw();
    data.forEach(function(student) {
        attendanceTable.row.add([
            student.studentID,
            student.name,
            student.email,
            student.date,
            student.status,
            student.section
        ]).draw(false);
    });
}


});
