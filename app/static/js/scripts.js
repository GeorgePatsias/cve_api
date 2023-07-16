$(document).ready(function () {

  // Toggle the side navigation
  const sidebarToggle = document.body.querySelector('#sidebarToggle');
  if (sidebarToggle) {
    // Uncomment Below to persist sidebar toggle between refreshes
    // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
    //     document.body.classList.toggle('sb-sidenav-toggled');
    // }
    sidebarToggle.addEventListener('click', event => {
      event.preventDefault();
      document.body.classList.toggle('sb-sidenav-toggled');
      localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
    });
  }

  // Notifications
  $.ajax({
    url: "/notifications",
    success: function (notif_data) {
      const notifications = JSON.parse(notif_data);
      console.log(notifications);

      if (!notifications || notifications.count == "0") {
        $("#notifications").hide();
        $('#notificationItems').remove();
        return;
      };

      if (notifications.count.length == 3) {
        $("#notifications").text("99+");
        return;
      } else {
        $("#notifications").text(notifications.count);
      };

      notifications_html = `
        <div class="row">
          <div class="col-xl-12 text-center">
            <a class="notifications" href="/notifications/delete">
             Clear All <i class="fa-solid fa-trash fa-lg me-1"></i>
            </a>
          </div>
        </div>
        <hr class="dropdown-divider" />
      `;
      // Limit to 5 notifications only
      notifications.data.slice(-5).forEach((notification_item) => {
        notifications_html = notifications_html + `
        <li>
        <a class="notifications" href="/investigate/${notification_item.cve}">
          <div class="container">
            <div class="row">
              <div class="col-xl-12 text-nowrap">
                <i class="fa-solid fa-bug"></i>
                ${notification_item.cve}
              </div>
            </div>
            <div class="row">
              <div class="col-xl-12">
              <i class="fa-solid fa-magnifying-glass"></i>
                ${notification_item.keyword}
              </div>
            </div>
          </div>
          </a>
        </li>
        <hr class="dropdown-divider" />
        `;
      });


      notifications_html = notifications_html + `
      <div class="row">
      <div class="col-xl-12 text-center">
      <a class="notifications" href="/events">Show All <i class="fa-solid fa-arrow-up-right-from-square me-1"></i></a>
      </div>
    </div>
      `;

      $("#notificationItems").append(notifications_html);
    }
  });


  $("#error_msg").fadeTo(5000, 1).fadeOut(1000);

  $("#resetPass").click(function () {

    if ($("#resetPassModal").length != 0) {
      $("#resetPassModal").modal('show');
    } else {
      html = `
            <div id="resetPassModal" class="modal" tabindex="-1" role="dialog">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Reset Password</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <form action="/reset-password" method="POST">
                        <div class="modal-body">
                    
                            <input class="form-control rounded-pill" id="inputResetUsername" type="hidden" name="username"
                                placeholder="Username" value="" required />
                                
                            <div class="form-floating mb-3">
                                <input class="form-control rounded-pill" id="inputResetCurrentPassword" type="password" name="current-password"
                                    placeholder="Enter current password" value="" autocomplete="off" required />
                                <label for="inputResetCurrentPassword">
                                    <h6><i class="fa-solid fa-lock"></i> Current Password</h6>
                                </label>
                            </div>
                            <div class="form-floating mb-3">
                                <input class="form-control rounded-pill" id="inputResetPassword" type="password" name="new-password"
                                    placeholder="Enter new password" value="" autocomplete="off" required />
                                <label for="inputResetPassword">
                                    <h6><i class="fa-solid fa-user"></i> Enter new password</h6>
                                </label>
                            </div>
        
                            <div class="form-floating mb-3">
                                <input class="form-control rounded-pill" id="inputConfirmPassword" type="password" name="confirm-password"
                                    placeholder="Confirm Password" value="" autocomplete="off" required />
                                <label for="inputConfirmPassword">
                                    <h6><i class="fa-solid fa-key"></i> Confirm new password</h6>
                                </label>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                            <button type="submit" class="btn btn-success">Change Password</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>                
    `;
      $("body").append(html);

      $('#inputResetUsername').val($('#current-user-id').text());

      $("#resetPassModal").modal('show');
    }
  });







});