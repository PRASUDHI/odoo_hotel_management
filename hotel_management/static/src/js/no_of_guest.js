/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";

publicWidget.registry.HotelGuestForm = publicWidget.Widget.extend({
    selector: ".hotel-booking-form",
    events: {
        'click .add_guest': '_onClickAddGuest',
        'click .remove_guest': '_onClickRemoveGuest',
        'submit form.o_wbooth_registration_form': '_onSubmitForm',
        'change input[name="guests"]': '_onChangeGuests',
    },

    start: function () {
        this._super.apply(this, arguments);
        this._toggleGuestTable();
        this._updateAddGuestButton();
    },

    _onChangeGuests: function () {
        this._toggleGuestTable();
        this._updateAddGuestButton();
    },

    _toggleGuestTable: function () {
        let guests = parseInt(this.$el.find("input[name='guests']").val() || 1);
        if (guests <= 1) {
            this.$el.find("#guest_table").closest(".mb-3").hide();
        } else {
            this.$el.find("#guest_table").closest(".mb-3").show();
        }
    },

    _updateAddGuestButton: function () {
        let maxGuests = parseInt(this.$el.find("input[name='guests']").val() || 1);
        let currentGuests = this.$el.find("#guest_table tbody tr").length;

        if (currentGuests >= maxGuests) {
            this.$el.find(".add_guest").hide();
        } else {
            this.$el.find(".add_guest").show();
        }
    },

    _onClickAddGuest: function () {
        let $row = this.$el.find("tr.guest_line:first").clone();
        $row.find("input, select").val("");
        this.$el.find("#guest_table tbody").append($row);

        this._updateAddGuestButton();
    },

    _onClickRemoveGuest: function (ev) {
        if (this.$el.find("#guest_table tbody tr").length > 1) {
            $(ev.currentTarget).closest("tr").remove();
        }
        this._updateAddGuestButton();
    },

    _onSubmitForm: function (ev) {
        let guestLines = [];
        this.$el.find("#guest_table tbody tr").each(function () {
            let guest_id = $(this).find("select[name='guest_id']").val();
            if (guest_id) {
                guestLines.push({
                    guest_id: guest_id,
                    age: $(this).find("input[name='guest_age']").val(),
                    gender: $(this).find("select[name='guest_gender']").val(),
                });
            }
        });

        if (guestLines.length) {
            $('<input>').attr({
                type: 'hidden',
                name: 'guest_lines',
                value: JSON.stringify(guestLines)
            }).appendTo(ev.currentTarget);
        }
    }
});
