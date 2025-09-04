///** @odoo-module **/
//
//import publicWidget from "@web/legacy/js/public/public_widget";
//
//const FacilityPillsWidget = publicWidget.Widget.extend({
//    selector: '#facility-pills-container',
//    events: { 'click .remove-facility-btn': '_onRemoveFacilityClick' },
//
//    init() {
//        this._super(...arguments);
//        this.selectedFacilities = [];
//    },
//
//    start() {
//        this.facilityDropdown = this.el.closest('.s_website_form_field')
//            ?.querySelector('#facility_ids');
//        if (!this.facilityDropdown) return this._super(...arguments);
//
//        [...this.facilityDropdown.options].forEach(opt => {
//            if (opt.selected) {
//                this.selectedFacilities.push({ id: opt.value, name: opt.text.trim() });
//            }
//        });
//
//        this.facilityDropdown.addEventListener('click', e => this._onFacilityClick(e));
//        this._updateFacilities();
//
//        return this._super(...arguments);
//    },
//
//    _onFacilityClick(e) {
//        if (e.target.tagName !== 'OPTION') return;
//
//        const { value: id, textContent } = e.target;
//        const name = textContent.trim();
//        const exists = this.selectedFacilities.find(f => f.id === id);
//
//        this.selectedFacilities = exists
//            ? this.selectedFacilities.filter(f => f.id !== id)
//            : [...this.selectedFacilities, { id, name }];
//
//        e.target.selected = !exists;
//        this._updateFacilities();
//    },
//
//    _onRemoveFacilityClick(e) {
//        const id = e.currentTarget.dataset.facilityId;
//        this.selectedFacilities = this.selectedFacilities.filter(f => f.id !== id);
//
//        const opt = this.facilityDropdown?.querySelector(`option[value="${id}"]`);
//        if (opt) opt.selected = false;
//
//        this._updateFacilities();
//    },
//
//    _updateFacilities() {
//        this.el.innerHTML = '';
//        this.selectedFacilities.forEach(({ id, name }) => {
//            const pill = Object.assign(document.createElement('div'), {
//                className: 'facility-pill',
//                style: 'background:#e6f0ff;color:#000;padding:4px 8px;border-radius:16px;font-size:14px;margin:2px;display:inline-flex;align-items:center;',
//                textContent: name,
//            });
//
//            const btn = Object.assign(document.createElement('div'), {
//                className: 'remove-facility-btn',
//                dataset: { facilityId: id },
//                textContent: '×',
//                style: 'background:#000;color:#000;width:18px;height:18px;display:flex;align-items:center; justify-content:center;cursor:pointer;font-size:12px;font-weight:bold;margin-left:6px;border-radius:50%;'
//            });
//
//            pill.appendChild(btn);
//            this.el.appendChild(pill);
//        });
//    },
//});
//
//publicWidget.registry.FacilityPills = FacilityPillsWidget;
//export default FacilityPillsWidget;