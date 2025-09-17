/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";

publicWidget.registry.FoodOrderCart = publicWidget.Widget.extend({
    selector: ".food-order-page",

    events: {
    "click .btn-add-to-list": "_onAddToList",
    "click .btn-confirm-order": "_onConfirmOrder",
    "click .btn-remove-item": "_onRemoveItem",
},

    _onRemoveItem: async function (ev) {
        ev.preventDefault();
        const lineId = $(ev.currentTarget).data("line-id");

        const result = await rpc("/food/remove_from_cart", { line_id: lineId });
        if (result.success) {
            this._renderCart(result.cart);
        } else {
            alert(result.error || "Failed to remove item");
        }
    },

    start: function () {
        this._super(...arguments);
        const cartData = this.$el.data("cart") || [];
        this._renderCart(cartData);
    },

    _onAddToList: async function (ev) {
        ev.preventDefault();
        const $btn = $(ev.currentTarget);
        const foodId = $btn.data("food-id");
        const qty = $btn.closest(".modal").find("input[name='quantity']").val() || 1;

        const result = await rpc("/food/add_to_cart", { food_id: foodId, quantity: parseInt(qty) });
        if (result.success) {
            this._renderCart(result.cart);
        }
    },

    _onConfirmOrder: async function () {
        const result = await rpc("/food/confirm_order", {});
        if (result.success) {
            alert("Order placed successfully! Order ID: " + result.order_id);
            this.$el.find(".btn-confirm-order").hide();
        } else {
            alert(result.error || "Something went wrong");
        }
    },

    _renderCart: function (cart) {
        const $cart = this.$el.find(".cart-items");
        const $confirmBtn = this.$el.find(".btn-confirm-order");
        $cart.empty();

        let total = 0;

        if (!cart || cart.length === 0) {
            $confirmBtn.hide();
            $cart.append(`
                <li class="list-group-item text-center text-muted">
                    No items in your order
                </li>
            `);
            return;
        }

        $confirmBtn.show();
        $cart.append(`
            <li class="list-group-item bg-primary text-white d-flex justify-content-between">
                <div style="width:40%">Item</div>
                <div style="width:30%; text-align:center">Price × Qty</div>
                <div style="width:30%; text-align:right">Subtotal</div>
            </li>
        `);

        cart.forEach(item => {
            total += item.subtotal;
            $cart.append(`
                <li class="list-group-item d-flex justify-content-between align-items-center">
                    <div style="width:40%">${item.name}</div>
                    <div style="width:30%; text-align:center">
                        $${item.price.toFixed(2)} × ${item.quantity}
                    </div>
                    <div style="width:20%; text-align:right" class="fw-bold text-success">
                        $${item.subtotal.toFixed(2)}
                    </div>
                    <div style="width:10%; text-align:right">
                        <button class="btn btn-sm btn-danger btn-remove-item"
                                data-line-id="${item.food_id}">
                            ✖
                        </button>
                    </div>
                </li>
            `);
        });

        $cart.append(`
            <li class="list-group-item bg-light d-flex justify-content-between align-items-center">
                <strong style="width:40%">Total</strong>
                <div style="width:30%"></div>
                <strong style="width:30%; text-align:right" class="text-primary">
                    $${total.toFixed(2)}
                </strong>
            </li>
        `);
    },
});