# coding: utf-8
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _
import calendar
from odoo.exceptions import UserError, ValidationError

class hr_tiempo_servicio(models.Model):
    _name = 'hr.payroll.dias.vacaciones'
    _description = 'Tiempo Servicio'

    service_years= fields.Integer()
    pay_day = fields.Integer()