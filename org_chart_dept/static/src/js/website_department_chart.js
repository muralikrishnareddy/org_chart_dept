function openerp_chart(instance) {

    var module = instance.org_chart_dept;
    var _t     = instance.web._t;
    var QWeb   = instance.web.qweb;
    

module.deptchartWidget = instance.web.Widget.extend({
        template: 'deptchartWidget',
        events: {
        },
        init: function(parent, params){
            this._super(parent,params);
            var self = this;
            self.companies = [];
            self.income_details = [];
            self.expense_details = [];   
            },
        
        start: function(){
            window.document.title = 'Department Hierarchy - Odoo';   
            this._super();
            var self = this;
            this.title="Department Hierarchy";
            $('.js_pick_quit').click(function(){ 
            		return new instance.web.Model("ir.model.data").get_func("search_read")([['name', '=', 'open_view_employee_list_my']], ['res_id']).pipe(function(res) {
            		window.location = '/web#action=' + res[0]['res_id'];
                	}); 
                	});	    	
            var deferred_promises = [];  
            return $.when.apply($, deferred_promises).then(function(){
                stopsplash(100);
        	self.$(".oe_loading").hide();
        	self.get_data();           	
                });
                
        }, 
        get_data: function(){
        
        startsplash();
        var self = this;
        self.$('#maintd').empty();        
        self.lines = "";
        self.model_dept = new instance.web.Model("hr.department");
        self.model_emp = new instance.web.Model("hr.employee");     
        params = ([[]], []);                   
            
                
        self.model_dept
                    .call("department_employees", (params))
                    .then(function(results) {
                        _(results).each(function (item) {
                        
                        content = '<ul><li id='+item['id']+'><a><table class="datatbl"><tr>\
			              <td>\
				          <div class="dept-div-class"><table>\
			                      <tr><td class="dept" colspan="3" '+(item['job_title']=='Department'?'style="background-color:#cc0099"':'style="background-color:#9933ff"')+'>'+item['name']+'</td></tr>\
			                      <tr ><td rowspan="3" width="25%"><img width="64px" height="64px" class="oe_employee_picture" src="'+item['image']+'"/></td></tr>\
			                     <tr><td><a style="color:blue;" href="mailto:'+item['work_email']+'">'+item['work_email']+'</a></td></tr>\
							     <tr><td>'+item['job_title']+'</td></tr>\
			                  </table></div>\
			             </td>\
		                  </tr></table></a></li></ul>';
		                  console.log(self.$('#'+(item['parent_id']).toString()+''));
                        if(self.$('#'+(item['parent_id']).toString()+'').html()!=undefined){
                          self.$('#'+(item['parent_id']).toString()+'').append(content);
                        }
                        else
                        {
                          self.$('#maintd').append(content);
                        }
                    
                    });
                    $( '.tree li' ).each( function() {
						if( $( this ).children( 'ul' ).length > 0 ) {
								$( this ).addClass( 'parent' );
						}
				});
				
				$( '.tree li.parent > a' ).click( function( ) {
						$( this ).parent().toggleClass( 'active' );
						$( this ).parent().children( 'ul' ).slideToggle( 'fast' );
				});
				
				$( '.tree li' ).each( function() {
						$( this ).toggleClass( 'active' );
						$( this ).children( 'ul' ).slideToggle( 'fast' );
				});				
                 stopsplash(500);
                 });
                 
                 
		 
        },
            
    });
    openerp.web.client_actions.add('org_chart_dept.depthierarchy', 'instance.org_chart_dept.deptchartWidget');
}


openerp.org_chart_dept = function(openerp) {
    openerp.org_chart_dept = openerp.org_chart_dept || {};
    openerp_chart(openerp);
}
