# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2013-2015 Open Business Solutions, SRL.
#    Write by Ernesto Mendez (tecnologia@obsdr.com)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


from openerp.osv import osv, fields
import base64
from openerp.tools.translate import _
import time, datetime
from openerp import tools
import pdb
from openerp.exceptions import Warning

#_logger = logging.getLogger(__name__)

def _get_month(self, cursor, user_id, context=None):
    return (
       ('01', 'Enero'),
       ('02', 'Febrero'),
       ('03', 'Marzo'),
       ('04', 'Abril'),
       ('05', 'Mayo'),
       ('06', 'Junio'),
       ('07', 'Julio'),
       ('08', 'Agosto'),
       ('09', 'Septimbre'),
       ('10', 'Octubre'),
       ('11', 'Noviembre'),
       ('12', 'Diciembre')
    )

class tss_report(osv.Model):
    _name = 'tss.report'
    _description = 'Archivo de Autodeterminacion TSS'


    def _line_count(self, cr, uid, ids, context=None):
        tss_report_obj = self.pool.get('tss.report')
        tss_report = tss_report_obj.browse(cr, uid, ids, context=context)[0]
        return len(tss_report.tss_report_line_ids)

    def _get_updated_fields(self, cr, uid, ids, context=None):
        vals = {}
        vals['company_id'] = 1
        vals['line_count'] = self._line_count(cr, uid, ids, context=context)
        return vals

    _columns = {
        #'name': fields.char('Nombre'),
        'company_id': fields.many2one('res.company', u'Compañia', required=True),
        'tipo_de_archivo': fields.selection([
            ('AM','AM'),
            ('AR','AR')], string='Tipo de Archivo', size=2, required=True),
        'period_id': fields.many2one('account.period', u'Período', required=True),
        'line_count': fields.integer(u"Total de registros", readonly=True),
        'report': fields.binary(u"Reporte", readonly=True),
        'report_name': fields.char(u"Nombre de Reporte", 40, readonly=True),
        'tss_report_line_ids': fields.one2many('tss.report.line', 'tss_report_id', u'Lineas'),
        'state': fields.selection((('draft','Pendiente'),('sent','Enviado'),('cancel','Cancel')),
                                  'State', readonly=True),

    }

    _defaults = {
        'company_id': lambda self, cr, uid, c: self.pool.get('res.users').browse(cr, uid, uid, c).company_id.id,
        'state': 'draft',
        }

    def create(self, cr, uid, values, context=None):
        """

        """

        res = super(tss_report, self).create(cr, uid, values, context=context)

        # Loads all purchases
        self.create_tss_report_line(cr, uid, res, values['period_id'], context=context)

        # Update readonly fields
        vals = self._get_updated_fields(cr, uid, [res], context=None)
        self.write(cr, uid, [res], vals)
        return res

    def write(self, cr, uid, ids, vals, context=None):
        """
        Re-write to update read-only fields.

        """
        super(tss_report, self).write(cr, uid, ids, vals, context)
        vals.update(self._get_updated_fields(cr, uid, ids, context=None))

        result = super(tss_report, self).write(cr, uid, ids, vals, context)
        return result
    '''
    def re_create_payslip_run_line(self, cr, uid, ids, context=None):
        lines_obj = self.pool.get('bhd.payslip.run.line.report')
        report = self.browse(cr, uid, ids[0])
        line_ids = [line.id for line in report.payslip_run_line_report_ids]
        lines_obj.unlink(cr, uid, line_ids)

        result = self.create_payslip_run_line(cr, uid, report.id, report.payslip_run_id.id, context=context)

        vals = self._get_updated_fields(cr, uid, ids, context=None)
        self.write(cr, uid, ids, vals)

        return result
    '''
    def create_tss_report_line(self, cr, uid, tss_report_id, period_id, context=None):
        #pdb.set_trace()

        wizard = self.browse(cr, uid, tss_report_id, context=context)

        #payslip_run_id = self.browse(cr, uid, payslip_run_id)
        hr_payslip_obj = self.pool.get('hr.payslip')
        hr_payslip_run_obj = self.pool.get('hr.payslip.run')
        hr_payslip_line_obj = self.pool.get('hr.payslip.line')
        tss_report_line_obj = self.pool.get('tss.report.line')
        account_period_obj = self.pool.get('account.period')
        hr_employee_obj = self.pool.get('hr.employee')
        hr_salary_rule_category_obj = self.pool.get('hr.salary.rule.category')

        period = account_period_obj.search(cr, uid, [("id", "=", period_id)])
        period_vals = account_period_obj.browse(cr, uid, period)

        date_from = period_vals.date_start
        date_to = period_vals.date_stop

        contract_obj = self.pool.get('hr.contract')

        '''
        draft_payslip_ids = hr_payslip_obj.search(cr, uid, [("state", "in", ["draft", "verify", "cancel"]),
        ("date_from", ">=", date_start),("date_to","<=",date_stop)])
        if draft_payslip_ids:
            raise osv.except_osv(_(u'Nominas en Borrador o en Espera de Verificacion!'),
            _(u"Asegúrese que todas las nominas de este lote esten validadas."))
        '''

        #payslip_ids = hr_payslip_obj.search(cr, uid, [("state", "in", ["done"]),
        # ("date_from", ">=", date_start),("date_to","<=",date_stop)])

        domain_filters = []

        if wizard.period_id:
            domain_filters.append(("date_start", ">=", date_from))
            domain_filters.append(("date_end", "<=", date_to))

        payslip_run_ids = hr_payslip_run_obj.search(cr, uid, domain_filters)
        payslip_run = hr_payslip_run_obj.browse(cr, uid, payslip_run_ids)

        if not payslip_run_ids:
                raise osv.except_osv(_(u'No existen nominas registradas!'),
                                     _(u"Por favor seleccione otro periodo."))

        payslip_ids = hr_payslip_obj.search(cr, uid, [('payslip_run_id', 'in', payslip_run_ids)])
        payslips = hr_payslip_obj.browse(cr, uid, payslip_ids)

        key_output = set()
        for key in payslip_run:
            key_output.add(key.clave_nomina)

        for line in key_output:

            #print str(line)
            payslip_ids = hr_payslip_obj.search(cr, uid, [('payslip_run_id', 'in', payslip_run_ids),
                                                          ('clave_nomina', '=', str(line))])
            payslips = hr_payslip_obj.browse(cr, uid, payslip_ids)

            clave_nomina = str(line)

            #Bien desde aqui
            output = set()
            for line in payslips:
                output.add(line.employee_id)

            sequence = 0
            line_count = 0

            for employee_id in output:
                nombres = (employee_id.names).encode("utf-8") or ''
                primer_apellido = (employee_id.first_lastname).encode("utf-8") or ''
                if not employee_id.second_lastname:
                    segundo_apellido = ''
                else:
                    segundo_apellido = (employee_id.second_lastname).encode("utf-8") or ''
                aporte_voluntario = 0.00
                rnc_ced_agent_ret = ''
                rem_ot_agent = 0.00
                ing_exent_periodo = 0.00
                saldo_favor_periodo = 0.00
                salario_infotep = 0.00
                tipo_ingreso = '0001'
                gross = 0.00

                basic = 0.00
                overtime = 0.00
                holidays = 0.00
                comisions = 0.00
                allowance = 0.00

                if not employee_id.birthday:
                    fecha_nacimiento = ''
                else:

                    fecha_nacimiento = employee_id.birthday.split("-") or ''
                    year = fecha_nacimiento[0]
                    month = fecha_nacimiento[1]
                    day = fecha_nacimiento[2]
                    fecha_nacimiento = day + month + year

                    #fecha_nacimiento = employee_id.birthday.strftime("%d%m%Y")
                                           #replace(u"-", u"") or False

                if not employee_id.gender:
                    raise osv.except_osv(_(u'Genero no definido!'), _(u"El siguiente empleado no tiene genero"
                                                                      u" definido (Masculino / Femenino ), favor "
                                                                      u"corrregir antes de continuar: %s"
                                                                      % employee_id.name))
                elif employee_id.gender == 'male':
                    sexo = 'M'
                elif employee_id.gender == 'female':
                    sexo = 'F'
                else:
                    sexo = ''

                if not employee_id.identification_id and not employee_id.passport_id and not employee_id.nss_id:
                    raise osv.except_osv(_(u'Cédula / Pasaporte / NSS !No encontrado!'),
                                         _(u"El siguiente empleado no posee un No. de Cedula, Pasaporte o NSS "
                                           u"registrado, favor corregir antes de continuar: %s"
                                           % employee_id.name))
                elif not employee_id.identification_id and employee_id.passport_id:
                    numero_doc = employee_id.passport_id
                    tipo_doc = 'P'
                elif employee_id.identification_id:
                    if (employee_id.identification_id and not
                            len("".join(employee_id.identification_id).strip()) in [11, 13]):
                        raise osv.except_osv(_(u'Cédula Incorrecta'), _(u"Verifique el No. de Identificacion "
                                                                        u"de este empleado: %s" % employee_id.name))
                    numero_doc = "".join(employee_id.identification_id).strip()
                    tipo_doc = 'C'
                else:
                    numero_doc = ''
                    tipo_doc = 'N'

                #Salario ISR y Salario INFOTEP
                slip_basic_ids = hr_payslip_line_obj.search(cr, uid, [("slip_id", "in", payslip_ids),
                    ('employee_id', '=', employee_id.id), ("code","=","BASIC"), ("amount",">",0)])
                for slip_basic_line in hr_payslip_line_obj.browse(cr, uid, slip_basic_ids):
                    basic += slip_basic_line.amount
                    #salario_isr += slip_basic_line.amount
                    salario_infotep += slip_basic_line.amount

                slip_gross_ids = hr_payslip_line_obj.search(cr, uid, [("slip_id", "in", payslip_ids),
                    ('employee_id', '=', employee_id.id), ("code","=","GROSS"), ("amount",">",0)])
                for slip_gross_line in hr_payslip_line_obj.browse(cr, uid, slip_gross_ids):
                    gross += slip_gross_line.amount

                slip_allowance_ids = hr_payslip_line_obj.search(cr, uid, [("slip_id", "in", payslip_ids),
                    ('employee_id', '=', employee_id.id), ("code","=","ALW"), ("amount",">",0)])
                for slip_allowance_line in hr_payslip_line_obj.browse(cr, uid, slip_allowance_ids):
                    allowance += slip_allowance_line.amount

                overtime_codes = ['HE','HED1','HED2','HED3','HEN1']
                slip_overtime_ids = hr_payslip_line_obj.search(cr, uid, [("slip_id", "in", payslip_ids),
                    ('employee_id', '=', employee_id.id), ("code","in",overtime_codes), ("amount",">",0)])
                for slip_overtime_line in hr_payslip_line_obj.browse(cr, uid, slip_overtime_ids):
                    overtime += slip_overtime_line.amount

                holidays_codes = ['VAC1','VAC2','VAC3']
                slip_holidays_ids = hr_payslip_line_obj.search(cr, uid, [("slip_id", "in", payslip_ids),
                    ('employee_id', '=', employee_id.id), ("code","in",holidays_codes), ("amount",">",0)])
                for slip_holidays_line in hr_payslip_line_obj.browse(cr, uid, slip_holidays_ids):
                    holidays += slip_holidays_line.amount

                tss_amount = 0.00
                slip_tss_ids = hr_payslip_line_obj.search(cr, uid, [("slip_id", "in", payslip_ids),
                    ('employee_id', '=', employee_id.id), ("category_id.code","=",'RETRIBD'), ("amount",">",0)])
                for slip_tss_line in hr_payslip_line_obj.browse(cr, uid, slip_tss_ids):
                    tss_amount += slip_tss_line.amount

                salario_cotizable = (basic + comisions + holidays)
                salario_isr = (basic - tss_amount) + overtime
                otras_remuneraciones = (overtime + holidays + allowance + comisions)

                #print clave_nomina, nombres, primer_apellido, segundo_apellido, sexo, numero_doc, \
                #    tipo_doc, fecha_nacimiento, gross, overtime, salario_cotizable, otras_remuneraciones

                tipo_registro = 'D'

                values = {
                    u'TIPO_REGISTRO': tipo_registro,
                    u'CLAVE_NOMINA': clave_nomina.zfill(4),
                    u'NUMERO_DOC': numero_doc.replace("-", ""),
                    u'NOMBRES': nombres.upper(),
                    u'PRIMER_APELLIDO': primer_apellido.upper(),
                    u'SEGUNDO_APELLIDO': segundo_apellido.upper(),
                    u'SEXO': sexo,
                    u'TIPO_DOCUMENTO': tipo_doc,
                    u'FECHA_NAC': fecha_nacimiento,
                    u'SALARIO_COT': abs(salario_cotizable),
                    u'APORTE_VOL': abs(aporte_voluntario),
                    u'SALARIO_ISR': abs(salario_isr),
                    u'OTRAS_REM': abs(otras_remuneraciones),
                    u'RNC_CED_AGENT_RET': rnc_ced_agent_ret,
                    u'REM_OT_AGENT': abs(rem_ot_agent),
                    u'ING_EXENT_PERIODO': abs(ing_exent_periodo),
                    u'SALDO_FAVOR_PERIODO': abs(saldo_favor_periodo),
                    u'SALARIO_INFOTEP': abs(salario_infotep),
                    u'TIPO_INGRESO': tipo_ingreso,
                    u'tss_report_id': tss_report_id,
                }

                sequence += 1
                line_count += 1

                tss_report_line_obj.create(cr, uid, values, context=context)

        self.action_generate_txt(cr, uid, tss_report_id, context=context)

        return True

    def action_generate_txt(self, cr, uid, ids, context=None):
        path = '/tmp/autodeterminacion_tss.txt'
        f = open(path,'w')

        #Report header
        header_obj = self.pool.get('tss.report')
        header = header_obj.browse(cr, uid, ids, context=context)

        if not header.company_id.vat:
            raise osv.except_osv(_(u'Advertencia!'), _(u"Debe configurar el RNC de la empresa!"))

        tipo_registro = str('E')
        document_header = str(header.company_id.vat.replace('-', '').rjust(11))
        proceso = str(header.tipo_de_archivo)
        period_month = header.period_id.name[:2]
        period_year = header.period_id.name[-4:]
        period = str(period_month + period_year)
        header_str = tipo_registro + proceso + document_header + period

        f.write(header_str + '\n')

        # Report Detail Lines
        for line in header.tss_report_line_ids:
            tipo_registro = str(line.TIPO_REGISTRO)
            clave_nomina = str(line.CLAVE_NOMINA).zfill(4)
            numero_doc = str(line.NUMERO_DOC).ljust(25, ' ')
            nombres = str((line.NOMBRES).encode("utf-8")).ljust(50, ' ')
            primer_apellido = str((line.PRIMER_APELLIDO).encode("utf-8")).ljust(40, ' ')
            segundo_apellido = str((line.SEGUNDO_APELLIDO).encode("utf-8")).ljust(40, ' ')
            sexo = str(line.SEXO).ljust(1,' ')
            tipo_documento = str(line.TIPO_DOCUMENTO).ljust(1,' ')
            fecha_nac = str(line.FECHA_NAC).ljust(8,' ')
            salario_cot = str('%.2f' % line.SALARIO_COT).zfill(16)
            aporte_vol = str('%.2f' % line.APORTE_VOL).zfill(16)
            salario_isr = str('%.2f' % line.SALARIO_ISR).zfill(16)
            otras_rem = str('%.2f' % line.OTRAS_REM).zfill(16)
            rnc_ced_agent_ret = str(line.RNC_CED_AGENT_RET).rjust(11)
            rem_ot_agent = str('%.2f' % line.REM_OT_AGENT).zfill(16)
            ing_exent_periodo = str('%.2f' % line.ING_EXENT_PERIODO).zfill(16)
            saldo_favor_periodo = str('%.2f' % line.SALDO_FAVOR_PERIODO).zfill(16)
            salario_infotep = str('%.2f' % line.SALARIO_INFOTEP).zfill(16)
            tipo_ingreso = str(line.TIPO_INGRESO)

            line_str = tipo_registro + clave_nomina + numero_doc + nombres + primer_apellido + segundo_apellido\
                       + sexo + tipo_documento + fecha_nac + salario_cot + aporte_vol + salario_isr + otras_rem\
                       + rnc_ced_agent_ret + rem_ot_agent + ing_exent_periodo + saldo_favor_periodo + salario_infotep + tipo_ingreso

            f.write(line_str + '\n')

        #Report foother
        footer_obj = self.pool.get('tss.report')
        footer = footer_obj.browse(cr, uid, ids, context=context)
        tipo_registro = str('S')
        numero_registro = str(footer.line_count).zfill(6)
        footer_str = tipo_registro + numero_registro
        f.write(footer_str)

        f.close()

        f = open(path,'rb')
        report = base64.b64encode(f.read())
        f.close()
        report_name = 'tss_file' + '_' + document_header +  '.txt'
        self.write(cr, uid, [ids], {'report': report, 'report_name': report_name})
        return True


