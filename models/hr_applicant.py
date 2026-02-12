from odoo import models, fields, api
from odoo.exceptions import UserError

class HrApplicant(models.Model):
    _inherit = 'hr.applicant'

    last_test = fields.Date('Last Test')
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
    contract_type_id = fields.Many2one('hr.contract.type', 'Contract Type')
    
    def write(self, vals):
        if 'stage_id' in vals and not self.env.context.get('import_file'):
            for rec in self:
                if rec.hire_decision == 'do_not_pursue':
                    raise UserError('Cannot change stage for applicants with "Do Not Pursue" status.')
        return super().write(vals)