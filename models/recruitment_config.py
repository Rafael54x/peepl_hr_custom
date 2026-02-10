# -*- coding: utf-8 -*-

from odoo import models, fields

class RecruitmentTestConfig(models.Model):
    _name = 'recruitment.test.config'
    _description = 'Test Configuration'
    _order = 'sequence, name'

    name = fields.Char('Test Name', required=True)
    code = fields.Char('Code', required=True)
    sequence = fields.Integer('Sequence', default=10)
    active = fields.Boolean('Active', default=True)

class RecruitmentPhaseConfig(models.Model):
    _name = 'recruitment.phase.config'
    _description = 'Recruitment Phase Configuration'
    _order = 'sequence, name'

    name = fields.Char('Phase Name', required=True)
    code = fields.Char('Code', required=True)
    sequence = fields.Integer('Sequence', default=10)
    active = fields.Boolean('Active', default=True)

class RecruitmentStatusConfig(models.Model):
    _name = 'recruitment.status.config'
    _description = 'Recruitment Status Configuration'
    _order = 'sequence, name'

    name = fields.Char('Status Name', required=True)
    code = fields.Char('Code', required=True)
    sequence = fields.Integer('Sequence', default=10)
    active = fields.Boolean('Active', default=True)