class tss_report_line(osv.Model):
    _name = 'tss.report.line'

    _columns = {
        u'TIPO_REGISTRO': fields.char(u'Tipo de Registro', 1, required = True),
        u'CLAVE_NOMINA': fields.integer(u'Clave Nomina', required=True),
        u'TIPO_DOCUMENTO': fields.selection([('C', u'C'), ('N', u'N'), ('P', u'P')], size=1, string=u'Tipo Doc.', required=True),
        u'NUMERO_DOC': fields.char(u"Numero Documento", 11, required=True),
        u'NOMBRES': fields.char(u'Nombres', 128, required=True),
        u'PRIMER_APELLIDO': fields.char(u'1er. Apellido', 62, required=True),
        u'SEGUNDO_APELLIDO': fields.char(u'2do. Apellido', 62, required=False),
        u'SEXO': fields.selection([('M', u'M'), ('F', u'F'), (' ', u' ')], size=1, string=u'Sexo', required=False),
        u'FECHA_NAC': fields.char(u"Fecha Nacimiento", 8, required=False),
        u'SALARIO_COT': fields.float(u'Salario Cotizable', required=True),
        u'APORTE_VOL': fields.float(u'Aporte Voluntario', required=False),
        u'SALARIO_ISR': fields.float(u'Salario ISR', required=False),
        u'OTRAS_REM': fields.float(u'Otras Remuneraciones', required=False),
        u'RNC_CED_AGENT_RET': fields.char(u"RNC/Ced. Agent. Reten.", 11, required=False),
        u'REM_OT_AGENT': fields.float(u'Remuneracion Otros Agentes', required=False),
        u'ING_EXENT_PERIODO': fields.float(u'Ingresos Exentos del Periodo', required=False),
        u'SALDO_FAVOR_PERIODO': fields.float(u'Saldo a Favor del Periodo', required=False),
        u'SALARIO_INFOTEP': fields.float(u'Salario Infotep', required=False),
        u'TIPO_INGRESO': fields.selection([('0001', u'Normal'),
                                            ('0002', u'Trabajador Ocasional (no fijo'),
                                            ('0003', u'Asalariado por hora o labora tiempo parcial'),
                                            ('0004',u'No laboro mes completo por razones varias'),
                                            ('0005',u'Salario prorrateado semanal/bisemanal'),
                                            ('0006',u'Pensionado antes de la Ley 87-01'),
                                            ('0007',u'Exento por Ley de pago al SDSS')], size=4, string=u'Tipo Ingreso', required=False),
        u'tss_report_id': fields.many2one('tss.report')
    }