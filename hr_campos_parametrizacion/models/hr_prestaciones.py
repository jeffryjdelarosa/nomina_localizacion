# coding: utf-8
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _
import calendar
from odoo.exceptions import UserError, ValidationError

class hr_tiempo_servicio(models.Model):
    _name = 'hr.payroll.prestaciones'
    _description = 'Tabla de Prestaciones'

    company_id = fields.Many2one("res.company", string="Compañia", default=lambda self: self.env.company)
    employee_id=fields.Many2one("hr.employee",string="Empleado")
    ano= fields.Integer()
    mes = fields.Integer(string='Mes cumplido')
    nro_mes = fields.Integer()
    sueldo_int_mensual = fields.Float()
    nro_ano = fields.Integer()
    dias_disfrutes = fields.Integer(string='Dias de prestaciones')
    alicuota = fields.Float()
    retiros = fields.Float()
    acumulado = fields.Float()

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    ultimo_suldo_base_mensual = fields.Float()


    def action_payslip_done(self):
        #raise UserError(_('Prueba BEBE'))
        res = super(HrPayslip, self).action_payslip_done()
        sueldo_base_mensual=0.0001
        nro_ano=dias_disfrutes=alicuota=acumulado=0
        mes=0
        mes_nomina=self.mes(self.date_to)
        ano_actual=self.ano(self.date_to)
        valida=self.env['hr.payroll.prestaciones'].search([('employee_id','=',self.employee_id.id),('ano','=',ano_actual),('nro_mes','=',mes_nomina)])
        if not valida:
            if self.contract_id.wage>0:
                sueldo_base_mensual=self.contract_id.wage
                self.ultimo_suldo_base_mensual=sueldo_base_mensual
            if self.tiempo_antiguedad>0:
                nro_ano=self.tiempo_antiguedad
            indicadores=self.env['hr.payroll.indicadores.economicos'].search([('code','=','DUT')])
            if indicadores:
                for det_indi in indicadores:
                    nro_dias_utilidades=det_indi.valor
            verifica=self.env['hr.payroll.prestaciones'].search([('employee_id','=',self.employee_id.id),('id','!=',self.id)],order="mes ASC") #('ano','=',ano_actual)
            if verifica:
                #raise UserError(_('Ya hay una nomina procesada/pagada en el mes seleccionado para %s')%self.employee_id.name)
                for det_v in verifica:
                    #acumulado=det_v.alicuota
                    if det_v.mes==11:
                        mes=0
                    else:
                        mes=det_v.mes+1
            if mes==3 or mes==6 or mes==9:
                dias_disfrutes=15
            if mes==0:
                busca_mes=self.env['hr.payroll.prestaciones'].search([('employee_id','=',self.employee_id.id),('mes','=','0'),('id','!=',self.id)],order="mes ASC")
                if busca_mes:
                    dias_disfrutes=15
                if not busca_mes:
                    dias_disfrutes=0
            #if self.tiempo_antiguedad==0:
                #dias_disfrutes=15
            #if self.tiempo_antiguedad>0:
                #dias_disfrutes=self.dias_vacaciones+1
            sueldo_base_diario=sueldo_base_mensual/30
            fraccion_diaria_vaca=sueldo_base_diario*self.dias_vacaciones/360
            fraccion_diaria_utilidades=sueldo_base_diario*nro_dias_utilidades/360
            sueldo_integral_mensual=(sueldo_base_diario+fraccion_diaria_vaca+fraccion_diaria_utilidades)*30

            alicuota=(sueldo_integral_mensual/30)*dias_disfrutes
            acumulado=self.compute_acumulado()+alicuota

            ret = self.env['hr.payroll.prestaciones']
            values = {
            'employee_id': self.employee_id.id,
            'sueldo_int_mensual':sueldo_integral_mensual,
            'nro_ano':nro_ano,
            'mes':mes,
            'nro_mes':mes_nomina,
            'ano':self.ano(self.date_to),
            'dias_disfrutes':dias_disfrutes,
            'alicuota':alicuota,
            'acumulado':acumulado,
            }
            rets=ret.create(values)

    def compute_acumulado(self):
        acum=0
        lista=self.env['hr.payroll.prestaciones'].search([('employee_id','=',self.employee_id.id),('id','!=',self.id),('nro_mes','!=',self.mes(self.date_to))])
        if lista:
            for det in lista:
                acum=acum+det.alicuota
        return acum

    def mes(self,date):
        fecha = str(date)
        fecha_aux=fecha
        mes=fecha[5:7]
        resultado=mes
        return int(resultado)

    def ano(self,date):
        fecha = str(date)
        fecha_aux=fecha
        ano=fecha_aux[0:4]  
        resultado=ano
        return int(resultado)
