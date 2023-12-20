// edititing project
$(document).on("click", ".edit-linkp", function () {
  var projectId = $(this).data("project-id");
  console.log(projectId);
  // Rest of the code to open the modal and retrieve project details
  $.ajax({
    url: "/api/project/" + projectId,
    type: "GET",
    success: function (response) {
      var project = response.project;

      // Set the project details in the modal
      $("#Project_name").val(project.project_name);
      $("#project_id").val(projectId);
      $("#project_description").val(project.project_description);
      $("#selx").val(project.team_members);

      // Open the modal
      $("#myModalp").modal("show");
    },
    error: function (xhr, status, error) {
      // Handle error
      console.log(error);
    },
  });
});

// Get the CSRF token from the cookie
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      // Check if the cookie name matches the CSRF cookie name
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Deleting a project
$(document).on("click", ".delete-linkp", function () {
  var projectId = $(this).data("project-id");
  console.log(projectId);

  // Show a confirmation dialog before deleting the project
  if (confirm("Are you sure you want to delete this project?")) {
    // Get the CSRF token
    var csrftoken = getCookie("csrftoken");

    // Send a DELETE request to the server
    $.ajax({
      url: "/api/delete_project/" + projectId,
      type: "DELETE",
      beforeSend: function (xhr) {
        // Set the CSRF token in the request header
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      },
      success: function (response) {
        // Handle the success response
        alert("Project deleted successfully");
        location.reload();
      },
      error: function (xhr, status, error) {
        // For example, you can show an error message
        console.log(error);
        alert("An error occurred while deleting the project");
      },
    });
  }
});

// Removing a team member from the project
$(document).on("click", ".remove-link", function () {
  var member_id = $(this).data("member-id");
  var project_id = $(this).data("project-id");
  console.log(project_id);
  console.log(member_id);

  // Show a confirmation dialog before removing the team member
  if (confirm("Are you sure you want to remove this team member?")) {
    // Get the CSRF token
    var csrftoken = getCookie("csrftoken");

    // Send a DELETE request to the server
    $.ajax({
      url: "/project_view/" + project_id + "/delete_member/" + member_id + "/",
      type: "DELETE",
      beforeSend: function (xhr) {
        // Set the CSRF token in the request header
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      },
      success: function (response) {
        // Handle the success response
        alert("Team member removed successfully");
        location.reload();
      },
      error: function (xhr, status, error) {
        // For example, you can show an error message
        console.log(error);
        alert("An error occurred while removing the team member");
      },
    });
  }
});

// edititing the ticket
$(document).on("click", ".edit-ticket-link", function () {
  var project_id = $(this).data("project-id");
  var ticket_id = $(this).data("ticket-id");
  console.log("this is the id");
  console.log(project_id);
  console.log(ticket_id);
  $.ajax({
    url: "/project_view/" + project_id + "/edit_ticket/" + ticket_id + "/",
    type: "GET",
    dataType: "json",
    success: function (response) {
      console.log(response);
      var ticket = response.ticket;

      console.log(ticket);

      // Set the project details in the modal
      $("#ticket-title").val(ticket.title);
      $("#ticket-description").val(ticket.description);
      $("#ticket-time").val(ticket.estimated_time);
      $("#ticket-type").val(ticket.ticket_type);
      $("#ticket-priority").val(ticket.priority);
      $("#ticket-status").val(ticket.status);
      $("#ticket_id").val(ticket_id);
      $("#ticket-sel").val(
        ticket.assigned_devs.map(function (dev) {
          return dev.id;
        })
      );

      // Open the modal
      $("#myModal2").modal("show");
    },
    error: function (xhr, status, error) {
      // Handle error
      console.log(error);
    },
  });
});

