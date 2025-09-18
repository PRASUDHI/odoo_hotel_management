/** @odoo-module **/
import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";
import { Orderline } from "@point_of_sale/app/generic_components/orderline/orderline";
import { patch } from "@web/core/utils/patch";
patch(PosOrderline.prototype, {
    setup(vals) {
        console.log('this :',this)
        return super.setup(...arguments);
    },
    getDisplayData() {
        console.log(this)
        return {
            ...super.getDisplayData(),
            brand_name: this.product_id.brand_name || "",
        };
    },
});
