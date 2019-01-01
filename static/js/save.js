// vars
var config_file = null
var games = {
    "ADA": "Pokemon Diamond",
    "APA": "Pokemon Pearl",
    "CPU": "Pokemon Platinum",
    "IPK": "Pokemon Heart Gold",
    "IPG": "Pokemon Soul Silver",
    "IRB": "Pokemon Black",
    "IRA": "Pokemon White",
    "IRE": "Pokemon Black 2",
    "IRD": "Pokemon White 2"
}

var regions = {
    "E": "USA",
    "S": "Spain",
    "K": "Korea",
    "J": "Japan",
    "I": "Italy",
    "D": "Germany",
    "F": "France",
    "O": "Europe"
}

var existing = []

// functions

function validateConfig(file){
    // First try to convert to json
    try{
        config_file = JSON.parse(file)
    } catch(e){
        return false
    }
    // check if the config file ha the extraSaves key
    if(!config_file.hasOwnProperty("extraSaves")){
        return false
    }
    return true
}

function loadExtraSavesData(){
    document.getElementById("config_file").style.display = "None"
    document.getElementById("saves_div").style.display = "Block"
    document.getElementById("add-new").addEventListener("click", ngModalLoad)
    document.getElementById("add-game").addEventListener("click", addNewGame)
    game_id = null
    game_name = null
    game_region = null
    var table = document.getElementById("saves_table")
    for(var game in config_file.extraSaves){

        if (games[game.substring(0, 3)] != undefined){
            game_id = game
            game_name = games[game.substring(0, 3)]
            game_region = regions[game.substring(3, 4)]
            // add the new row
            let new_row = table.insertRow(-1)
            let game_id_cell = new_row.insertCell(0)
            let game_name_cell = new_row.insertCell(1)
            let game_region_cell = new_row.insertCell(2)
            let folders_cell = new_row.insertCell(3)
            let files_cell = new_row.insertCell(4)
            // add the data
            game_id_cell.innerHTML = game_id
            game_name_cell.innerHTML = game_name
            game_region_cell.innerHTML = game_region
            for(folder in config_file.extraSaves[game_id].folders){
                folders_cell.innerHTML += "<div id='"+ game_id +"-folder-"+ folder +"'>" + config_file.extraSaves[game_id].folders[folder] + "</div>"
            }
            for(file in config_file.extraSaves[game_id].files){
                files_cell.innerHTML += "<div id='"+ game_id +"-file-"+ file +"'>" + config_file.extraSaves[game_id].files[file] + "</div>"
            }
            existing.push(game_id)
        } else{
            console.log("Couldn't match the following game id: " + game)
        }
    }
}

// ngModalLoad handles loading the add new game modal
function ngModalLoad(){
    // first clear the selection list
    let game_select = document.getElementById('games-select')
    let game_region_select = document.getElementById('game-region-select')
    while(game_select.firstChild){
        game_select.removeChild(game_select.firstChild)
    }
    while(game_region_select.firstChild){
        game_region_select.removeChild(game_region_select.firstChild)
    }
    // Then append to them
    for(id in games){
        let opt = document.createElement('option')
        opt.value = id
        opt.innerHTML = games[id]
        game_select.appendChild(opt)
    }
    for(region in regions){
        let opt = document.createElement('option')
        opt.value = region
        opt.innerHTML = regions[region]
        game_region_select.appendChild(opt)
    }
    // Then clear the text inputs
    document.getElementById('save-folders').value = ''
    document.getElementById('save-files').value = ''
}


function addNewGame(){
    // First let's combine the region and game_id to see if the game is already in our saves list
    let game_select = document.getElementById('games-select')
    let game_region_select = document.getElementById('game-region-select')
    let new_game_id = game_select.options[game_select.selectedIndex].value + game_region_select.options[game_region_select.selectedIndex].value
    if (existing.indexOf(new_game_id) > -1){
        alert("Game is already in your configuration file!")
        return
    }
}

// Init stuff
document.getElementById("config_file").addEventListener("change", function(){
        var reader = new FileReader();
        reader.onload = function () {
            if (validateConfig(reader.result)) {
                loadExtraSavesData()
            } else {
                alert("Invalid config file!")
            }
    };
    reader.readAsBinaryString(this.files[0])
})