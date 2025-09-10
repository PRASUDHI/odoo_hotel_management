/** @odoo-module */
import { renderToElement } from "@web/core/utils/render";
import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";

publicWidget.registry.HotelGallerySnippet = publicWidget.Widget.extend({
    selector: ".hotel-gallery-section",
    async willStart() {
        const result = await rpc('/get_hotel_gallery', {});
        if (result) {
            this.$target.empty().html(
                renderToElement('hotel_management.hotel_gallery_template', { result })
            );
        }
    },
});