// script.js
const message = "Hello from Node.js!";
console.log(message);

// You can also access command-line arguments passed from Python
const arg = process.argv[2]; 
if (arg) {
    console.log("Argument received in Node:", arg);
}
