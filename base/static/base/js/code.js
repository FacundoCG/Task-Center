const textarea = document.getElementById("txt");

textarea.addEventListener("input", function (e) {
  this.style.height = this.scrollHeight + "px";
});

function textAreaAdjust(element) {
  element.style.height = "1px";
  element.style.height = (element.scrollHeight)+"px";
}
