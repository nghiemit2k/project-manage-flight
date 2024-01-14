let flight_name = ""
let ticket_class_name = ""

function init(){
    flight_name = document.getElementById("flight").value
    ticket_class_name = document.getElementById("ticket_class").value
}

function choose(obj){
    if (obj.id.includes("ticket_class"))
        ticket_class_name = document.getElementById(obj.id).value;
    else
        flight_name = document.getElementById(obj.id).value

    if (ticket_class_name !== "" && flight_name !== ""){
            fetch('/api/sell_ticket', {
                method: "POST",
                body: JSON.stringify({
                    "flight_name": flight_name,
                    "ticket_class_name": ticket_class_name
                }),
                headers: {
                    'Content-Type': 'application/json'
                }
            }).then(res => res.json()).then(data => {
                location.reload();
            })
        }
}

function printTicket(){
    if (confirm("Bạn chắc chắn với các thông tin trên") === true){
        fetch("/api/print_ticket", {
             method: "post",
             body: JSON.stringify({
                "price": Number(document.getElementById("price").innerText)
             }),
             headers: {
                'Content-Type': 'application/json'
             }
        }).then(res => res.json()).then(data => {
            if (data.status === 200){
                alert("Xuất vé thành công");
                window.location = "/";
            }
            else
                alert(data.err_msg);
        })
    }
}