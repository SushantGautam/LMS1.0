// Show Hide Edit Basic Info Card
// $(".edit-basic-card").hide();
// $("#edit-basic-info").click(function () {
//   $(".edit-basic-card").show();
//   $(".view-basic-card").hide();
// });
// $("#view-basic-info").click(function () {
//   $(".view-basic-card").show();
//   $(".edit-basic-card").hide();
// });
// $("#reset-basic-info").click(function (e) {
//   e.preventDefault();
//   $(".view-basic-card").show();
//   $(".edit-basic-card").hide();
// });

// // Show Hide Edit Contact Info Card
// $(".edit-contact-card").hide();
// $("#edit-contact-info").click(function () {
//   $(".edit-contact-card").show();
//   $(".view-contact-card").hide();
// });
// $("#view-contact-info").click(function () {
//   $(".view-contact-card").show();
//   $(".edit-contact-card").hide();
// });
// $("#reset-contact-info").click(function (e) {
//   e.preventDefault();
//   $(".view-contact-card").show();
//   $(".edit-contact-card").hide();
// });

// // Show Hide Edit Description Info Card
// $(".edit-description-card").hide();
// $("#edit-description-info").click(function () {
//   $(".edit-description-card").show();
//   $(".view-description-card").hide();
// });
// $("#view-description-info").click(function () {
//   $(".view-description-card").show();
//   $(".edit-description-card").hide();
// });
// $("#reset-description-info").click(function (e) {
//   e.preventDefault();
//   $(".view-description-card").show();
//   $(".edit-description-card").hide();
// });

// Submit data of basic card info
$(".edit-basic-card").submit(function (e) {
  e.preventDefault(); // avoid to execute the actual submit of the form.
  $.ajax({
    url: "/editprofile/basicinfo",
    type: "POST",
    data: {
      csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
      username: $("#id_username").val(),
      first_name: $("#id_first_name").val(),
      last_name: $("#id_last_name").val(),
      Member_BirthDate: $("#id_Member_BirthDate").val(),
      Member_Gender: $("input[name='gender']:checked").val(),
    },

    success: function (response) {
      console.log("Success");
      location.reload();
    },
    error: function () {
      console.log("Error in updating the user data");
    },
  });
});

// Submit data of contact card info
$(".edit-contact-card").submit(function (e) {
  e.preventDefault(); // avoid to execute the actual submit of the form.
  $.ajax({
    url: "/editprofile/contactinfo",
    type: "POST",
    data: {
      csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
      email: $("#id_email").val(),
      Member_Phone: $("#id_Member_Phone").val(),
      Member_Temporary_Address: $("#id_Member_Temporary_Address").val(),
      Member_Permanent_Address: $("#id_Member_Permanent_Address").val(),
    },

    success: function (response) {
      console.log("Success");
      location.reload();
    },
    error: function () {
      console.log("Error in posting assignment create form");
    },
  });
});

// Submit data of contact card info
$(".edit-description-card").submit(function (e) {
  e.preventDefault(); // avoid to execute the actual submit of the form.
  $.ajax({
    url: "/editprofile/descriptioninfo",
    type: "POST",
    data: {
      csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
      Member_Memo: $("#id_Member_Memo").val(),
    },

    success: function (response) {
      console.log("Success");
      location.reload();
    },
    error: function () {
      console.log("Error in posting assignment create form");
    },
  });
});

// upload image
$("#id_Member_Avatar").on("change", function () {
  formdata = new FormData();
  var file = this.files[0];
  if (formdata) {
    if (file.size > 2097152) {
      alert(
        "Image size is greater than 2 Mb. Please upload image of smaller size"
      );
    } else {
      formdata.append("Member_Avatar", file);
      formdata.append(
        "csrfmiddlewaretoken",
        $('input[name="csrfmiddlewaretoken"]').val()
      );
      jQuery.ajax({
        url: "/editprofile/upload_image",
        type: "POST",
        data: formdata,
        processData: false,
        contentType: false,
        success: function (response) {
          console.log(response.msg);
          location.reload();
        },
      });
    }
  }
});
