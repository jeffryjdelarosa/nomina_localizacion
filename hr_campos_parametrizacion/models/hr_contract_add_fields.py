# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
import re
from odoo import api, fields, models, _ , exceptions
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class Contract(models.Model):
    _name = 'hr.contract'
    _inherit = ["hr.contract"]

    #######################################ASIGNACIONES##################################################################
    night_bonus_check = fields.Boolean(string='Night Bonus')
    night_bonus_value = fields.Integer(string='Night Bonus Value', default=7)
    #night_bonus = fields.Float(string='Night Bonus', digits=(10,2))
    days_of_salary_pending_check = fields.Boolean(string='Days of Salary Pending')
    days_of_salary_pending_value = fields.Integer('Days of Salary Pending Value', size=2)
    sundays_check = fields.Boolean(string='Sundays')
    sundays_value = fields.Integer(string='Sunday value')
    holidays_check = fields.Boolean(string='Holidays')
    holidays_value = fields.Integer('Holidays Value')
    holiday_not_worked_check = fields.Boolean(string='Holiday not Worked')
    holiday_not_worked_value = fields.Integer(string='Holiday not Worked Value', size=2)
    diurnal_extra_hours_check = fields.Boolean(string='Diurnal Extra Hours')
    diurnal_extra_hours_value = fields.Char(string='Diurnal Extra Hours Value', size=5, help="Accepts values between 00:00 and 23:59")
    nocturnal_extra_hours_check = fields.Boolean(string='Nocturnal Extra Hours')
    diurnal_extra_hours = fields.Float(string='Diurnal Extra Hours',digits=(10,2), store=True)
    salary_assignment_check = fields.Boolean(string='Salary Assignment')
    salary_assignment_value = fields.Integer(string='Salary Assignment Value')
    non_salary_assignation_check = fields.Boolean(string='Non-Salary Assignation')
    non_salary_assignation_value = fields.Float(string='Non-Salary Assignation Value', digits=(10,2))
    ##################################### DEDUCCIONES########################################################################################
    hours_not_worked_check = fields.Boolean(string='Hours not Worked')
    hours_not_worked_value = fields.Char(string='Hours not Worked Value', size=5, help="Accepts values between 00:00 and 23:59")
    hours_not_worked = fields.Float('Hours not Worked', digits=(10, 2))
    unexcused_absences_check = fields.Boolean(string='Unexcused Absences')
    #unexcused_absences_value = fields.Char(string='Unexcused Absences Value', size=5, help="Accepts values between 00:00 and 23:59")
    unexcused_absences_value = fields.Integer(string='Unexcused Absences', size=2)
    unpaid_permit_days_check = fields.Boolean(string='Unpaid Permit Days')
    unpaid_permit_days_value = fields.Integer(string='Unpaid Permit Value Days', size=2)
    unpaid_permit_hours_check = fields.Boolean(string='Unpaid Permit Hours')
    unpaid_permit_hours_value = fields.Char(string='Unpaid Permit Hours Value', size=5, help="Accepts values between 00:00 and 23:59")
    unpaid_permit_hours = fields.Float(string='Unpaid Permit Hours', digits=(10, 2))
    faov_withholding_check = fields.Boolean(string='F.A.O.V. Withholding')
    saving_fund_withholding_check = fields.Boolean(string='Saving Fund Withholding')
    islr_withholding_check = fields.Boolean(string='I.S.L.R. Withholding')
    islr_withholding_value = fields.Float(string='I.S.L.R. Withholding Value', digits=(2,2))
    # 'retencion_pie_check = fields.Boolean('Retencion P.I.E.')non_salary_deduction_value
    # 'retencion_sso_check = fields.Boolean('Retencion S.S.O.')
    salary_deduction_check = fields.Boolean(string='Salary Deduction')
    salary_deduction_value = fields.Float(string='Salary Deduction Value', digits=(10, 2))
    non_salary_deduction_check = fields.Boolean(string='Non-Salary Deduction')
    non_salary_deduction_value = fields.Integer(string='Non-Salary Deduction Value')
    deduction_bono_vac_check = fields.Boolean(string='Deduction Bono Vacacional')
    deduction_bono_vac_value = fields.Integer(string='Deduction Bono Vacacional value')
    ausencias_ded_check= fields.Boolean(string='Cantidad de dias de Ausencias check')
    ausencias_ded_value = fields.Integer(string='Cantidad de dias de Ausencias value')
    dcto_sso_check = fields.Boolean('Activar dcto SSO')
    dcto_reg_prest_empleo_check = fields.Boolean('Activar dtco regimen prestacional de empleo')
    retencion_faov_check = fields.Boolean('Retencion FAOV')
    subsidio_patria_check = fields.Boolean('Subsidio Patria')
    subsidio_patria_value = fields.Float(string='Subsidio Patria Value')
    retroactivo_check = fields.Boolean('Retroactivo')
    retroactivo_value = fields.Float(string='Retroactivo')
    prestamo_check = fields.Boolean('Prestamo')
    prestamo_value = fields.Float(string='Prestamo')
    reposo_33_check = fields.Boolean('Reposo 33%')
    cuenta_seguro_medico_check= fields.Boolean('Cuenta de Seguro Medico Colectivo de Familiares')
    cuenta_seguro_medico_value = fields.Float(string='Cuenta de Seguro Medico Colectivo de Familiares')
    anticipo_extra_check = fields.Boolean('Anticipo Extraordinario')
    anticipo_extra_value = fields.Float(string='Anticipo extraordinaro')
    dias_reposo_check= fields.Boolean('Dias de reposo')
    dias_reposo_value = fields.Integer('Dias de Reposo')
    salary_retroactive_check = fields.Boolean(string='Salary Retroactive')
    salary_retroactive_value = fields.Float(string='Salary Retroactive Value', digits=(10,2))
    bono_alimenticio_check = fields.Boolean(string='Bono Alimenticio')
    bono_alimenticio_value = fields.Float(string='Monto bono alimenticio', digits=(10,2))
    bono_alimenticio_currency = fields.Many2one('res.currency','Moneda')