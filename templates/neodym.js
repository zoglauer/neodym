 
 console.log("Neodym.js"); 
 
// The menu interface
var SubMenuShown = false;
 
function ToggleSubMenu() {
  SubMenuShown = !SubMenuShown;
  var SubMenu = document.getElementById("nd-mainmenu");
  if (SubMenuShown == true) {
    SubMenu.classList.add("nd-mainmenushow");
    document.getElementById("nd-menubutton-text").innerHTML = "&times;";
  } else {
    SubMenu.classList.remove("nd-mainmenushow");
    document.getElementById("nd-menubutton-text").innerHTML = "&equiv;";
  }
}
function DeactivateSubMenu() {
  SubMenuShown = false;
  var SubMenu = document.getElementById("nd-mainmenu");
  SubMenu.classList.remove("nd-mainmenushow");
  document.getElementById("nd-menubutton-text").innerHTML = "&equiv;";
}
