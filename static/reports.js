var $j = jQuery.noConflict();
var reportsTable;

$j(document).ready(function() {
    reportsTable = $j('#reportsTable').DataTable({
        "ajax": {
            "url": "/get_reports",
            "dataSrc": "data"
        }, 
        "columns": [
            { "data": "reportID" },
            { "data": "name" },
            { "data": "section" },
            { "data": "timestamp" },
            { "data": "description" },
            { "data": "status" },
            { "data": "role" },
            { "data": "grade_level" },
            { "data": null, "orderable": false, "render": function(data, type, full, meta) {
                return '<input type="checkbox" class="report-checkbox" value="' + full.reportID + '">';
            }}
        ],
        "initComplete": function(settings, json) {
            // Filter by Status
            $j('#statusFilter').on('change', function () {
                reportsTable.column(5).search($j(this).val()).draw();
            });

            // Filter by Role
            $j('#roleFilter').on('change', function () {
                reportsTable.column(6).search($j('#roleFilter').val()).draw();
            });

            // Filter by Grade Level
            $j('#gradeFilter').on('change', function () {
                reportsTable.column(7).search($j('#gradeFilter').val()).draw();
            });

            // Handle Mark as Resolved button
            $j('#markResolvedButton').on('click', function () {
                var selectedReportIDs = $j('.report-checkbox:checked').map(function() {
                    return $j(this).val();
                }).get();

                if (selectedReportIDs.length > 0) {
                    $j.ajax({
                        type: 'POST',
                        url: '/mark_resolved',
                        data: JSON.stringify({ reportIDs: selectedReportIDs }),
                        contentType: 'application/json',
                        success: function(data) {
                            // Handle success, e.g., update UI or refresh the table
                            console.log(data.message);
                        },
                        error: function(error) {
                            // Handle error
                            console.error(error);
                        }
                    });
                }
            });

            // Handle Mark as Unresolved button (similar to Mark as Resolved)
            $j('#markUnresolvedButton').on('click', function () {
                // Implement the same AJAX logic for marking as unresolved
            });

            // Handle Delete Selected button
            $j('#deleteSelectedButton').on('click', function () {
                var selectedReportIDs = $j('.report-checkbox:checked').map(function() {
                    return $j(this).val();
                }).get();

                if (selectedReportIDs.length > 0) {
                    // Implement the logic for deleting selected reports
                }
            });
        },
        "paging": true,
        "lengthChange": false,
        "info": false,
        "lengthMenu": [5]
    });

    $j('#selectAllButton').on('click', function () {
        $j('.report-checkbox').prop('checked', true);
    });

    // Handle Deselect All button
    $j('#deselectAllButton').on('click', function () {
        $j('.report-checkbox').prop('checked', false);
    });

    $j('#markResolvedButton').on('click', function () {
        var selectedReportIDs = $j('.report-checkbox:checked').map(function() {
            return $j(this).val();
        }).get();
    
        if (selectedReportIDs.length > 0) {
            $j.ajax({
                type: 'POST',
                url: '/mark_resolved',
                data: JSON.stringify({ reportIDs: selectedReportIDs }),
                contentType: 'application/json',
                success: function(data) {
                    // Handle success, e.g., update UI or refresh the table
                    console.log(data.message);
                    // Reload the DataTable
                    reportsTable.ajax.reload();
                },
                error: function(error) {
                    // Handle error
                    console.error(error);
                }
            });
        }
    });
    
    $j('#markUnresolvedButton').on('click', function () {
        var selectedReportIDs = $j('.report-checkbox:checked').map(function() {
            return $j(this).val();
        }).get();
    
        if (selectedReportIDs.length > 0) {
            $j.ajax({
                type: 'POST',
                url: '/mark_unresolved',
                data: JSON.stringify({ reportIDs: selectedReportIDs }),
                contentType: 'application/json',
                success: function(data) {
                    // Handle success, e.g., update UI or refresh the table
                    console.log(data.message);
                    // Reload the DataTable
                    reportsTable.ajax.reload();
                },
                error: function(error) {
                    // Handle error
                    console.error(error);
                }
            });
        }


});



$j('#deleteSelectedButton').on('click', function () {
    var selectedReportIDs = $j('.report-checkbox:checked').map(function() {
        return $j(this).val();
    }).get();

    if (selectedReportIDs.length > 0) {
        $j.ajax({
            type: 'POST',
            url: '/delete_reports',
            data: JSON.stringify({ reportIDs: selectedReportIDs }),
            contentType: 'application/json',
            success: function(data) {
                // Handle success, e.g., update UI or refresh the table
                console.log(data.message);
                // Reload the DataTable
                reportsTable.ajax.reload();
            },
            error: function(error) {
                // Handle error
                console.error(error);
            }
        });
    }

});




});
