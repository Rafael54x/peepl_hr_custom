# -*- coding: utf-8 -*-
from lxml.builder import E
from odoo import api, fields, models, _
from odoo.tools import make_index_name, create_index


class RecruitmentCustomField(models.Model):
    """Custom field templates for hr.applicant"""
    _name = 'recruitment.custom.field'
    _description = 'Recruitment Custom Field'
    _order = 'sequence, id'

    name = fields.Text('Field Name', required=True, translate=True)
    description = fields.Text('Description', translate=True)
    sequence = fields.Integer('Sequence', default=10)
    active = fields.Boolean('Active', default=True)
    field_type = fields.Selection([
        ('char', 'Text'),
        ('text', 'Multiline Text'),
        ('integer', 'Integer'),
        ('float', 'Decimal'),
        ('boolean', 'Checkbox'),
        ('date', 'Date'),
        ('datetime', 'DateTime'),
        ('selection', 'Dropdown'),
        ('many2one', 'Many2one'),
    ], string='Field Type', default='char', required=True)
    selection_values = fields.Text('Selection Values', help='One per line for dropdown')
    relation_model = fields.Char('Related Model', help='e.g. res.partner')
    anchor_field = fields.Selection([
        ('partner_name', 'Name'),
        ('job_id', 'Job Position'),
        ('contract_type_id', 'Contract Type'),
        ('vgr', 'VGR'),
        ('ngr', 'NGR'),
        ('lag', 'LAG'),
        ('che', 'CHE'),
        ('bei', 'BEI'),
        ('vcr', 'VCR'),
        ('ncr', 'NCR'),
        ('last_test', 'Date of Online Test'),
        ('stage_id', 'Recruitment Phase'),
        ('hire_decision', 'Recruitment Status'),
        ('applicant_notes', 'Notes'),
        ('meets_staff_requirements', 'Meets Requirements'),
        ('create_date', 'Applied on'),
    ], string='Position', default='ncr', required=True)
    position = fields.Selection([
        ('before', 'Before'),
        ('after', 'After'),
    ], string='Insert', default='after', required=True)

    def _column_name(self):
        self.ensure_one()
        return f"x_field{self.id}_value"

    def _find_template_column(self, model=False):
        domain = [('name', 'in', [t._column_name() for t in self])]
        if model:
            domain.append(('model', '=', model))
        else:
            domain.append(('model', '=', 'hr.applicant'))
        return self.env['ir.model.fields'].sudo().search(domain)

    def _sync_all_template_columns(self):
        """Sync fields on hr.applicant model"""
        self._sync_template_column('hr.applicant')

    def _sync_template_column(self, model):
        for template in self:
            column = template._column_name()
            
            existing_field = self.env['ir.model.fields'].sudo().search([
                ('name', '=', column),
                ('model', '=', model)
            ], limit=1)

            # If field exists and type changed, delete it first
            if existing_field and existing_field.ttype != template.field_type:
                existing_field.sudo().unlink()
                existing_field = False

            field_data = {
                'name': column,
                'field_description': template.name,
                'state': 'manual',
                'model': model,
                'model_id': self.env['ir.model']._get_id(model),
                'ttype': template.field_type,
                'copied': True,
            }

            if template.field_type == 'selection' and template.selection_values:
                options = [line.strip() for line in template.selection_values.split('\n') if line.strip()]
                field_data['selection'] = str([(opt, opt) for opt in options])
            
            if template.field_type == 'many2one' and template.relation_model:
                field_data['relation'] = template.relation_model

            if not existing_field:
                field = self.env['ir.model.fields'].with_context(
                    update_custom_fields=True
                ).sudo().create(field_data)
                
                Model = self.env[model]
                if Model._auto:
                    tablename = Model._table
                    indexname = make_index_name(tablename, column)
                    try:
                        create_index(self.env.cr, indexname, tablename, [column], 'btree', f'{column} IS NOT NULL')
                        field['index'] = True
                    except Exception:
                        pass
            else:
                existing_field.write(field_data)

    def write(self, vals):
        res = super().write(vals)
        if any(key in vals for key in ['name', 'field_type', 'selection_values', 'relation_model', 'active']):
            try:
                self._sync_all_template_columns()
                self.env.registry.clear_cache('stable')
                self.env.registry.init_models(self.env.cr, ['hr.applicant'], self.env.context)
            except Exception:
                pass
        return res

    def unlink(self):
        try:
            self._find_template_column().unlink()
        except Exception:
            pass
        res = super().unlink()
        try:
            self.env.registry.clear_cache('stable')
            self.env.registry.init_models(self.env.cr, ['hr.applicant'], self.env.context)
        except Exception:
            pass
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'type': 'success',
                'message': 'Field deleted. Page will reload...',
                'next': {
                    'type': 'ir.actions.client',
                    'tag': 'reload',
                },
            }
        }

    @api.model
    def create(self, vals):
        record = super().create(vals)
        try:
            record._sync_all_template_columns()
            self.env.registry.clear_cache('stable')
            self.env.registry.init_models(self.env.cr, ['hr.applicant'], self.env.context)
        except Exception:
            pass
        return record
    
    def action_refresh_page(self):
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }


