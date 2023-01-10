
odoo.define('portal_user_to_developer.portal_time_off',function(require){
    'use strict';
    var publicWidget = require('web.public.widget');
    var rpc = require('web.rpc');
    var session = require('web.session');
    publicWidget.registry.Aircraft_listing = publicWidget.Widget.extend({
        selector: ".ddd",
//        template: 'portal_time_off_details',
         events: {
                'click #button-40':'onclick_time_off_type',
        },


        willStart: function(){
        var self = this;
        console.log('willStartwillStartwillStart')
        return this._super()
        .then(function() {
            const description = document.getElementById('description');
            const myfile = document.getElementById('myfile');
            const date_from = document.getElementById('date_from');
            const date_to = document.getElementById('date_to');
            description.value = '';
            myfile.value = '';
            date_from.value = '';
            date_to.value = '';
            var def0 =  self._rpc({
                model: "time.off.type",
                method: "get_time_of_types",
            }).then(function(result) {
                console.log('lllllllllllllllll', result)
                for (var c in result[0]) {
                    var val = result[0]
                    console.log('lllllllllllllllll11', val)
                    self.$('#time_off_type').append('<option value="' + val[c].id + '">' + val[c].name + '</option>')
               };
                console.log('vals', result[1])
               Object.entries(result[1]).forEach(([key, value]) => {
                    console.log('vals', key, value)
                    if (key == 'To Submit'){
                       console.log('To SubmitTo Submit')
                       var link = "/to_submit"
                       var tag = 'Submitted'
                    }
                    if (key == 'To approve'){
                       console.log('To SubmitTo Submit')
                       var link = "/to_approve"
                       var tag = 'To approve'
                    }
                    if (key == 'Refused'){
                       console.log('To SubmitTo Submit')
                       var link = "/refused"
                       var tag = 'Refused'
                    }
                    if (key == 'Second Approval'){
                       console.log('To SubmitTo Submit')
                       var link = "/second_approval"
                       var tag = 'Second Approval'
                    }
                    if (key == 'Approved'){
                       console.log('To SubmitTo Submit')
                       var link = "/approved"
                       var tag = 'Approved'
                    }
                    self.$('.leaderboard__profiles').append('<div class="leaderboard__profile" id="' + key + '">
                    <a class="leaderboard__name" href=' + link + '>' + tag + '</a>
                    <div class="leaderboard__value">' + value + '</div>')
               });
            });
        return $.when(def0);
        });
        },

        onclick_time_off_type :function(events){
//        var user = session.uid
//        var option = $(events.target).val();
        console.log('oooooooooo');
//        const firstNameInput = document.getElementById('description');
//        firstNameInput.value = '';


//        var self = this
//            rpc.query({
//                model: "time.off.type",
//                method: "get_time_of_types",
//            }).then(function (result) {
//                console.log('result', result)
//                for (var c in result) {
//                    console.log('resultc', result[c].name)
//                    $('#time_off_type').append('<option value="' + result[c].id + '">' + result[c].name + '</option>')
//               };
//            });
        },
    });

});

