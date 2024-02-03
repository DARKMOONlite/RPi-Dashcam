const express = require('express');
const cors = require('cors');

const app = express();

app.use(cors());

// your routes here

app.listen(3000, () => console.log('Server started'));


// Get the button element
const button = document.getElementById('fetchButton');

// Add a click event listener to the button
button.addEventListener('click', () => {
    console.log("Button clicked")
    // Fetch item data from the backend when the button is clicked
    fetch('http://192.168.0.136/items/1')
        .then(response => response.json())
        .then(data => {
            console.log("Item data fetched: ", data)
            // Create a div to display the item
            const itemDiv = document.createElement('div');

            // Add the item data to the div
            itemDiv.textContent = `Item: ${data.name}, Price: ${data.price}`;

            // Add the div to the body of the document
            document.body.appendChild(itemDiv);
            
        })
        .catch(error => {
            console.error('Error:', error);
        });
});