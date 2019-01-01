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

var s = null

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
    document.getElementById("download").addEventListener("click", download)
    game_id = null
    game_name = null
    game_region = null
    var table = document.getElementById("saves_table")
    s = config_file.extraSaves
    for(var game in config_file.extraSaves){

        if (games[game.substring(0, 3)] != undefined){
            game_id = game
            game_name = games[game.substring(0, 3)]
            game_region = regions[game.substring(3, 4)]
            // add the new row
            let new_row = table.insertRow(-1)
            new_row.id=game_id
            let game_id_cell = new_row.insertCell(0)
            let game_name_cell = new_row.insertCell(1)
            let game_region_cell = new_row.insertCell(2)
            let folders_cell = new_row.insertCell(3)
            let files_cell = new_row.insertCell(4)
            let edit_cell = new_row.insertCell(5)
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
            edit_cell.innerHTML = "<i style='cursor: pointer;' class='far fa-pencil'></i>"
            edit_cell.addEventListener("click", function(){
                egModalLoad(game_id)
            })
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

// egModalLoad handles the loading of the edit game modal
function egModalLoad(game){
    // get the table row
    row = document.getElementById(game)
    // set the modal title
    document.getElementById("editGameModalLabel").innerHTML = "Editing Game: " + game
    // Get the save and folder columns
    let existing_folders = Array.from(row.cells[3].children)
    let existing_folders_string = ""
    let existing_saves = Array.from(row.cells[4].children)
    let existing_saves_string = ""
    // loop through them
    for (folder in existing_folders){
        if (existing_folders.length-1 == folder){
            existing_folders_string += existing_folders[folder].innerHTML
        } else {
            existing_folders_string += existing_folders[folder].innerHTML + ","
        }
    }
    for (save in existing_saves){
        if (existing_saves.length-1 == save){
            existing_saves_string += existing_saves[save].innerHTML
        } else {
            existing_saves_string += existing_saves[save].innerHTML + ","
        }
    }
    // set the input values
    document.getElementById("existing-save-folders").value = existing_folders_string
    document.getElementById("existing-save-files").value = existing_saves_string
    // add the event listener to the save button
    document.getElementById("save-game").addEventListener("click", function(){
        saveGame(game)
    })
    // Show the modal
    $('#editGameModal').modal('show');
}

function saveGame(game){
    // get the table row
    row = document.getElementById(game)
    // get the input values
    new_save_folders_input = document.getElementById("existing-save-folders").value
    new_save_files_input = document.getElementById("existing-save-files").value
    folders_cell = row.cells[3]
    files_cell = row.cells[4]
    if(new_save_folders_input == "" && new_save_files_input == ""){
        alert("You must at-least provide 1 file or 1 folder!")
        return
    }
    // split them
    new_save_folders = new_save_folders_input.split(",")
    new_save_files = new_save_files_input.split(",")

    if(new_save_folders.length > 0 && new_save_folders[0] != ""){
        // blank the existing data
        folders_cell.innerHTML = ""
        for(let i = 0; i < new_save_folders.length; i++){
            folders_cell.innerHTML += "<div id='"+ game +"-folder-"+ i +"'>" + new_save_folders[i] + "</div>"
        }
    } else {
        new_save_folders = []
    }
    if(new_save_files.length > 0 && new_save_files[0] != ""){
        // blank the existing data
        files_cell.innerHTML = ""
        for(let i = 0; i < new_save_files.length; i++){
            files_cell.innerHTML += "<div id='"+ game +"-file-"+ i +"'>" + new_save_files[i] + "</div>"
        }
    } else {
        new_save_files = []
    }
    // update the game in the structure/object
    s[game] = {
        "files": new_save_files,
        "folders": new_save_folders
    }
    // Close the modal
    $('#editGameModal').modal('hide');

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
    // If we get to this point it's not
    // So let's get the save folders and files
    let save_files = document.getElementById("save-files")
    let save_folders = document.getElementById("save-folders")
    // make sure both aren't blank
    if(save_files.value == "" && save_folders.value == ""){
        alert("You must at-least provide 1 file or 1 folder!")
        return
    }
    // Let's split them into a list
    let saves = save_files.value.split(",")
    let folders = save_folders.value.split(",")

    // Now let's add them to the table!
    let table = document.getElementById("saves_table")
    // creating new row
    let new_row = table.insertRow(-1)
    new_row.id=new_game_id
    // create the new row's columns
    let game_id_cell = new_row.insertCell(0)
    let game_name_cell = new_row.insertCell(1)
    let game_region_cell = new_row.insertCell(2)
    let folders_cell = new_row.insertCell(3)
    let files_cell = new_row.insertCell(4)
    let edit_cell = new_row.insertCell(5)
    edit_cell.innerHTML = "<i style='cursor: pointer;' class='far fa-pencil'></i>"
    edit_cell.addEventListener("click", function(){
        egModalLoad(new_game_id)
    })
    // inserting data into the columns
    game_id_cell.innerHTML = new_game_id
    game_name_cell.innerHTML = game_select.options[game_select.selectedIndex].text
    game_region_cell.innerHTML = game_region_select.options[game_region_select.selectedIndex].text
    // check to see if we have a folder
    if(folders.length > 0 && folders[0] != ""){
        for(let i = 0; i < folders.length; i++){
            folders_cell.innerHTML += "<div id='"+ new_game_id +"-folder-"+ i +"'>" + folders[i] + "</div>"
        }
    } else {
        folders = []
    }
    if(saves.length > 0 && saves[0] != ""){
        for(let i = 0; i < saves.length; i++){
            files_cell.innerHTML += "<div id='"+ new_game_id +"-file-"+ i +"'>" + saves[i] + "</div>"
        }
    } else {
        saves = []
    }
    // Now add the rew game to the existing array
    existing.push(new_game_id)
    // and add it to the extraSaves struct/object
    s[new_game_id] = {
        "files": saves,
        "folders": folders
    }
    // close the modal
    $('#newGameModal').modal('hide');
}


function download(){
    // set the config_file extraSaves to the new one
    config_file.extraSaves = s
    // credit: https://stackoverflow.com/a/30800715
    var dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(config_file, null, 2));
    var downloadAnchorNode = document.createElement('a');
    downloadAnchorNode.setAttribute("href",     dataStr);
    downloadAnchorNode.setAttribute("download", "config" + ".json");
    document.body.appendChild(downloadAnchorNode); // required for firefox
    downloadAnchorNode.click();
    downloadAnchorNode.remove();
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