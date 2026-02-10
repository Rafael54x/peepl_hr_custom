from odoo import models, fields, api
from odoo.exceptions import UserError

class HrApplicant(models.Model):
    _inherit = 'hr.applicant'

    # Assessment Fields
    last_test = fields.Date('Last Test')
    vgr = fields.Float('VGR')
    ngr = fields.Float('NGR')
    lag = fields.Float('LAG')
    che = fields.Float('CHE')
    bei = fields.Selection([
        ('a1', 'A1'), ('a2', 'A2'), 
        ('b1', 'B1'), ('b2', 'B2'), 
        ('c1', 'C1'), ('c2', 'C2')
    ], 'BEI')
    vcr = fields.Float('VCR')
    ncr = fields.Float('NCR')
    
    @api.model
    def get_view(self, view_id=None, view_type='form', **options):
        res = super().get_view(view_id, view_type, **options)
        if view_type == 'tree':
            active_tests = self.env['recruitment.test.config'].search([('active', '=', True)])
            test_codes = [t.code.lower() for t in active_tests]
            
            # Parse XML and modify fields visibility
            from lxml import etree
            doc = etree.XML(res['arch'])
            
            # Hide inactive test fields
            all_test_fields = ['vgr', 'ngr', 'lag', 'che', 'bei', 'vcr', 'ncr']
            for field_name in all_test_fields:
                if field_name not in test_codes:
                    for field in doc.xpath(f"//field[@name='{field_name}']"):
                        field.set('column_invisible', '1')
            
            res['arch'] = etree.tostring(doc, encoding='unicode')
        return res
    
    # Recruitment Progress
    recruitment_phase = fields.Selection([
        ('online_failed', 'Online Test Failed'),
        ('online_passed', 'Online Test Passed'),
        ('ai_interview', 'AI Interview'),
        ('user_interview', 'User Interview'),
        ('psc_interview', 'PSC Interview')
    ], 'Phase')
    
    hire_decision = fields.Selection([
        ('on_progress', 'On Progress'),
        ('recommended', 'Recommended'),
        ('offer_made', 'Offer Made'),
        ('do_not_pursue', 'Do Not Pursue')
    ], 'Decision')
    
    # Validation Fields
    contract_type_id = fields.Many2one('hr.contract.type', 'Contract Type')
    meets_staff_requirements = fields.Boolean('Meets Requirements', compute='_compute_staff_requirements', store=True)
    total_score = fields.Float('Total Score', compute='_compute_total_score', store=True)
    
    @api.depends('vgr', 'ngr', 'lag', 'che', 'bei', 'vcr', 'ncr', 'contract_type_id')
    def _compute_staff_requirements(self):
        for rec in self:
            if not rec.contract_type_id:
                rec.meets_staff_requirements = False
                continue
                
            contract_name = rec.contract_type_id.name.lower()
            
            if 'staff' in contract_name:
                meets_requirements = (
                    (rec.vgr or 0) >= 5 and
                    (rec.ngr or 0) >= 5 and
                    (rec.lag or 0) >= 5 and
                    (rec.che or 0) >= 7 and
                    rec.bei in ['b1', 'b2', 'c1', 'c2'] and
                    (rec.vcr or 0) >= 4 and
                    (rec.ncr or 0) >= 4
                )
            elif 'spv' in contract_name or 'supervisor' in contract_name or 'manager' in contract_name:
                meets_requirements = (
                    (rec.vgr or 0) >= 6 and
                    (rec.ngr or 0) >= 6 and
                    (rec.lag or 0) >= 6 and
                    (rec.che or 0) >= 8 and
                    rec.bei in ['b1', 'b2', 'c1', 'c2'] and
                    (rec.vcr or 0) >= 6 and
                    (rec.ncr or 0) >= 6
                )
            else:
                meets_requirements = False
                
            rec.meets_staff_requirements = meets_requirements
            
            if meets_requirements:
                rec.hire_decision = 'on_progress'
            else:
                rec.hire_decision = 'do_not_pursue'
    
    @api.onchange('vgr', 'ngr', 'lag', 'che', 'bei', 'vcr', 'ncr', 'contract_type_id')
    def _onchange_validation_fields(self):
        self._compute_staff_requirements()
    
    @api.depends('vgr', 'ngr', 'lag', 'che', 'vcr', 'ncr')
    def _compute_total_score(self):
        for rec in self:
            scores = [rec.vgr or 0, rec.ngr or 0, rec.lag or 0, rec.che or 0, rec.vcr or 0, rec.ncr or 0]
            rec.total_score = sum(scores) / len([s for s in scores if s > 0]) if any(scores) else 0
    
    def write(self, vals):
        if 'stage_id' in vals and not self.env.context.get('import_file'):
            for rec in self:
                if rec.hire_decision == 'do_not_pursue':
                    raise UserError('Cannot change stage for applicants with "Do Not Pursue" status.')
        return super().write(vals)