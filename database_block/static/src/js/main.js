/*  Copyright 2020 Eugene Molotov <https://it-projects.info/team/em230418>
    License MIT (https://opensource.org/licenses/MIT). */
odoo.define("database_block.main", function (require) {
    "use strict";

    var AppsMenu = require("web.AppsMenu");

    AppsMenu.include({
        start: function () {
            this._super.apply(this, arguments);

            let content = `<div class="oe_instance_register oe_instance_register_form" style="display: block;">
                            <form name="subscription" class="form-inline justify-content-center mt-4" _lpchecked="1">
                            <div class="form-group">
                                <label for="subscription_code">Subscription Code: </label>
                                <input type="text" class="form-control mx-2" name="sub_code" placeholder="Paste code here" title="Your subscription code">
                            </div>
                            <button class="btn btn-primary submit">Renew</button>
                            </form>
                        </div>`

            if (odoo.session_info.database_block_message) {
                $(".database_block_message").html(
                    odoo.session_info.database_block_message + content
                );

                if (!odoo.session_info.database_block_is_warning) {
                    $(".o_action_manager").block({
                        message: $(".block_ui.database_block_message").html(
                            odoo.session_info.database_block_message
                        ),
                    });
                    $("header").css("z-index", $.blockUI.defaults.baseZ + 20);
                }

                if (odoo.session_info.database_block_show_message_in_apps_menu) {
                    $(".dropdown-menu > .database_block_message").show();
                }
            }
        },
        events: {
            'submit form[name=subscription]': function(ev){
                ev.preventDefault();
                let self = this
                this._rpc({
                    route: `/get_dbconfig`,
                    params: {},
                }).then(function (res) {
                    console.log('response '+ JSON.stringify(res))
                    let data = JSON.parse(res)
                    console.log('response '+ data.dbuuid)

                    if (!data.dbuuid) return alert("Database UUID is not configured");
                    if (!data.license_server) return alert("License verification server is not configured");
                    self.renewSubscriptionAsync(data.dbuuid, data.license_server)

                }).guardedCatch(function (error) {
                    let msg = error.message.message
                    console.log(msg)
                    alert("Server Error!", msg)
                });

            }
        },
        renewSubscriptionAsync: function(dbuuid, server){
            let self = this
            let input = $("input[name=sub_code]")
            let btn = $("button.submit")
            let sub_code = input.val()
            if(sub_code === ''){
                return alert('Subscription code is required')
            }
    
            if(sub_code !== ''){
                let form = $("form[name=subscription]")[0];
                let formData = new FormData(form);
    
                var xmlRequest = $.ajax({
                    type: "POST",
                    url: `${server}/validate_license`,
                    data: formData,
                    processData: false,
                    contentType: false,
                    cache: false,
                    timeout: 800000,
                    beforeSend: function (req) {
                        req.setRequestHeader("dbuuid", dbuuid);
                        btn.html("<i class='fa fa-spinner fa-spin'></i>")
                        btn.disable = true
                    }
                });
    
                xmlRequest.done(function (data) {
                    console.log('Recieving response from server => '+ JSON.stringify(data))
                    const response = JSON.parse(data)
                    if(!response.valid) return alert(response.message)
                    self.updateDbExpiryAsync(response.date_to)
                    
                });
                xmlRequest.fail(function (jqXHR, textStatus) {
                    alert("Bad Request", `${textStatus}`)
                });
                xmlRequest.always(function () {
                    btn.html("Renew")
                    btn.disable = false
                })
    
            }
        },
        updateDbExpiryAsync:  function(date){
            if(date == '') return alert('Invalid expiry date')
            this._rpc({
                route: `/update_db_expiry`,
                params: {'expiry_date':  date},
            }).then(function (res) {
                console.log('response '+ JSON.stringify(res))
                let data = JSON.parse(res)
                $(".oe_instance_register_form").addClass('d-none')
                $('.database_block_message').addClass('d-none')
                if (data.status) return alert("Subscription renewed successfully!");

            }).guardedCatch(function (error) {
                let msg = error.message.message
                console.log(msg)
                alert("Server Error!", msg)
            });
        }
        
    });
});