/** @odoo-module **/
import { Orderline } from "@point_of_sale/app/generic_components/orderline/orderline";
import { patch } from "@web/core/utils/patch";


Orderline.props = {
    ...Orderline.props,
    line: {
        ...Orderline.props.line,
        shape: {
            ...Orderline.props.line.shape,
            brand_name: { type: String, optional: true },
        },
    },
};
