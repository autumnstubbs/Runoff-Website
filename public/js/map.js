/*controls map functionality, over functionality, statistics box functionality*/

/* make initial image overlay (day 0) */ 

// var imageUrl = 'https://CISC475-498-EOF-Runoff-Project.github.io/images/Event0_projected.png';
var imageUrl = 'C:/Users/oodle/OneDrive/Documents/INTERNSHIP/CISC475-498-EOF-Runoff-Project.github.io/new_images_4326/new_colors/Event0_projected.png'
window.imageOverlay = L.imageOverlay(
    imageUrl,
    // [[51.2 + 3.6 + 0.9, -100.0 - 1.9 - 0.5], [35.0 - 5.5, -70.0 + 4.5]],
    // [[55.7, -102.4], [29.5, -65.5]]
    [[61.5, -101.95], [24.05, -64.5]],
    // [[37.0447, -97.6176], [48.7132, -68.9932]],
    {
        opacity: 0.5,
        interactive: true
    });

/* build map base layer with map data from mapbox */

var baseLayer = L.tileLayer('https://api.maptiler.com/maps/basic-4326/256/{z}/{x}/{y}@2x.png?key=WKrfAQnQ31aoyi9nLmNr', {
        // maptiler map https://api.maptiler.com/maps/basic-4326/256/{z}/{x}/{y}.png?key=WKrfAQnQ31aoyi9nLmNr
        // old map for 3857:'https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoicmRlYW4iLCJhIjoiY2t1eWl3dnA2NzNpNTJwbzNvcHRxejdxaCJ9.tIGjuwey9icme7TC-y-U9g'      
        // attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
          attribution: 'Map data &copy; <a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a>',
          maxZoom: 30,
          id: 'mapbox/streets-v11',
          tileSize: 512,
          // tileSize: 256, // added
          zoomOffset: -1,
          origin: [-180, 90],
          // accessToken: 'pk.eyJ1IjoicmRlYW4iLCJhIjoiY2t1eWl3dnA2NzNpNTJwbzNvcHRxejdxaCJ9.tIGjuwey9icme7TC-y-U9g'
        });

/* initialize map object, add in base and image layers */
var crs = L.CRS.EPSG4326
// var crs = L.CRS.EPSG3857
var mymap = new L.Map('mapid', {
  // center: new L.LatLng(45.00, -87.00),
  center: new L.LatLng(45.00, -84.00),
  zoom: 2,
  minZoom: 3,
  maxZoom: 9,
  crs: crs,
  //layers: [baseLayer, imageOverlay]
  layers: [baseLayer, window.imageOverlay]
});

//mymap.setMaxBounds([
//    [52.73, -100.49],
//    [30.13, -64.72]
//]);

/* make popup object to display when map is clicked */

var popup = L.popup();

/* create helper text, disappears once map is clicked */

var statsTableHolder = document.getElementById("statsTableHolder");
var helperSpan = document.createElement('span');
helperSpan.setAttribute('style','color:white');
var helperText = document.createTextNode("Click a region on the map to get more detailed information!");
helperSpan.append(helperText);
statsTableHolder.appendChild(helperSpan);

/* function that runs when map is clicked. Adds popup + fills table with 10 days of stats */

function imagePopup(e) {
    //var e = leafletEvent.originalEvent;
    var temp_event = e.originalEvent;
    var rect = temp_event.target.getBoundingClientRect();
    var zoomedX = temp_event.clientX - rect.left; //x position within the element.
    var zoomedY = temp_event.clientY - rect.top;  //y position within the element

    const x = Math.round(zoomedX * imgWidth / rect.width);
    const y = Math.round(zoomedY * imgHeight / rect.height);

    var statsTable = document.getElementById("popupStatsTable");
  
    if (statsTable.tBodies[0].rows.length == 0) {
        statsTableHolder.removeChild(helperSpan);
    }
    
    //iterate through rows
    for(var j = 0; j < 10; j++) {
        if (statsTable.tBodies[0].rows.length < j+1) {
            statsTable.tBodies[0].insertRow(j);
        }
        //iterate through cells in row
        for (var k = 0; k < 5; k++) {
            if (statsTable.tBodies[0].rows[j].cells.length < k+1) {
                statsTable.tBodies[0].rows[j].insertCell(k);
            }
        }
    }
    
    let str = window.imageOverlay.getElement().src;
    let popupday = str.charAt(str.length - 15);
    
    for(var day = 0; day < 10; day++) {
        fillGridRow(x, y, day, popupday, e);
    }   
}


/* TODO: Change function name to updatePopups() */
/* Helper function called in slidebar.js to update popup text */

function clearpopups(newDay) {
    //mymap.closePopup();
    let statsTable = document.getElementById("popupStatsTable");
    if (statsTable.tBodies[0].rows.length > 1) {
        popup.setContent('<H6>RISK: ' + statsTable.tBodies[0].rows[newDay].cells[1].innerHTML + '</H6>');
    }
}

