/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";

publicWidget.registry.HotelGuestForm = publicWidget.Widget.extend({
    selector: ".hotel-booking-form",
    events: {
        'click .add_guest': '_onClickAddGuest',
        'click .remove_guest': '_onClickRemoveGuest',
        'submit form.o_wbooth_registration_form': '_onSubmitForm',
    },

    _onClickAddGuest: function () {
        let $row = this.$el.find("tr.guest_line:first").clone();
        $row.find("input, select").val("");
        this.$el.find("#guest_table tbody").append($row);
    },

    _onClickRemoveGuest: function (ev) {
        if (this.$el.find("#guest_table tbody tr").length > 1) {
            $(ev.currentTarget).closest("tr").remove();
        }
    },
    _onSubmitForm: function (ev) {
        let guestLines = [];
        this.$el.find("#guest_table tbody tr").each(function () {
            guestLines.push({
                guest_id: $(this).find("select[name='guest_id']").val(),
                age: $(this).find("input[name='guest_age']").val(),
                gender: $(this).find("select[name='guest_gender']").val(),
            });
        });


        $('<input>').attr({type: 'hidden',name: 'guest_lines',value: JSON.stringify(guestLines)}).appendTo(ev.currentTarget);
    }
});
