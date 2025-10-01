/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Component, onWillStart, onMounted, useState } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";

class InventoryDashboard extends Component {
    static props = {}; // Required in Owl

    setup() {
        this.state = useState({
            data: {},
            filters: { year: new Date().getFullYear(), month: null, week: null },
        });

        onWillStart(async () => {
            await this.loadData();
        });

        onMounted(() => {
            this.renderCharts();
        });
    }

    async loadData() {
        this.state.data = await rpc("/inventory/dashboard/data", { filters: this.state.filters });
    }

    async onFilterChange(ev) {
        const name = ev.target.name;
        const value = ev.target.value;
        this.state.filters[name] = value || null;
        await this.loadData();
        this.renderCharts();
    }

    renderCharts() {
        const data = this.state.data;

        const createBarChart = (id, labels, values, label, color) => {
            const ctx = document.getElementById(id);
            if (!ctx) return;
            new Chart(ctx.getContext("2d"), {
                type: "bar",
                data: { labels, datasets: [{ label, data: values, backgroundColor: color }] },
                options: { responsive: true, maintainAspectRatio: false },
            });
        };

        const createPieChart = (id, labels, values, colors) => {
            const ctx = document.getElementById(id);
            if (!ctx) return;
            new Chart(ctx.getContext("2d"), {
                type: "pie",
                data: { labels, datasets: [{ data: values, backgroundColor: colors }] },
                options: { responsive: true, maintainAspectRatio: false },
            });
        };

        if (data.incoming?.length)
            createBarChart("incomingChart", data.incoming.map(i => i.product_id[1]), data.incoming.map(i => i.product_uom_qty), "Incoming Stock", "rgb(54, 162, 235)");

        if (data.outgoing?.length)
            createBarChart("outgoingChart", data.outgoing.map(i => i.product_id[1]), data.outgoing.map(i => i.product_uom_qty), "Outgoing Stock", "rgb(255, 99, 132)");

        if (data.internal?.length)
            createBarChart("internalTransferChart", data.internal.map(i => i.product_id[1]), data.internal.map(i => i.product_uom_qty), "Internal Transfers", "rgb(255, 159, 64)");

        if (data.location_stock?.length)
            createPieChart("locationChart", data.location_stock.map(l => l.location_id[1]), data.location_stock.map(l => l.quantity), ["rgb(54, 162, 235)", "rgb(255, 99, 132)", "rgb(255, 206, 86)", "rgb(75, 192, 192)", "rgb(153, 102, 255)"]);

        if (data.picking_types?.length)
            createBarChart("pickingTypeChart", data.picking_types.map(p => p.picking_type_id[1]), data.picking_types.map(p => p.picking_type_id[0] ? p['picking_type_id_count'] || 0 : 0), "Pickings", "rgb(153, 102, 255)");

        if (data.warehouses?.length)
            createPieChart("warehouseChart", data.warehouses.map(w => w.name), data.warehouses.map(() => 1), ["rgb(75, 192, 192)", "rgb(153, 102, 255)", "rgb(255, 206, 86)", "rgb(54, 162, 235)", "rgb(255, 99, 132)"]);

        // Doughnut chart for Inventory Valuation
        const valuationCtx = document.getElementById("valuationChart");
        if (valuationCtx) {
            new Chart(valuationCtx.getContext("2d"), {
                type: "doughnut",
                data: {
                    labels: data.inventory_valuation.map(v => v.warehouse),
                    datasets: [{ label: "Inventory Value", data: data.inventory_valuation.map(v => v.value), backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0"], borderWidth: 1 }]
                },
                options: { responsive: true, plugins: { legend: { position: "bottom" } } }
            });
        }

        // Bar chart for Average Expense
        if (data.average_expense?.length) {
            const avgCtx = document.getElementById("averageExpenseChart");
            if (avgCtx) {
                new Chart(avgCtx.getContext("2d"), {
                    type: "bar",
                    data: {
                        labels: data.average_expense.map(p => p.product),
                        datasets: [{ label: "Average Expense", data: data.average_expense.map(p => p.average_expense), backgroundColor: "rgb(52, 152, 219)" }]
                    },
                    options: { responsive: true, maintainAspectRatio: false }
                });
            }
        }
    }
}

InventoryDashboard.template = "inventory_dashboard.InventoryDashboard";
registry.category("actions").add("inventory_dashboard_tag", InventoryDashboard);
