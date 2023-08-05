let type = document.getElementById("type")
function select(id) {
  type.value = id;
  document.getElementById("demo").innerHTML = ('Selected: ' + type.value);
}
