/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";
import { renderToElement } from "@web/core/utils/render";

function chunk(array, size) {
    const result = [];
    if (!array || !array.length) {
        return result;
    }
    for (let i = 0; i < array.length; i += size) {
        result.push(array.slice(i, i + size));
    }
    return result;
}

publicWidget.registry.HotelGallerySnippet = publicWidget.Widget.extend({
    selector: ".hotel-gallery-snippet",

    async willStart() {
        const data = await rpc('/get_hotel_gallery', {});
        console.log("Gallery Data:", data);
        this.images = data.gallery || [];
    },

    async start() {
        const refEl = this.$el.find("#hotelGalleryCarouselWrapper");
        const chunkData = chunk(this.images, 5);
        refEl.html(renderToElement("hotel_management.hotel_gallery_snippet_template", {
            chunkData,
        }));
    },
});

export default publicWidget.registry.HotelGallerySnippet;
