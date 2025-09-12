/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";
import { renderToElement } from "@web/core/utils/render";

function chunk(array, size) {
    const result = [];
    for (let i = 0; i < array.length; i += size) {
        result.push(array.slice(i, i + size));
    }
    return result;
}

var HotelGallerySnippet = publicWidget.Widget.extend({
    selector: ".hotel-gallery-snippet",

    willStart: async function () {
        const data = await rpc("/hotel_gallery_data", {});
        const { images, unique_id } = data;
        Object.assign(this, { images, unique_id, chunkData: chunk(images, 5) });
    },

    start: function () {
        const $container = this.$el;
        $container.html(renderToElement("hotel_management.hotel_gallery_carousel", {
            images: this.images,
            unique_id: this.unique_id,
            chunkData: this.chunkData
        }));
        return this._super.apply(this, arguments);
    }
});

publicWidget.registry.HotelGallerySnippet = HotelGallerySnippet;
export default HotelGallerySnippet;
