import RpcClient from './json_rpc2.js';

class Store{
    constructor(){
        var that = this;
        this._mutations = {
            set_reflect(value){
                that.reflect = value
                that.output(value)
            },
            set_user(value){
                that.user = value
            },
            set_connected(value){
                that.connected = value
            },
            set_status(value){
                that.status = value
            },
            set_broadcast(value){
                that.broadcast = value
            }
        }
    }
    output(data){
       var parent = document.getElementById('output');
       var child = document.createElement("pre");
       child.innerHTML=JSON.stringify(data, null, 4);
       parent.insertBefore(child, parent.firstChild);
    }
    commit(action, value){
        if(action == "set_reflect"){
            this._mutations.set_reflect(value)
        } else {
            this.output(value)
        }
    }
}

var app = new RpcClient(new Store(), "/rpc");

function do_add(target){
    app.call("add",[
            parseFloat(document.forms[0].a.value),
            parseFloat(document.forms[0].b.value)
        ]).then(function(response){
            var result = document.getElementById("add_result");
            result.innerHTML = response;
        })
    return false;
}

function do_service(action){
    var service_name = document.forms[1].service_name.value
    if(action == "Start"){
        app.call("run_service", [service_name])
    } else {
        app.call("stop_service", [service_name])
    }
    return false;
}

window.app = app;
window.do_add = do_add;
window.do_service = do_service