class RecruitmentCustomFieldMixin(models.AbstractModel):
    """Mixin that provides dynamic fields for hr.applicant"""
    _name = 'recruitment.custom.field.mixin'
    _description = 'Recruitment Custom Field Mixin'

    def _get_template_fnames(self):
        templates = self.env['recruitment.custom.field'].search([('active', '=', True)])
        return [fname for template in templates if (fname := template._column_name()) in self]

    def _get_field_responses(self):
        """Return dict of template_id: response for this record"""
        result = {}
        for fname in self._get_template_fnames():
            if self[fname]:
                template_id = int(fname.split('field')[1].split('_')[0])
                result[template_id] = self[fname]
        return result

    @api.model
    def fields_get(self, allfields=None, attributes=None):
        fields = super().fields_get(allfields, attributes)
        try:
            if not self.env.context.get("studio"):
                templates = self.env['recruitment.custom.field'].search([('active', '=', True)])
                for template in templates:
                    fname = template._column_name()
                    if fname in fields:
                        fields[fname]['string'] = template.name
        except Exception:
            pass
        return fields

    def _get_view(self, view_id=None, view_type='form', **options):
        arch, view = super()._get_view(view_id, view_type, **options)
        try:
            return self._patch_view(arch, view, view_type)
        except Exception:
            return arch, view

    def _patch_view(self, arch, view, view_type):
        try:
            if not self.env.context.get("studio"):
                templates = self.env['recruitment.custom.field'].search([('active', '=', True)], order='sequence')
                
                if view_type == 'list':
                    for template in templates:
                        fname = template._column_name()
                        if fname not in self._fields:
                            continue
                        
                        # Try to find anchor field in the view
                        anchor_node = arch.find(f'.//field[@name="{template.anchor_field}"]')
                        
                        # Fallback: if anchor not found, use create_date as last field
                        if anchor_node is None:
                            anchor_node = arch.find('.//field[@name="create_date"]')
                        
                        if anchor_node is None:
                            continue
                        
                        field_attrs = {
                            'name': fname,
                            'optional': 'show',
                            'width': '150px',
                        }
                        
                        if template.field_type == 'text':
                            field_attrs['widget'] = 'text'
                        elif template.field_type == 'boolean':
                            field_attrs['widget'] = 'boolean_toggle'
                        elif template.field_type in ('date', 'datetime', 'float', 'integer'):
                            field_attrs['widget'] = template.field_type
                        
                        new_field = E.field(**field_attrs)
                        if template.position == 'before':
                            anchor_node.addprevious(new_field)
                        else:
                            anchor_node.addnext(new_field)
                
                elif view_type == 'form':
                    page_assessment = arch.find('.//page[@name="assessment"]')
                    if page_assessment is not None:
                        for template in templates:
                            fname = template._column_name()
                            if fname not in self._fields:
                                continue
                            
                            anchor_node = page_assessment.find(f'.//field[@name="{template.anchor_field}"]')
                            if anchor_node is None:
                                continue
                            
                            field_attrs = {'name': fname}
                            
                            if template.field_type == 'text':
                                field_attrs['widget'] = 'text'
                            elif template.field_type == 'boolean':
                                field_attrs['widget'] = 'boolean_toggle'
                            elif template.field_type in ('date', 'datetime'):
                                field_attrs['widget'] = template.field_type
                            
                            new_field = E.field(**field_attrs)
                            if template.position == 'before':
                                anchor_node.addprevious(new_field)
                            else:
                                anchor_node.addnext(new_field)
        except Exception:
            pass
        
        return arch, view


class HrApplicant(models.Model):
    _inherit = ['hr.applicant', 'recruitment.custom.field.mixin']
