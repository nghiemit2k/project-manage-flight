let flight_name = ""
let ticket_class_name = ""
let quantity = 0

function init(){
    flight_name = document.getElementById("flight").value
    ticket_class_name = document.getElementById("ticket_class").value
    quantity = Number(document.getElementById("quantity").value)
}

function choose(obj){
    if (obj.id === "quantity"){
        if (Number(obj.value) <= 0){
            alert("Vui lòng nhập số lượng vé lớn hơn 0");
            obj.value = "0";
        }
        else
            quantity = Number(obj.value);
    } else if (obj.id.includes("ticket_class"))
        ticket_class_name = document.getElementById(obj.id).value;
    else
        flight_name = document.getElementById(obj.id).value

    if (quantity > 0 && ticket_class_name !== "" && flight_name !== ""){
            fetch('/api/book_ticket', {
                method: "POST",
                body: JSON.stringify({
                    "flight_name": flight_name,
                    "ticket_class_name": ticket_class_name,
                    "quantity": quantity
                }),
                headers: {
                    'Content-Type': 'application/json'
                }
            }).then(res => res.json()).then(data => {
                location.reload();
            })
        }
}

function pay(){
    if (confirm("Bạn chắc chắn muốn thanh toán") === true){
        fetch("/api/pay", {
         method: "post",
         body: JSON.stringify({
            "price": Number(document.getElementById("price").innerText) - Number(document.getElementById("discount").innerText)
         }),
         headers: {
            'Content-Type': 'application/json'
         }
        }).then(res => res.json()).then(data => {
            if (data.status === 200){
                alert("Thanh toán thành công");
                window.location = "/";
            }
            else
                alert(data.err_msg);
        })
    }
}