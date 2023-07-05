$(document).ready(function () {
    $('.more-vert-icon').popover({
      content: function () {
        return $('#popover-content').html();
      },
      html: true,
      placement: 'bottom',
    });
  });
  
  // Open the modal when clicking on the edit link
  $(document).on('click', '.edit-link', function () {
    $('#myModal2').modal('show');
  });
  

  // Dismiss popover on document click
  $(document).on('click', function (e) {
    $('.more-vert-icon').each(function () {
      // Check if the clicked element is inside the popover or the popover trigger itself
      var popoverElement = $(this);
      if (
        !popoverElement.is(e.target) &&
        popoverElement.has(e.target).length === 0 &&
        $('.popover').has(e.target).length === 0
      ) {
        popoverElement.popover('hide');
      }
    });
  });


// editing the comments
$(document).ready(function () {
  $('.more-vert-icon2').popover({
    content: function () {
      return $('#popover-content2').html();
    },
    html: true,
    placement: 'bottom',
  });
});

  // Dismiss popover on document click
  $(document).on('click', function (e) {
    $('.more-vert-icon2').each(function () {
      // Check if the clicked element is inside the popover or the popover trigger itself
      var popoverElement = $(this);
      if (
        !popoverElement.is(e.target) &&
        popoverElement.has(e.target).length === 0 &&
        $('.popover').has(e.target).length === 0
      ) {
        popoverElement.popover('hide');
      }
    });
  });

  // removing dev from the team
  $(document).ready(function () {
    $('.more-vert-icon3').popover({
      content: function () {
        return $('#popover-content3').html();
      },
      html: true,
      placement: 'bottom',
    });
  });
  
    // Dismiss popover on document click
    $(document).on('click', function (e) {
      $('.more-vert-icon3').each(function () {
        // Check if the clicked element is inside the popover or the popover trigger itself
        var popoverElement = $(this);
        if (
          !popoverElement.is(e.target) &&
          popoverElement.has(e.target).length === 0 &&
          $('.popover').has(e.target).length === 0
        ) {
          popoverElement.popover('hide');
        }
      });
    });