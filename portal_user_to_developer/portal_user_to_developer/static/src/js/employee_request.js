
odoo.define('portal_user_to_developer.employee_requests',function(require){
    'use strict';
    var publicWidget = require('web.public.widget');
    var rpc = require('web.rpc');
    var session = require('web.session');
    publicWidget.registry.employee_requests = publicWidget.Widget.extend({
        selector: ".employee_requests",
//        template: 'portal_time_off_details',
         events: {
                'change #request_type':'change_request_type',
        },

        init: function() {
        this._super.apply(this, arguments);
        this.isMobile = true;

        },

        willStart: function(){
        var self = this;
        console.log('willStartwillStartwillStart')
        return this._super()

        },

        change_request_type :function(events){
        var option = $(events.target).val();
            console.log(option);
            console.log(events.target);
            if (option=='family_status'){
                $('.family_status-fields').removeClass('d-none');
            }
            else {
                $('.family_status-fields').addClass('d-none');
            }
            if (option == 'children'){
                $('.children-fields').removeClass('d-none');
            }
            else{
                $('.children-fields').addClass('d-none');
            }
            if (option == 'working_hours'){
                var def0 =  this._rpc({
                model: "employee.request",
                method: "get_working_hour",
                }).then(function(result) {
                console.log('lllllllllllllllll', result)
                for (var c in result) {
                    self.$('#working_hours_id').append('<option value="' + result[c].id + '">' + result[c].name + '</option>')
               };
            });
                $('.working_hours-fields').removeClass('d-none');
            }
            else{
                $('.working_hours-fields').addClass('d-none');
            }
        },
    });

});

