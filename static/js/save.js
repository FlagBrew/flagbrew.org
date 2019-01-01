// vars
var config_file = null
var games = [{
    "GAME_ID": "ADAE",
    "GAME_NAME": "Pokemon Diamond",
    "GAME_REGION": "USA"
}]
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
    game_id = null
    game_name = null
    game_region = null
    var table = document.getElementById("saves_table")
    for(var game in config_file.extraSaves){
        let match = false
        for(g in games){
            if (games[g].GAME_ID == game){
                game_id = game
                game_name = games[g].GAME_NAME
                game_region = games[g].GAME_REGION
                match = true
                break
            }
        }
        if(match){
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
                folders_cell.innerHTML += config_file.extraSaves[game_id].folders[folder] + "\n"
            }
            for(file in config_file.extraSaves[game_id].files){
                files_cell.innerHTML += config_file.extraSaves[game_id].files[file] + "\n"
            }
        } else{
            console.log("Couldn't match the following game id: " + game)
        }
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