// Deleting the ticket
$(document).on("click", ".delete-ticket-link", function () {
  var ticket_id = $(this).data("ticket-id");
  var project_id = $(this).data("project-id");
  console.log(project_id);
  console.log(ticket_id);

  // Show a confirmation dialog before removing the team member
  if (confirm("Are you sure you want to delete this Ticket?")) {
    // Get the CSRF token
    var csrftoken = getCookie("csrftoken");

    // Send a DELETE request to the server
    $.ajax({
      url: "/project_view/" + project_id + "/delete_ticket/" + ticket_id + "/",
      type: "DELETE",
      beforeSend: function (xhr) {
        // Set the CSRF token in the request header
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      },
      success: function (response) {
        // Handle the success response
        alert("Ticket Deleted successfully");
        location.reload();
      },
      error: function (xhr, status, error) {
        // For example, you can show an error message
        console.log(error);
        alert("An error occurred while deleting the ticket");
      },
    });
  }
});
document.addEventListener("DOMContentLoaded", function () {
  // Function to handle the click event on the ticket row
  function handleTicketClick(event) {
    const ticketId = event.currentTarget.dataset.ticketId;
    const projectId = event.currentTarget.dataset.projectId;

    function getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie !== "") {
        var cookies = document.cookie.split(";");
        for (var i = 0; i < cookies.length; i++) {
          var cookie = cookies[i].trim();
          // Check if the cookie name matches the CSRF cookie name
          if (cookie.substring(0, name.length + 1) === name + "=") {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }

    // Function to fetch ticket details
    function fetchTicketDetails(ticketId, projectId) {
      // Make an AJAX request to retrieve the ticket details
      fetch(`/project_view/${projectId}/get_ticket_details/${ticketId}/`)
        .then((response) => response.json())
        .then((data) => {
          // Update the HTML of the details section with the retrieved data
          const detailsDiv = document.getElementById("ticket-details");
          // Modify the code below to populate the details section with the retrieved data
          detailsDiv.innerHTML = `
          <div class="row size1">
          <div class="col-sm-4">
            <div class="text-color6">Ticket Title</div>
            <div class="text-color5 pt-1">${data.title}</div>
          </div>
          <div class="col-sm-4">
            <div class="text-color6">Author</div>
            <div class="pt-1">${data.author}</div>
          </div>
          <div class="col-sm-4">
            <div class="text-color6">Description</div>
            <div class="pt-1">${data.description}</div>
          </div>
          <div class="row pt-3 pb-2">
            <div class="col-sm-3">
              <div class="ps-1 pb-2 text-color6">Status</div>
              <div><span class="badge rounded-pill badge-c">${
                data.status
              }</span></div>
            </div>
            <div class="col-sm-3">
              <div class="ps-5 pb-2 ms-1 text-color6">Priority</div>
              <div class="ps-5"><span class="badge rounded-pill badge-c">${
                data.priority
              }</span></div>
            </div>
            <div class="col-sm-3">
              <div class="ps-5 pb-2 ms-1 text-color6">Type</div>
              <div class="ps-5"><span class="badge rounded-pill badge-c">${
                data.ticket_type
              }</span></div>
            </div>
            <div class="col-sm-3">
              <div class="pb-2 mb-1 text-color6">Time(Hours)</div>
              <div>${data.estimated_time}</div>
            </div>
            <div class="border-bottom p-2"></div>
            <div class="ps-3 pb-2 pt-2 text-color6">Assigned Dev</div>
            <div class="ps-3">${data.assigned_devs.join(", ")}</div>
          </div>
        </div>
          `;

          // Update the comments section with the retrieved comments
          const commentsDiv = document.getElementById("ticket-comments");
          let commentsHTML = "";
          data.comments.forEach((comment) => {
            commentsHTML += `
             <div id="comment-${comment.id}">
              <div class="border-charts2 bg-light2 pt-1">
                <div class="d-flex">
                  <div class="h6 size1 ps-2 pt-2 pe-2">${comment.author.first_name} ${comment.author.last_name}</div>
                  <div class="size2 pt-1 align-item-center">${comment.created_at}</div>
                </div>
                <div class="d-flex justify-content-between">
                  <div class="size3 ps-2">${comment.content}</div>
                  <div class="dropdown">
                    <i class="material-icons more-vert-iconx" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false" >more_horiz</i>
                    <div class="dropdown-menu">
                      <a class="dropdown-item delete-comment-link" data-comment-id="${comment.id}">Delete Comment</a>
                    </div>
                  </div>
                </div>
              </div>
              </div>
            `;
          });
          commentsDiv.innerHTML = `
            <div class="pt-2 h6">Comments</div>
            <div class="input-group mb-3 pt-1">
              <input id="comment-input" type="text" class="form-control" placeholder="Enter comment">
              <button id="comment-button" class="btn btn-primary btn-sm dialog-custom-button" type="submit">Comment</button>
            </div>
            <div class="comments-container">
            ${commentsHTML}
            </div>
          `;
          // Add CSS to enable scrollbar for comments section
          const commentsContainer = commentsDiv.querySelector(
            ".comments-container"
          );
          commentsContainer.style.maxHeight = "100px"; // Adjust the height as needed
          commentsContainer.style.overflowY = "auto";
          // deleteting a comment
          const deleteCommentLinks = document.getElementsByClassName(
            "delete-comment-link"
          );
          Array.from(deleteCommentLinks).forEach((deleteCommentLink) => {
            deleteCommentLink.addEventListener("click", handleDeleteComment);
          });

          // Add event listener to the comment button
          const commentButton = document.getElementById("comment-button");
          commentButton.addEventListener("click", () => {
            const commentInput = document.getElementById("comment-input");
            const commentContent = commentInput.value.trim();
            if (commentContent !== "") {
              const commentData = new FormData();
              commentData.append("ticketId", ticketId);
              commentData.append("projectId", projectId);
              commentData.append("content", commentContent);

              // Make an AJAX request to save the comment
              fetch("/save_comment/", {
                method: "POST",
                headers: {
                  "X-CSRFToken": getCookie("csrftoken"),
                },
                body: commentData,
              })
                .then((response) => response.json())
                .then((savedComment) => {
                  // Append the new comment to the comments section
                  const authorFirstName = savedComment.author.first_name || "";
                  const authorLastName = savedComment.author.last_name || "";
                  const authorName = authorFirstName + " " + authorLastName;
                  // Append the new comment to the comments section
                  const newCommentHTML = `
                    <div class="border-charts2 bg-light2 pt-1">
                      <div class="d-flex">
                        <div class="h6 size1 ps-2 pt-2 pe-2">${authorName}</div>
                        <div class="size2 pt-1 align-item-center">${savedComment.created_at}</div>
                      </div>
                      <div class="d-flex justify-content-between">
                        <div class="size3 ps-2">${savedComment.content}</div>
                        <div class="dropdown">
                        <i class="material-icons more-vert-iconx" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false" >more_horiz</i>
                        <div class="dropdown-menu">
                          <a class="dropdown-item delete-comment-link" data-comment-id="${savedComment.id}">Delete Comment</a>
                        </div>
                      </div>
                      </div>
                    </div>
                  `;
                  commentsContainer.insertAdjacentHTML(
                    "afterbegin",
                    newCommentHTML
                  );

                  // Clear the comment input field
                  commentInput.value = "";
                })
                .catch((error) => {
                  console.log("Error:", error);
                });
            }
          });
        })
        .catch((error) => {
          console.log("Error:", error);
        });
    }

    fetchTicketDetails(ticketId, projectId);
  }

  // Event listener for deleting a comment
  function handleDeleteComment(event) {
    event.preventDefault();
    const commentId = event.currentTarget.dataset.commentId;

    // Make an AJAX request to delete the comment
    fetch("/delete_comment/" + commentId + "/", {
      method: "POST",
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
      },
    })
      .then((response) => {
        // Check if the deletion was successful
        if (response.ok) {
          // Remove the deleted comment from the comments section
          const commentElement = document.getElementById(
            "comment-" + commentId
          );
          if (commentElement) {
            commentElement.remove();
          }
        } else {
          console.log("Error:", response.status);
        }
      })
      .catch((error) => {
        console.log("Error:", error);
      });
  }

  // Attach the event listener to all ticket rows
  const ticketRows = document.getElementsByClassName("ticket-row");
  Array.from(ticketRows).forEach((ticketRow) => {
    ticketRow.addEventListener("click", handleTicketClick);
  });
});
