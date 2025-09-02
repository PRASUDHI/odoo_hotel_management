///** @odoo-module **/
//import publicWidget from "@web/legacy/js/public/public_widget";
//import ajax from 'web.ajax';
//
//publicWidget.registry.HotelBookingForm = publicWidget.Widget.extend({
//    selector: '.hotel-booking-form',
//    events: {
//        'change select[name="bed"]': '_updateRooms',
//        'change input[name="facility_ids"]': '_updateRooms',
////    },
//
//    _updateRooms: function () {
//        const bed = this.$el.find('select[name="bed"]').val();
//        const facility_ids = [];
//        console.log("dfghjk",events)
//        });
//
//        ajax.jsonRpc('/hotel/get_rooms', 'call', {
//            bed: bed,
//            facility_ids: facility_ids,
//        }).then(rooms => {
//            const $roomSelect = this.$el.find('select[name="room_id"]');
//            $roomSelect.empty().append('<option value="">-- Select Room --</option>');
//            rooms.forEach(room => {
//                $roomSelect.append(`<option value="${room.id}">${room.name}</option>`);
//            });
//        });
//    },
//});