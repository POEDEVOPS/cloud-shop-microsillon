let loggedIn = "";
let loginPage = document.getElementById("login-page");
let guestPage = document.getElementById("guest-page");
let startPage = document.getElementById("start-page");
let logitem =  document.getElementById("login");
let shopData = "";
let albums = "";
let artists = "";
let cart = "";


// fetch shop data
fetch(`shop/`)
.then(response => response.json())
.then(data => 
{
    if (data.toString() === "401")
    {
        console.log("No shop info found");
    }
    else
    {
       shopData = data;
       document.getElementById("shopname").innerHTML=shopData[0].name.toUpperCase();
       document.getElementById("musicstyle").innerHTML=shopData[0].style.toLowerCase();
       console.log(shopData);
    }
});

// fetch album data
fetch("albums/")
.then(response => response.json())
.then(data => 
{
    if (data.toString() === "401")
    {
        console.log("No shop info found");
    }
    else
    {
       albums = data;
       console.log(albums);
    
       // affichage couvertures main page
       document.getElementById("cover1").src=`/${albums[0].art}`;
       document.getElementById("cover2").src=`/${albums[1].art}`;
    }
});

// fetch artists data
fetch("artists/")
.then(response => response.json())
.then(data => 
{
    if (data.toString() === "401")
    {
        console.log("No shop info found");
    }
    else
    {
       artists = data;
       console.log(artists);
    }
});


function login()
{
    if (loggedIn === "")
    {
        loginPage.removeAttribute("hidden");
        loggedIn="user"
    }
    else
    {
        loginPage.setAttribute("hidden", "");
        logitem.innerHTML="login";
        loggedIn="";
        guestPage.setAttribute("hidden", "");
        startPage.removeAttribute("hidden");
        document.getElementById("welcome").innerHTML=`Welcome`;
        console.log("logged out")
    }
}

function authme()
{
    username = document.getElementById("username").value;
    password = document.getElementById("password").value;
    
    if (username.length > 0 && password.length > 0)
    {
        fetch(`users/${username}/${password}`)
        .then(response => response.json())
        .then(data => 
        {
            if (data.toString() === "401")
            {
                console.log("Incorrect creds")
                document.getElementById("wrong-creds").removeAttribute("hidden");
            }
            else
            {
                if (data.role === "client")
                {
                    console.log("Welcome client");
                    loggedIn="client";
                    startPage.setAttribute("hidden", "");
                    guestPage.removeAttribute("hidden");
                    displayCards();
                }
                else if (data.role === "admin")
                {
                    console.log("Welcome admin");
                    loggedIn="admin";
                }

                loginPage.setAttribute("hidden", "");
                logitem.innerHTML="logout";
                document.getElementById("welcome").innerHTML=`Welcome, ${username} ! `;
            }

            password.value="";
        });
    }

}

function displayCards()
{
    let card = "";

    albums.forEach(el => 
    {
        card+='<div class="card music-card" style="width: 18rem;margin: 10px;">';
        card+=`<img class="card-img-top " src="/${el.art}">`;
        card+='<div class="card-body">';
        card+=`<h5 class="card-title">${el.title}</h5>`;
        card+=`<p class="card-text"><b>Artist &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</b>${el.name}<br><b>Year &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</b> ${el.price}<br><b>Price &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</b>${el.price}.00€</p>`;
        card+='<a href="#" class="btn btn-primary">Add to cart</a>'
        card+='</div></div>';
    });

    guestPage.innerHTML = card;

}