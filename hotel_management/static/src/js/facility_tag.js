///** @odoo-module **/
//import publicWidget from "@web/legacy/js/public/public_widget";
//const TagPillsWidget = publicWidget.Widget.extend({
//   selector: '#tag-pills-container',
//   events: { 'click .remove-tag-btn': '_onRemoveTagClick' },
//   init(parent, options) {
//       this._super(...arguments);
//       this.selectedTags = [];
//   },
//   start() {
//       this.tagDropdown = this.el.querySelector('#contact_tag');
//       if (!this.tagDropdown) return this._super(...arguments);
//       [...this.tagDropdown.options].forEach(opt => {
//           if (opt.selected) this.selectedTags.push({ id: opt.value, name: opt.text.trim() });
//       });
//       this.tagDropdown.addEventListener('click', e => this._onTagClick(e));
//       this._updateTags();
//       return this._super(...arguments);
//   },
//   _onTagClick(e) {
//       if (e.target.tagName !== 'OPTION') return;
//       const { value: id, textContent } = e.target;
//       const name = textContent.trim();
//       const exists = this.selectedTags.find(t => t.id === id);
//       this.selectedTags = exists
//           ? this.selectedTags.filter(t => t.id !== id)
//           : [...this.selectedTags, { id, name }];
//       e.target.selected = !exists;
//       this._updateTags();
//   },
//   _onRemoveTagClick(e) {
//       const id = e.currentTarget.dataset.tagId;
//       this.selectedTags = this.selectedTags.filter(t => t.id !== id);
//       const opt = this.tagDropdown?.querySelector(`option[value="${id}"]`);
//       if (opt) opt.selected = false;
//       this._updateTags();
//   },
//   _updateTags() {
//       this.el.innerHTML = '';
//       this.selectedTags.forEach(({ id, name }) => {
//           const pill = Object.assign(document.createElement('div'), {
//               className: 'tag-pill',
//               style: 'background:#e6f0ff;color:#000;padding:4px 8px;border-radius:16px;font-size:14px;margin:2px;display:inline-flex;align-items:center;',
//               textContent: name,
//           });
//           const btn = Object.assign(document.createElement('div'), {
//               className: 'remove-tag-btn',
//               dataset: { tagId: id },
//               textContent: '×',
//               style: 'background:#6c757d;color:#fff;width:18px;height:18px;display:flex;align-items:center; justify-content:center;cursor:pointer;font-size:12px;font-weight:bold;margin-left:6px;border-radius:50%;'
//           });
//           pill.appendChild(btn);
//           this.el.appendChild(pill);
//       });
//   },
//});
//publicWidget.registry.TagPills = TagPillsWidget;
//export default TagPillsWidget;