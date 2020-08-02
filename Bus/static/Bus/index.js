document.addEventListener("DOMContentLoaded",function () {
    var el = document.querySelector('#routes');
    if(el){
        el.addEventListener('click', () => dropdownCheck(event));
    }
});

function dropdownCheck(event){
    event.preventDefault();

    var select1 = document.getElementById('from');
    var select2 = document.getElementById('to');
    var selected1 = [...select1.options]
                        .filter(option => option.selected)
                        .map(option => option.value);
    var selected2 = [...select2.options]
                        .filter(option => option.selected)
                        .map(option => option.value);

    console.log(`${selected1}`);
    console.log(`${selected2}`);
    if (`${selected1}` != `${selected2}`) {
        displayDetails(`${selected1}` ,`${selected2}`);
    } else {
        document.querySelector("#error").innerHTML = `<div class="alert alert-danger" role="alert"> Invalid Destination. </div>`;
    }
}


function displayDetails(from,to){
    var d = new Date(); var month = d.getMonth();var date = d.getDate();
    if(`${month}` < 10 && `${date}` < 10){
        d = d.getFullYear()+'-0'+(d.getMonth()+1)+'-0'+d.getDate();
    }
    else if(`${date}` < 10){
        d = d.getFullYear()+'-'+(d.getMonth()+1)+'-0'+d.getDate();
    }
    else if(`${month}` < 10){
        d = d.getFullYear()+'-0'+(d.getMonth()+1)+'-'+d.getDate();
    } else {
        d = d.getFullYear()+'-'+(d.getMonth()+1)+'-'+d.getDate();
    }
    console.log(d);
    const display = document.querySelector("#date");
    display.innerHTML = `<div>
        <label class="label" for="from" style="color: aliceblue;">Select Date:</label>
        <input type="date" id="date-drop">
        <input type="submit" value="Next" id="date-submit" class="btn btn-warning" style="background-color: darkorange; color: white;" >
    </div><hr>`;

    /* Event listener for Date */
    document.querySelector('#date-submit').addEventListener('click', () =>{
        var select = document.getElementById('date-drop');
        var date = select.value;
        
        if (date < d){
            alert("Please select date from future or present!");
        } else {
            fetch(`/routes/${from}/${to}`)
                .then(response => response.json())
                .then(timing =>{
                    timing.forEach(element => {
                        seats = element.total_seats;
                        price = element.price;
                        departure = element.departure;
                        arival = element.arival;
                        var item = document.createElement("div");
                        item.className = `card`;
                        item.innerHTML = `<div class="card-text"> <p><strong>From:</strong> ${from}</p>
                        <p><strong>To:</strong> ${to}</p>
                        <p><strong>Departure:</strong> ${departure}</p>
                        <p><strong>Arival:</strong> ${arival}</p>
                        <p><strong>Date:</strong> ${date}</p>
                        <p><strong>Price:</strong> $${price}</p>
                        <p><strong>Seats:</strong style = "color:red;"> ${seats}</p>
                        <p><strong>Number of seats: </strong><input type="text" id="seats-${element.id}"></p>
                        <input type="submit" value="Book Now" id="book" class="btn btn-warning" style="background-color: darkorange; color: white;" >
                        </div>`;
                        console.log(`${element.id}`);
                        document.querySelector("#timing").appendChild(item);
                        item.addEventListener('click', () =>{
                            seat = document.getElementById(`seats-${element.id}`).value;
                            if(seats - seat <= 0 || seat == 0){
                                alert("Invalid Number of seats");
                            } else{
                                console.log(`${element.id}`);
                                bookNow(`${from}`,`${to}`,`${element.id}`,`${seat}`,`${date}`);
                            }
                        })
                    })
                })

        }
    })
}


function bookNow(from,to,id,seats,date){
    alert(id);
    fetch("/booking",{
        method: "POST",
        body: JSON.stringify({
            _from: from,
            to: to,
            _id: id,
            seats: seats,
            date: date,
        }),
    })
    .then((response) => response.json())
    .then((result) =>{
        if (result.status == 200){
            var pop_up = document.createElement("div");
            pop_up.className = `hover_bkgr_fricc`;
            pop_up.innerHTML = `<div class="helper">
            <div class="popupCloseButton">&times;</div>
                <h2> Ticket it booked. </h2>
            </div>`;
            document.querySelector("#error").innerHTML = `<div class="alert alert-success" role="alert">${result.message}</div>`;
        } else{
            document.querySelector("#error").innerHTML = `<div class="alert alert-danger" role="alert">${result.error}</div>`;
        }
    });
}
