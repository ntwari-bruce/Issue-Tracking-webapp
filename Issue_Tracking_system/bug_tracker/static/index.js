$(document).on('click', '.edit-linkp', function () {
  var projectId = $(this).data('project-id');
  console.log(projectId)
  // Rest of the code to open the modal and retrieve project details
  $.ajax({
    url: '/api/project/' + projectId,
    type: 'GET',
    success: function (response) {
      var project = response.project;

      // Set the project details in the modal
      $('#Project_name').val(project.project_name);
      $('#project_id').val(projectId);
      $('#project_description').val(project.project_description);
      $('#selx').val(project.team_members);

      // Open the modal
      $('#myModalp').modal('show');
    },
    error: function (xhr, status, error) {
      // Handle error
      console.log(error);
    }
  });
});