const imgWidth = 1600, imgHeight = 1600;
window.imageOverlay.on('click', imagePopup);


/* Fills one row of the stats box table. Done independently because js loads images async */

function fillGridRow(x, y, img_day, popupday, e) {
    
    
    var statsTable = document.getElementById("popupStatsTable");
    /*
    let imgVars = new Image();
    imgVars.src = 'https://CISC475-498-EOF-Runoff-Project.github.io/images/Event' + img_day + '_vars.png';
    imgVars.onload = function() {
        
        let tempCanvas = document.createElement('canvas');
        tempCanvas.width = imgWidth;
        tempCanvas.height = imgHeight;
        let tempCtx = tempCanvas.getContext('2d');
        
        tempCtx.clearRect(0, 0, imgWidth, imgHeight);
        tempCtx.drawImage(imgVars, 0, 0, imgWidth, imgHeight);

        let varsData = tempCtx.getImageData(x, y, imgWidth, imgHeight); 
        let accprcp = ((varsData.data[0] / 255) * 200).toFixed(2);
        let acsnom = ((varsData.data[1] / 255) * 200).toFixed(2);
        let qsnow = ((varsData.data[2] / 255) * 200).toFixed(2);
        statsTable.tBodies[0].rows[img_day].cells[2].innerHTML = accprcp;
        statsTable.tBodies[0].rows[img_day].cells[3].innerHTML = acsnom;
        statsTable.tBodies[0].rows[img_day].cells[4].innerHTML = qsnow;
        for (var iter = 2; iter < 5; iter++) {
            if (statsTable.tBodies[0].rows[img_day].cells[iter].innerHTML == 0.00) {
                statsTable.tBodies[0].rows[img_day].cells[iter].innerHTML = "--";
            }
        }
    }
    
    let imgRisk = new Image();
    imgRisk.src = 'https://CISC475-498-EOF-Runoff-Project.github.io/images/Event' + img_day + '_projected.png';
    imgRisk.onload = function() {
        
        let tempCanvas = document.createElement('canvas');
        tempCanvas.width = imgWidth;
        tempCanvas.height = imgHeight;
        let tempCtx = tempCanvas.getContext('2d');
        
        tempCtx.clearRect(0, 0, imgWidth, imgHeight);
        tempCtx.drawImage(imgRisk, 0, 0, imgWidth, imgHeight);

        let riskData = tempCtx.getImageData(x, y, imgWidth, imgHeight); 
        let riskRed = riskData.data[0];
        let riskGreen = riskData.data[1];
        let riskBlue = riskData.data[2];
        let daily_risk = "MINIMAL";
        let max_risk_color = Math.max(riskData.data[0], riskData.data[1], riskData.data[2]);
        if (riskRed == 0) {
            daily_risk = "MINIMAL";
        } else if (max_risk_color == riskRed) {
            daily_risk = "HIGH";
        } else if (max_risk_color == riskGreen) {
            daily_risk = "LOW";
        } else {
            if (riskRed > riskGreen) {
                daily_risk = "MODERATE";
            }
        }
        
        statsTable.tBodies[0].rows[img_day].cells[1].innerHTML = daily_risk;
        if (img_day == popupday) {
            popup
                .setLatLng(e.latlng)
                .setContent('<H6>RISK: ' + statsTable.tBodies[0].rows[popupday].cells[1].innerHTML + '</H6>')
                .openOn(mymap);
        }
        if (daily_risk == "MINIMAL") {
            statsTable.tBodies[0].rows[img_day].cells[1].setAttribute("style","color: #BBFFBB");
        }
        else if (daily_risk == "LOW") {
            statsTable.tBodies[0].rows[img_day].cells[1].setAttribute("style","color: #FFFFBB");
        }
        else if (daily_risk == "MODERATE") {
            statsTable.tBodies[0].rows[img_day].cells[1].setAttribute("style","color: #FFDDBB");
        }
        else {
            statsTable.tBodies[0].rows[img_day].cells[1].setAttribute("style","color: #FFBBBB");
        }
    }
    
    */
    let formatted_day = new Date();
    let date_to_show = "Today";
    if (img_day != 0) {
        formatted_day.setDate(formatted_day.getDate() + img_day);
        date_to_show = (formatted_day.getMonth()+1) + "/" + formatted_day.getDate();
    }
    statsTable.tBodies[0].rows[img_day].cells[0].innerHTML = date_to_show;

    let data_arr = get_daily_data(1, 2, 1, e)

    day1 = ['NONE', 0.0, 0.0, 0.0]
    day2 = ['NONE', 0.0, 0.0, 0.0]
    day3 = ['NONE', 0.0, 0.0, 0.0]
    day4 = ['NONE', 0.0, 0.0, 0.0]
    day5 = ['MINIMAL', 1.58, 1.116, 0.0]
    day6 = ['MINIMAL', 0.73, 0.756, 0.0]
    day7 = ['NONE', 0.0, 0.0, 0.0]
    day8 = ['HIGH', 9.57, 9.18, 0.0]
    day9 = ['MODERATE', 3.66, 3.528, 0.0]
    day10 = ['MINIMAL', 2.86, 2.52, 0.0]

    days = [day1, day2, day3, day4, day5, day6, day7, day8, day9, day10]

    /*
    for (let i = 1; i <= 10; i++) {
        for (let j = 0; j <=3; j++) {
        statsTable.tBodies[0].rows[i].cells[1].innerHTML = days[i][j];
        }
    }
    */

    statsTable.tBodies[0].rows[0].cells[1].innerHTML = day1[0];
    statsTable.tBodies[0].rows[0].cells[2].innerHTML = day1[1];
    statsTable.tBodies[0].rows[0].cells[3].innerHTML = day1[2];
    statsTable.tBodies[0].rows[0].cells[4].innerHTML = day1[3];

    statsTable.tBodies[0].rows[1].cells[1].innerHTML = day2[0];
    statsTable.tBodies[0].rows[1].cells[2].innerHTML = day2[1];
    statsTable.tBodies[0].rows[1].cells[3].innerHTML = day2[2];
    statsTable.tBodies[0].rows[1].cells[4].innerHTML = day2[3];

    statsTable.tBodies[0].rows[2].cells[1].innerHTML = day3[0];
    statsTable.tBodies[0].rows[2].cells[2].innerHTML = day3[1];
    statsTable.tBodies[0].rows[2].cells[3].innerHTML = day3[2];
    statsTable.tBodies[0].rows[2].cells[4].innerHTML = day3[3];

    statsTable.tBodies[0].rows[3].cells[1].innerHTML = day4[0];
    statsTable.tBodies[0].rows[3].cells[2].innerHTML = day4[1];
    statsTable.tBodies[0].rows[3].cells[3].innerHTML = day4[2];
    statsTable.tBodies[0].rows[3].cells[4].innerHTML = day4[3];

    statsTable.tBodies[0].rows[4].cells[1].innerHTML = day5[0];
    statsTable.tBodies[0].rows[4].cells[2].innerHTML = day5[1];
    statsTable.tBodies[0].rows[4].cells[3].innerHTML = day5[2];
    statsTable.tBodies[0].rows[4].cells[4].innerHTML = day5[3];

    statsTable.tBodies[0].rows[5].cells[1].innerHTML = day6[0];
    statsTable.tBodies[0].rows[5].cells[2].innerHTML = day6[1];
    statsTable.tBodies[0].rows[5].cells[3].innerHTML = day6[2];
    statsTable.tBodies[0].rows[5].cells[4].innerHTML = day6[3];

    statsTable.tBodies[0].rows[6].cells[1].innerHTML = day7[0];
    statsTable.tBodies[0].rows[6].cells[2].innerHTML = day7[1];
    statsTable.tBodies[0].rows[6].cells[3].innerHTML = day7[2];
    statsTable.tBodies[0].rows[6].cells[4].innerHTML = day7[3];

    statsTable.tBodies[0].rows[7].cells[1].innerHTML = day8[0];
    statsTable.tBodies[0].rows[7].cells[2].innerHTML = day8[1];
    statsTable.tBodies[0].rows[7].cells[3].innerHTML = day8[2];
    statsTable.tBodies[0].rows[7].cells[4].innerHTML = day8[3];

    statsTable.tBodies[0].rows[8].cells[1].innerHTML = day9[0];
    statsTable.tBodies[0].rows[8].cells[2].innerHTML = day9[1];
    statsTable.tBodies[0].rows[8].cells[3].innerHTML = day9[2];
    statsTable.tBodies[0].rows[8].cells[4].innerHTML = day9[3];

    statsTable.tBodies[0].rows[9].cells[1].innerHTML = day10[0];
    statsTable.tBodies[0].rows[9].cells[2].innerHTML = day10[1];
    statsTable.tBodies[0].rows[9].cells[3].innerHTML = day10[2];
    statsTable.tBodies[0].rows[9].cells[4].innerHTML = day10[3];

    
    // make sure to make it so risk is colored still!!!!!!
}

function get_date(day_number) {
    // takes in a number 0 - 9
    // and forms it into a sql date
}

// takes in lat and lon points and a day (1-10)
// returns an array in the following form [risk, rainfall, snomelt, snowfall]
function get_daily_data(lat, lon, day, e) {
    // runs python program to get info
    // return data in array form
    return [0, 1.5, 3.7, 3.0]
}

