class ContactForm {

  constructor() {
  }

  validate() {

    if (jQuery("#firstName").val() === "") {
      alert("First Name is required field!");
      jQuery("#firstName").focus();
      return false;  
    }

    if (jQuery("#lastName").val() === "") {
      alert("Last Name is required field!");
      jQuery("#lastName").focus();
      return false;  
    }

    if (jQuery("#eMail").val() === "") {
      alert("Email is required field!");
      jQuery("#eMail").focus();
      return false;  
    }

    if (/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(jQuery("#eMail").val()) === false) {
      alert("Email is not in valid format!");
      jQuery("#eMail").focus();
      return false;  
    }
    
    if (jQuery("#subject").val() === "") {
      alert("Subject is required field!");
      jQuery("#subject").focus();
      return false;  
    }

    if (jQuery("#message").val() === "") {
      alert("Message is required field!");
      jQuery("#message").focus();
      return false;  
    }

    return true;
  }
}

var contactForm = new ContactForm();

jQuery(document).ready(function() {
  // Code to run when the DOM is ready
  jQuery("#btnSendMessage").click(function() {
    if (contactForm.validate() === true) {
      const post_fields = {
        first_name: jQuery('#firstName').val(),
        last_name: jQuery('#lastName').val(),
        email: jQuery('#eMail').val(),
        subject: jQuery('#subject').val(),
        message: jQuery('#message').val()
      };

      console.dir(post_fields);

      jQuery.ajax({
        url: '/contact-us/',
        method: 'POST',
        // contentType: 'application/json',
        data: post_fields/*JSON.stringify(data)*/,
        success: function (res) {
          if (res.redirect) {
            window.open(res.redirect, "_blank", "noopener,noreferrer");
          };

          if (res.thank_you_url) {
            document.location.href = res.thank_you_url;
          };
        }
        //success: res => console.log(res)
      });

    }
  });
});