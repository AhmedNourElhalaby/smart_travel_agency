from datetime import timedelta, datetime
import base64
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo import api, fields, models

class AgentUsersWizard(models.TransientModel):
    _name = 'agent.user.wizard'

    name = fields.Char('Name')
    username = fields.Char('User Name')
    password = fields.Char('Password')
    branch=fields.Boolean(default=False)
    travel_agency = fields.Many2one('travel.agency', 'Travel Agency')
    travel_agency_branch = fields.Many2one('agency.branch', 'Agency Branch')

    # @api.multi
    def generate_users(self):
        self.env['res.users'].create({'name': self.name, 'login': self.name,'password':self.password, 'groups_id': [
            self.env['res.groups'].search([('name', '=', 'User: All Agency Documents')]).id]})

    # @api.multi
    def generate_branch_users(self):
        self.env['res.users'].create({'name': self.name+'-'+str(self.travel_agency.agency_code), 'login': self.name+'-'+str(self.travel_agency.agency_code),'travel_agency_branch':self.id,'travel_agency':self.travel_agency.id, 'password': self.password, 'groups_id': [
            self.env['res.groups'].search([('name', '=', 'User: Own Documents')]).id]})
