///** @odoo-module **/
//import publicWidget from "@web/legacy/js/public/public_widget";
//import { rpc } from "@web/core/network/rpc";
//
//publicWidget.registry.HotelAccommodationForm = publicWidget.Widget.extend({
//    selector: "#wrap",
//    events: {
//        'click .add_guest_line': '_onAddGuest',
//        'click .remove_line': '_onRemoveGuest',
//        'click .submit_accommodation': '_onSubmitAccommodation',
//    },
//
//    _onAddGuest: function () {
//        var $new_row = $('#guest_table tbody tr.guest_line:first').clone();
//        $new_row.find('input, select').val('');
//        $new_row.appendTo('#guest_table tbody');
//    },
//
//    _onRemoveGuest: function (ev) {
//        if ($('#guest_table tbody tr').length > 1) {
//            $(ev.target).closest('tr').remove();
//        } else {
//            alert("At least one guest is required!");
//        }
//    },
//
//    _onSubmitAccommodation: async function (ev) {
//        ev.preventDefault();
//        var guest_id = $('#guest_id').val();
//        var guest_lines = [];
//
//        $('#guest_table tbody tr.guest_line').each(function () {
//            guest_lines.push({
//                'name': $(this).find('input[name="name"]').val(),
//                'age': $(this).find('input[name="age"]').val(),
//                'gender': $(this).find('select[name="gender"]').val(),
//            });
//        });
//
//        try {
//            let response = await rpc('/hotel/accommodation/submit', {
//                guest_id: guest_id,
//                accommodation_ids: guest_lines,
//            });
//            alert('Accommodation created successfully!');
//        } catch (error) {
//            console.error(error);
//            alert('Error creating accommodation.');
//        }
//    },
//});