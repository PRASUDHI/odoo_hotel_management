/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Component, onWillStart, useState, onMounted } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";
import { loadJS } from "@web/core/assets";

class InventoryDashboard extends Component {
    setup() {
        const currentYear = new Date().getFullYear();

        this.state = useState({
            data: {},
            filterType: 'all',
            selectedWeek: '',
            selectedMonth: '',
//            selectedYear: currentYear.toString(),
            activeFilterDisplay: 'All Time',
        });
        this.charts = {};

        onWillStart(async () => {
            if (typeof Chart === "undefined") {
                await loadJS("https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js");
            }
            await this.fetchData();
        });

        onMounted(() => {
            this.renderCharts();
        });
    }

    async fetchData() {
        let filters = { period: this.state.filterType };
        if (this.state.filterType === 'week' && this.state.selectedWeek) {
            filters.value = this.state.selectedWeek;
        } else if (this.state.filterType === 'month' && this.state.selectedMonth) {
            filters.value = this.state.selectedMonth;
        }

        this.state.data = await rpc("/inventory/dashboard/data", { filters });

        if (this.charts.incomingChart) {
             this.renderCharts();
        }
    }

    onWeekChange(ev) {
        this.state.selectedWeek = ev.target.value;
        this.state.filterType = 'week';
        this.state.activeFilterDisplay = `Week: ${this.state.selectedWeek}`;
        this.fetchData();
    }

    onMonthChange(ev) {
        this.state.selectedMonth = ev.target.value;
        this.state.filterType = 'month';
        const date = new Date(this.state.selectedMonth + '-02');
        const monthName = date.toLocaleString('default', { month: 'long' });
        const year = date.getFullYear();
        this.state.activeFilterDisplay = `Month: ${monthName} ${year}`;
        this.fetchData();
    }



    async clearFilters() {
        this.state.filterType = 'all';
        this.state.selectedWeek = '';
        this.state.selectedMonth = '';
//        this.state.selectedYear = new Date().getFullYear().toString();
        this.state.activeFilterDisplay = 'All Time';
        await this.fetchData();
    }

    destroyCharts() {
        for (const chartKey in this.charts) {
            if (this.charts[chartKey]) {
                this.charts[chartKey].destroy();
            }
        }
        this.charts = {};
    }

    renderCharts() {
        this.destroyCharts();
        const data = this.state.data;

        if (data.incoming) {
            const ctx = document.getElementById("incomingChart");
            if (ctx) {
                this.charts.incomingChart = new Chart(ctx, {
                    type: "bar",
                    data: {
                        labels: data.incoming.map(i => i.product_id[1]),
                        datasets: [{
                            label: "Incoming Stock",
                            data: data.incoming.map(i => i.product_uom_qty),
                            backgroundColor: "rgba(54, 162, 235, 0.6)"
                        }]
                    },
                    options: { responsive: true, maintainAspectRatio: false }
                });
            }
        }

        if (data.outgoing) {
            const ctx = document.getElementById("outgoingChart");
            if (ctx) {
                this.charts.outgoingChart = new Chart(ctx, {
                    type: "bar",
                    data: {
                        labels: data.outgoing.map(i => i.product_id[1]),
                        datasets: [{
                            label: "Outgoing Stock",
                            data: data.outgoing.map(i => i.product_uom_qty),
                            backgroundColor: "rgba(255, 99, 132, 0.6)"
                        }]
                    },
                    options: { responsive: true, maintainAspectRatio: false }
                });
            }
        }

        if (data.location_stock) {
            const ctx = document.getElementById('locationChart');
            if (ctx) {
                this.charts.locationChart = new Chart(ctx, {
                    type: 'pie',
                    data: {
                        labels: data.location_stock.map(l => l.location_id[1]),
                        datasets: [{
                            data: data.location_stock.map(l => l.quantity),
                            backgroundColor: ['#36A2EB', '#FF6384', '#FFCE56', '#4BC0C0', '#9966FF'],
                        }]
                    },
                    options: { responsive: true, maintainAspectRatio: false }
                });
            }
        }

        if (data.picking_types) {
            const ctx = document.getElementById('pickingTypeChart');
            if (ctx) {
                this.charts.pickingTypeChart = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: data.picking_types.map(p => p.picking_type_id[1]),
                        datasets: [{
                            label: 'Pickings',
                            data: data.picking_types.map(p => p.picking_type_id_count || 0),
                            backgroundColor: 'rgba(153, 102, 255, 0.6)',
                        }]
                    },
                    options: { responsive: true, maintainAspectRatio: false }
                });
            }
        }

        if (data.internal) {
            const ctx = document.getElementById('internalTransferChart');
            if (ctx) {
                this.charts.internalTransferChart = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: data.internal.map(i => i.product_id[1]),
                        datasets: [{
                            label: 'Internal Transfers',
                            data: data.internal.map(i => i.product_uom_qty),
                            backgroundColor: 'rgba(255, 159, 64, 0.6)',
                        }]
                    },
                    options: { responsive: true, maintainAspectRatio: false }
                });
            }
        }

        if (data.warehouses) {
            const ctx = document.getElementById('warehouseChart');
            if (ctx) {
                const warehouseCounts = {};
                (data.location_stock || []).forEach(loc => {
                    const whName = loc.location_id[1].split('/')[0];
                    warehouseCounts[whName] = (warehouseCounts[whName] || 0) + loc.quantity;
                });
                const labels = Object.keys(warehouseCounts);
                const values = Object.values(warehouseCounts);

                this.charts.warehouseChart = new Chart(ctx, {
                    type: 'pie',
                    data: {
                        labels: labels,
                        datasets: [{
                            data: values,
                            backgroundColor: ['#4BC0C0', '#9966FF', '#FFCE56', '#36A2EB', '#FF6384'],
                        }]
                    },
                    options: { responsive: true, maintainAspectRatio: false }
                });
            }
        }

        if (data.inventory_valuation) {
            const ctxValuation = document.getElementById('valuationChart');
             if(ctxValuation) {
                this.charts.valuationChart = new Chart(ctxValuation, {
                    type: 'doughnut',
                    data: {
                        labels: data.inventory_valuation.map(v => v.warehouse),
                        datasets: [{
                            label: 'Inventory Value',
                            data: data.inventory_valuation.map(v => v.value),
                            backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0'],
                            borderWidth: 1
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: { legend: { position: 'bottom' } }
                    }
                });
             }
        }

        if (data.average_expense) {
            const ctx = document.getElementById('averageExpenseChart');
            if (ctx) {
                this.charts.averageExpenseChart = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: data.average_expense.map(p => p.product),
                        datasets: [{
                            label: 'Average Expense',
                            data: data.average_expense.map(p => p.average_expense),
                            backgroundColor: 'rgba(52, 152, 219, 0.6)',
                        }]
                    },
                    options: { responsive: true, maintainAspectRatio: false }
                });
            }
        }
    }
}

InventoryDashboard.template = "inventory_dashboard.InventoryDashboard";
registry.category("actions").add("inventory_dashboard_tag", InventoryDashboard);