/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";
import { loadJS } from "@web/core/assets";
publicWidget.registry.WebsiteCustomerContactRequestForm = publicWidget.Widget.extend({
   selector: ".s_website_form_required",
   init: function (parent, options) {
       this._super.apply(this, arguments);
      // Load Select2 dynamically (ensure it's included)
    loadJS("https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.13/js/select2.min.js").then(() => {
           const selects = document.querySelectorAll('.s_website_form_required select');
          $(".s_website_form_required select").select2();
       }).catch(err => console.error("Error loading Select2:", err));
   },
});