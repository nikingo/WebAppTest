console.log("requestTest.js is called");
const request = new XMLHttpRequest();
request.open("GET", `http://localhost:3000/`);
request.addEventListener("load", (event) => {
    console.log(event.target.status); // => 200
    console.log(event.target.responseText); // => "{...}"
});
request.send();
console.log("334");