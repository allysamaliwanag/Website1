$(document).ready(function() {
    var table = $('#usersTable').DataTable();

    // Function to update the table with search results
    function updateTable(data) {
        table.clear().draw();
        data.forEach(function (user) {

            
            // Create the edit button and checkbox elements
        var editButton = '';
        var deleteButton = '<button class="deleteUser btn btn-danger">Delete</button>';
        var actions = editButton + ' ' + deleteButton;
        
        // Add the user data and the edit button and delete button to the row
        table.row.add([user.id, user.name, user.email, user.role, user.section, actions]).draw();
        });
    }
    
    // Handle the "Edit" button click to populate the modal with user data
    $('#usersTable tbody').on('click', 'button.editUser', function () {
        var data = table.row($(this).parents('tr')).data();
        // Get the user data from the row
        var userId = data[0];
        var userName = data[1];
        var userEmail = data[2];
        var userRole = data[3];
        var userSection = data[4];
        
        // Populate the modal fields
        $('#editUserId').val(userId);
        $('#editName').val(userName);
        $('#editEmail').val(userEmail);
        $('#editRole').val(userRole);
        $('#editSection').val(userSection);
        
        // Open the modal
        $('#editModal').modal('show');
    });

    // Handle the "Save Changes" button click to update user data
    $('#saveChanges').click(function () {
        // Get the updated user data from the modal fields
        var userId = $('#editUserId').val();
        var updatedName = $('#editName').val();
        var updatedEmail = $('#editEmail').val();
        var updatedRole = $('#editRole').val();
        var updatedSection = $('#editSection').val();
        
        // Make an AJAX request to update the user data
        $.ajax({
            type: 'POST',
            url: '/update_user',
            data: {
                userId: userId,
                name: updatedName,
                email: updatedEmail,
                role: updatedRole,
                section: updatedSection
            },
            success: function (response) {
                if (response.message === 'Update successful') {
                    // Update the user data in the DataTable
                    var row = table.row($(this).parents('tr'));
                    var rowData = row.data();
                    rowData[1] = updatedName; // Update the name column
                    rowData[2] = updatedEmail; // Update the email column
                    rowData[3] = updatedRole; // Update the role column
                    rowData[4] = updatedSection; // Update the section column
                    row.data(rowData).draw();
                    
                    // Close the modal
                    $('#editModal').modal('hide');
                } else {
                    alert('Update failed');
                }
            },
            error: function (error) {
                console.log(error);
            }
        });
    });

    // Handle the search button click
    $('#searchButton').click(function () {
        var searchQuery = $('#searchQuery').val();
        var roleFilter = $('#roleFilter').val();

        // Make an AJAX request to the Flask route (adjust the route as needed)
        $.ajax({
            type: 'POST',
            url: '/search_users',
            data: { search_query: searchQuery },
            success: function (response) {
                if (roleFilter === 'all') {
                    updateTable(response.students.concat(response.teachers));
                } else if (roleFilter === 'student') {
                    updateTable(response.students);
                } else if (roleFilter === 'teacher') {
                    updateTable(response.teachers);
                }
            },
            error: function (error) {
                console.log(error);
            }
        });
    });

// Handle the "Delete" button click
$('#usersTable tbody').on('click', 'button.deleteUser', function () {
    var data = table.row($(this).parents('tr')).data();
    var userId = data[0];
    var userRole = data[3];

    // Make an AJAX request to delete the user
    $.ajax({
        type: 'POST',
        url: '/delete_user',
        data: { role: userRole, userId: userId },
        success: function (response) {
            // Remove the row from the DataTable upon successful deletion
            table.row($(this).parents('tr')).remove().draw();
            table.draw();
        },
        error: function (error) {
            console.log(error);
        }
    });
});

});
