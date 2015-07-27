# -*- coding: utf-8 -*-
##############################################################################
#
#    HLVSolution, Open Source Management Solution
#
##############################################################################
import time
from openerp.report import report_sxw
from openerp import pooler
from openerp.osv import osv
from datetime import datetime
from openerp.tools.translate import _
import random
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT = "%Y-%m-%d"

from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, float_compare
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
# from green_erp_pharma_report.report import amount_to_text_vn
class Parser(report_sxw.rml_parse):
        
    def __init__(self, cr, uid, name, context):
        super(Parser, self).__init__(cr, uid, name, context=context)
        pool = pooler.get_pool(self.cr.dbname)
        self.localcontext.update({
            'get_partner_address':self.get_partner_address,
            'get_so_hd':self.get_so_hd,
            'get_ngay_hd':self.get_ngay_hd,
            'get_ngay_hethan':self.get_ngay_hethan,
        })
        
    
    def get_partner_address(self, picking):
        address = ''
        if picking.partner_id:
            address += picking.partner_id.street or ''
            address += picking.partner_id.state_id and ', ' + picking.partner_id.state_id.name or ''
            address += picking.partner_id.country_id and ', ' + picking.partner_id.country_id.name or ''
        return address
    
    def get_so_hd(self, picking):
        invoice_ids = self.pool.get('account.invoice').search(self.cr,self.uid,[('name','=',picking.name)])
        if invoice_ids:
            invoice = self.pool.get('account.invoice').browse(self.cr,self.uid,invoice_ids[0])
            so_hd = invoice.reference_number
        else:
            so_hd = ''
        return so_hd
    
    def get_ngay_hd(self, picking):
        invoice_ids = self.pool.get('account.invoice').search(self.cr,self.uid,[('name','=',picking.name)])
        if invoice_ids:
            invoice = self.pool.get('account.invoice').browse(self.cr,self.uid,invoice_ids[0])
            if invoice.date_invoice:
                ngay_hd = datetime.strptime(invoice.date_invoice, DATE_FORMAT)
                ngay_hd = ngay_hd.strftime('%d-%m-%Y')
            else:
                ngay_hd = ''
        else:
            ngay_hd = ''
        return ngay_hd
    
    def get_ngay_hethan(self, prodlot):
        if prodlot and prodlot.life_date:
            ngay_hh = datetime.strptime(prodlot.life_date, DATETIME_FORMAT)
            ngay_hh = ngay_hh.strftime('%d-%m-%Y')
        else:
            ngay_hh = ''
        return ngay_hh
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: