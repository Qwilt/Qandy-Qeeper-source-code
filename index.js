	function openBox()
	{			
		document.getElementById('login').style.display = "none";
		document.getElementById('spinner').style.display = "block";
		var test = setTimeout(validateCredentials,2000);
	}

	function createUser()
	{			
		document.getElementById('login').style.display = "none";
		document.getElementById('spinner').style.display = "block";
		var test = setTimeout(addUserToDB,2000);
	}
	
	function validateCredentials()
	{
		document.getElementById('spinner').style.display = "none";

		var password = document.getElementById('password').value;
		var userName = document.getElementById('username').value;
		alert("username is " + userName + " and password is " + password);

	}

	function addUserToDB()
	{
		document.getElementById('spinner').style.display = "none";

		var userPassword = document.getElementById('userpassword').value;
		var userName = document.getElementById('username').value;
		var adminPassword = document.getElementById('adminpassword').value;
		var openAmount = document.getElementById('openamount').value;
		alert("Creating user: admin with password " + adminPassword + " created username " + userName + " with password " + userPassword + " and amount of box opennings for a week: " + openAmount );

	}