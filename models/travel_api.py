from datetime import timedelta, datetime
import base64
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo import api, fields, models
class Travelapi(models.Model):
    _name='travel.front'

    # @api.multi
    def create_test(self):
        self.create_policy({'package':'family','dob':'2002-1-1','p_from':'2020-5-30','p_to':'2020-6-3','family':[{'name':'eslam','dob':'2005-12-2','passport_num':587961,'type':'kid','gender':'M'}]})

    @api.model
    def create_policy(self, data):
        DOB = datetime.strptime(data.get('dob'), '%Y-%m-%d').date()
        when = datetime.strptime(data.get('p_from'), '%Y-%m-%d').date()
        to = datetime.strptime(data.get('p_to'), '%Y-%m-%d').date()
        policy_id = self.env['policy.travel'].create(
            {'package': data.get('package'), 'insured': data.get('c_name'), 'address': data.get('add'),
             'gender': data.get('gender'), 'source': data.get('source'), 'passport_num': data.get('pass'),
             'national_id': data.get('id'), 'phone': data.get('phone'),
             'DOB': DOB, 'geographical_coverage': data.get('zone'), 'coverage_from': when, 'coverage_to': to,
             'state': 'approved'})
        if data.get('family'):
            for rec in data.get('family'):
               f= self.env['policy.family.age'].create(
                    {'pass_num': rec['passport_num'], 'name': rec['name'], 'DOB': rec['dob'], 'type': rec['type'],
                     'gender': rec['gender'], 'policy_id': policy_id.id})

               self.env['policy.family.age'].search([('id', '=', f.id)]).get_age()

        self.env['policy.travel'].search([('id', '=', policy_id.id)]).get_financial_data()
        self.env['policy.travel'].search([('id', '=', policy_id.id)]).send_mail_template(data.get('mail'))
        return [policy_id.id,policy_id.policy_num]

    @api.model
    def get_periods(self,data):
        x = data
        options = []
        data = self.env['travel.price.line'].search([('price_id.package', '=', 'individual'),('price_id.zone', '=', 'zone 1'),('price_id.from_age', '=', 0.00)])
        for option in data:
            options.append(option.period)
        print(options)
        return options




