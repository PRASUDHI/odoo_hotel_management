import { patch } from "@web/core/utils/patch";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { _t } from "@web/core/l10n/translation";
import { PosOrder } from "@point_of_sale/app/models/pos_order";


patch(PaymentScreen.prototype, {
    async validateOrder(isForceValidate) {
        const total_order = this.currentOrder;


        console.log("order", total_order);

        if (!total_order.partner_id) {
            this.dialog.add(AlertDialog, {
                title: _t("Select Customer"),
                body: _t("Please Select a Customer"),
            });
            return;
        }
        const due_limit = total_order.get_partner().due_limit;
        const total_amount = total_order.get_total_with_tax();

        console.log("due_limit",due_limit)
        console.log("total_amount",total_amount)

        if (due_limit > 0) {
            if (total_amount > due_limit) {
                this.dialog.add(AlertDialog, {
                    title: _t("Limit Exceeds"),
                    body: _t("Your purchase limit is : " + due_limit),
                });
                return;
            }
        }
        console.log("fwfffvss")
        return await super.validateOrder(...arguments);
    },
});