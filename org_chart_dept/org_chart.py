# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import timedelta,date
from operator import itemgetter
import time
import copy

import openerp
from openerp import SUPERUSER_ID, api
from openerp import tools
from openerp.osv import fields, osv, expression
from openerp.tools.translate import _
from openerp.tools.float_utils import float_round as round

import openerp.addons.decimal_precision as dp

_logger = logging.getLogger(__name__)

class hr_department(osv.osv):
    _inherit = "hr.department"  
    sequence=1000    
    
    def get_employees_data(self, cr, uid, emp_id, data=[], context=None):
        emp_obj = self.pool.get('hr.employee')
        for emp in emp_obj.browse(cr, uid, [emp_id],context=context):             
            employee = {}
            employee['id'] = str(emp.id)+'_emp'
            employee['sequence'] = self.sequence
            employee['oid'] = emp.id
            employee['name'] = emp.name
            employee['parent_id'] = emp.parent_id and str(emp.parent_id.id)+'_emp' or emp.parent_id.id
            employee['image'] = '/web/binary/image?model=hr.employee&amp;field=image_small&amp;id='+str(emp.id)+''
	    employee['work_email'] = emp.work_email and emp.work_email or ''
	    employee['job_title'] = emp.job_id and emp.job_id.name or ''
	    chld = filter(lambda val: val['oid'] == emp.id, data)
            if chld:    
                chld[0]['sequence'] = self.sequence
	    else:
	        data.append(employee)
	    self.sequence-=1
	    if emp.parent_id:
	        return self.get_employees_data(cr, uid, emp.parent_id.id, data, context=context)        	     
        return data
    
        
    def department_employees(self, cr, uid, context=None):
            
        finals = []   
        for dept in self.browse(cr, uid, self.search(cr, uid, [],context=context),context=context):
            department = {}
            department['id'] = dept.id
            department['name'] = dept.name
            department['parent_id'] = dept.parent_id and dept.parent_id.id or dept.parent_id.id
            department['image'] = '/org_chart_dept/static/src/img/dept1.jpeg'
            department['work_email'] = ''
            department['job_title'] = 'Department'
            finals.append(department)
            #Department Manager Details
            if dept.manager_id:
                manager = {}
                manager['id'] = str(dept.manager_id.id)+'_emp'
                manager['name'] = dept.manager_id.name
                manager['parent_id'] = dept.id
                manager['image'] = '/web/binary/image?model=hr.employee&amp;field=image_small&amp;id='+str(dept.manager_id.id)+''
                manager['work_email'] = dept.manager_id.work_email and dept.manager_id.work_email or ''
                manager['job_title'] = dept.manager_id.job_id and dept.manager_id.job_id.name or ''
                finals.append(manager)
                #Other Employees of Manager
                emp_obj = self.pool.get('hr.employee')
                empids = emp_obj.search(cr, uid, [('parent_id','=',dept.manager_id.id)],context=context)
                if empids:
                    for emp in emp_obj.browse(cr, uid, empids,context=context):             
                        employee = {}
                        employee['id'] = str(emp.id)+'_emp'
                        employee['name'] = emp.name
                        employee['parent_id'] = str(dept.manager_id.id)+'_emp'
                        employee['image'] = '/web/binary/image?model=hr.employee&amp;field=image_small&amp;id='+str(emp.id)+''
                	employee['work_email'] = emp.work_email and emp.work_email or ''
                	employee['job_title'] = emp.job_id and emp.job_id.name or ''
                        finals.append(employee) 
            #Employees 
            
                           
        emplst = []
        emp_obj = self.pool.get('hr.employee')
        emplids = emp_obj.search(cr, uid, [])
        for empl in emp_obj.browse(cr, uid, emplids, context=context):
            noids = emp_obj.search(cr, uid, [('parent_id','=',empl.id)],context=context)                
            if not noids:
                emplst = self.get_employees_data(cr, uid, empl.id, emplst, context=context)
        emplst = sorted([dict(y) for y in set(tuple(x.items()) for x in emplst)], key=lambda k: k['sequence'])
        for dt in emplst:
            chld = filter(lambda val: val['id'] == dt['id'], finals)
            if not chld:    
                finals.append(dt)
        finalst = []
        for idx,line in enumerate(finals):
            finalst.append(copy.deepcopy(line))
            index = len(finalst)
            chld = filter(lambda val: val['parent_id'] == line['id'], finals)
            for ch in chld:
                finalst.insert(index,copy.deepcopy(ch))
        return finals 
        
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:





















