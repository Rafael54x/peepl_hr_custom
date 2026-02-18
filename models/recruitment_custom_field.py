# -*- coding: utf-8 -*-
import operator
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
        ('last_test', 'Date of Online Test'),
        ('stage_id', 'Recruitment Phase'),
        ('hire_decision', 'Recruitment Status'),
        ('applicant_notes', 'Notes'),
        ('create_date', 'Applied on'),
    ], string='Position', default='last_test', required=True)
    position = fields.Selection([
        ('before', 'Before'),
        ('after', 'After'),
    ], string='Insert', default='after', required=True)
    
    # Validation Rules
    validation_active = fields.Boolean('Enable Auto-Decision', help='Auto-update hire_decision based on field value')
    validation_operator = fields.Selection([
        ('=', 'Equal to'),
        ('!=', 'Not Equal to'),
        ('>', 'Greater than'),
        ('>=', 'Greater or Equal'),
        ('<', 'Less than'),
        ('<=', 'Less or Equal'),
        ('in', 'In (comma separated)'),
        ('not in', 'Not In (comma separated)'),
        ('between', 'Between (min,max)'),
    ], string='Operator')
    validation_value = fields.Char('Threshold Value', help='Value to compare. Examples:\n- Single: 60\n- Multiple: A,B,C\n- Range: 50,100')
    target_decision = fields.Many2one('recruitment.status.config', string='Set Decision To', domain=[('active', '=', True)], ondelete='set null')
    default_decision = fields.Many2one('recruitment.status.config', string='Default Decision', domain=[('active', '=', True)], ondelete='set null', help='Set this decision if no validation rule matches')

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
        if any(key in vals for key in ['name', 'field_type', 'selection_values', 'relation_model', 'active', 'anchor_field', 'position', 'sequence']):
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
                templates = self.env['recruitment.custom.field'].search([('active', '=', True)], order='sequence, id')
                
                if view_type == 'list':
                    # Track inserted fields to avoid duplicates
                    inserted = set()
                    
                    for template in templates:
                        fname = template._column_name()
                        if fname not in self._fields or fname in inserted:
                            continue
                        
                        anchor_node = arch.find(f'.//field[@name="{template.anchor_field}"]')
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
                        
                        inserted.add(fname)
                
                elif view_type == 'form':
                    page_assessment = arch.find('.//page[@name="assessment"]')
                    if page_assessment is not None:
                        inserted = set()
                        
                        for template in templates:
                            fname = template._column_name()
                            if fname not in self._fields or fname in inserted:
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
                            
                            inserted.add(fname)
        except Exception:
            pass
        
        return arch, view


    def _apply_dynamic_rules(self):
        """Apply validation rules to update hire_decision"""
        ops = {'=': operator.eq, '!=': operator.ne, '>': operator.gt, '>=': operator.ge, '<': operator.lt, '<=': operator.le}
        
        templates = self.env['recruitment.custom.field'].search([
            ('active', '=', True),
            ('validation_active', '=', True)
        ])
        
        for record in self:
            for template in templates:
                fname = template._column_name()
                if fname not in record or not record[fname]:
                    # Set default decision if field has value and default is set
                    if fname in record and template.default_decision:
                        record.hire_decision = template.default_decision.code
                    continue
                
                # Check if validation rule exists
                if not template.validation_operator or not template.target_decision:
                    # No validation rule, use default if set
                    if template.default_decision:
                        record.hire_decision = template.default_decision.code
                    continue
                
                try:
                    user_val = record[fname]
                    rule_val = template.validation_value
                    op = template.validation_operator
                    rule_matched = False
                    
                    # Handle 'in' operator
                    if op == 'in':
                        values = [v.strip() for v in rule_val.split(',')]
                        if template.field_type in ('integer', 'float'):
                            values = [float(v) for v in values]
                            user_val = float(user_val)
                        if user_val in values:
                            record.hire_decision = template.target_decision.code
                            rule_matched = True
                    
                    # Handle 'not in' operator
                    elif op == 'not in':
                        values = [v.strip() for v in rule_val.split(',')]
                        if template.field_type in ('integer', 'float'):
                            values = [float(v) for v in values]
                            user_val = float(user_val)
                        if user_val not in values:
                            record.hire_decision = template.target_decision.code
                            rule_matched = True
                    
                    # Handle 'between' operator
                    elif op == 'between':
                        min_val, max_val = [v.strip() for v in rule_val.split(',')]
                        if template.field_type in ('integer', 'float'):
                            min_val, max_val = float(min_val), float(max_val)
                            user_val = float(user_val)
                            if min_val <= user_val <= max_val:
                                record.hire_decision = template.target_decision.code
                                rule_matched = True
                        else:
                            if template.selection_values:
                                options = [v.strip() for v in template.selection_values.split('\n') if v.strip()]
                                try:
                                    min_idx = options.index(min_val)
                                    max_idx = options.index(max_val)
                                    user_idx = options.index(user_val)
                                    if min_idx <= user_idx <= max_idx:
                                        record.hire_decision = template.target_decision.code
                                        rule_matched = True
                                except ValueError:
                                    pass
                    
                    # Standard operators for selection
                    elif template.field_type == 'selection' and op in ('>', '>=', '<', '<='):
                        if template.selection_values:
                            options = [v.strip() for v in template.selection_values.split('\n') if v.strip()]
                            try:
                                user_idx = options.index(user_val)
                                rule_idx = options.index(rule_val)
                                if ops[op](user_idx, rule_idx):
                                    record.hire_decision = template.target_decision.code
                                    rule_matched = True
                            except ValueError:
                                pass
                    
                    # Standard operators for numeric
                    else:
                        if template.field_type in ('integer', 'float'):
                            user_val = float(user_val)
                            rule_val = float(rule_val)
                        
                        if ops[op](user_val, rule_val):
                            record.hire_decision = template.target_decision.code
                            rule_matched = True
                    
                    # If no rule matched, use default
                    if not rule_matched and template.default_decision:
                        record.hire_decision = template.default_decision.code
                        
                except:
                    # On error, use default if set
                    if template.default_decision:
                        record.hire_decision = template.default_decision.code
                    continue
    
    @api.model
    def create(self, vals):
        record = super().create(vals)
        record._apply_dynamic_rules()
        return record
    
    def write(self, vals):
        res = super().write(vals)
        if any(k.startswith('x_field') for k in vals.keys()):
            self._apply_dynamic_rules()
        return res


class HrApplicant(models.Model):
    _inherit = ['hr.applicant', 'recruitment.custom.field.mixin']
