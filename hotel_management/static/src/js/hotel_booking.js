/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";

publicWidget.registry.HotelBookingForm = publicWidget.Widget.extend({
    selector: ".hotel-booking-form",
    events: {
        'change select[name="bed"]': '_onChangeFilter',
        'change input[name="facility_ids"]': '_onChangeFilter',
    },

    _onChangeFilter: function () {
        console.log("event");

        const bed = this.$el.find('select[name="bed"]').val();
        console.log("Selected bed:", bed);


//        const facilities = this.$el.find('select[name="facility_ids"]').val() || [];
        const facilities = [];
        this.$el.find('input[name="facility_ids"]:checked').each(function () {
            facilities.push($(this).val());
        });
        console.log("Selected facilities:", facilities);

        this._fetchRooms(bed, facilities);
    },

    async _fetchRooms(bed, facilities) {
    try {
        const rooms = await rpc("/hotel/get_rooms", {
            bed: bed,
            facility_ids: facilities,
        });

        console.log("Rooms response:", rooms);

        const $roomSelect = this.$el.find('.js-room-select');
        $roomSelect.empty();
        $roomSelect.append(`<option value="">Select Room</option>`);

        (rooms.rooms || rooms || []).forEach((room) => {
            $roomSelect.append(
                `<option value="${room.id}">${room.name}</option>`
            );
        });
    } catch (error) {
        console.error("Error fetching rooms:", error);
    }
}

});
